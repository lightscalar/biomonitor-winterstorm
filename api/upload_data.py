import numpy as np
import os
from shutil import copy2 as copy
from glob import glob
from mathtools.utils import Vessel
from filters import *
import re
from ipdb import set_trace as debug
import pandas as pd
from zipfile import ZipFile
from datetime import datetime


# Temporary data file location.
TEMP_LOC = './data/tmp'
ARXIV_LOC = './data/arxiv'
CSV_LOC = './data/csv'
ZIP_LOC = './data/zip'
WEB_LOC = '../static/zipped/'
MAXVAL = 2**24-1
MAXREF = 2.5
COVFAC = MAXREF*(1/MAXVAL)


def timestamp():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


def find_sd_cards():
    '''Find valid SD cards.'''
    # Define valid SD cards.
    valid_volumes = ['YELLOW', 'BLUE', 'RED', 'WHITE', 'GREEN']
    valid_volumes = ['/Volumes/{:s}'.format(v) for v in valid_volumes]
    available_disks = glob('/Volumes/*')
    return [v for v in available_disks if v in valid_volumes]


def upload_data():
    '''Upload Biomonitor data from the board.'''
    for sd_card in find_sd_cards():
        data_files = glob('{:s}/*.dat'.format(sd_card))
        for data_file in data_files:
            copy(data_file, TEMP_LOC)


def get_pid(data_file):
    '''Extract PID of data files.'''
    rgx = '.*PID(\\d+)_'
    pid = re.search(rgx, data_file)
    pid = pid[1] if pid else None
    return pid


def translate_line(line):
    '''Translate a line from the Biomonitor device.'''
    biomonitor_regex = r"(B1)\s*(\d*)\s*(\w{0,8})\s*(\w*)"
    out = re.search(biomonitor_regex, line)
    channel_number, value, timestamp = None, None, None
    if out:
        # We caught something!
        if out.group(1) == 'B1':
            # Looks like we have some BioMonitor output.
            try: # channel number there?
                channel_number = int(out.group(2), 16)
            except:
                pass
            try: # value present?
                value = (int(out.group(3),16))*COVFAC
            except:
                pass
            try: # timestamp present?
                timestamp = (int(out.group(4),16))
            except:
                pass
    return channel_number, value, timestamp


def read_data_file(data_file, data):
    '''Read the data from specified file.'''

    # Read content from the file.
    with open(data_file, 'r', encoding='latin-1') as f:
        content = f.readlines()

    # Extract data line by line.
    for line in content:
        c, v, t = translate_line(line)
        if (c is not None) and (t is not None) and (v is not None):
            data.t[c].append(t)
            data.v[c].append(v)
    return data


def create_csv(data):
    '''Create CSV files containing the data.'''
    files_to_compress = []
    zip_location = '{:s}/{:s}.zip'.format(ZIP_LOC, data.pid)
    for c, channel_name in enumerate(['PZT', 'PPG', 'IMP']):
        filename = '{:s}/{:s}_{:s}.csv'.format(CSV_LOC, data.pid, channel_name)
        files_to_compress.append(filename)
        data_dict = {'timestamps': data.t[c], 'values': data.v[c],
                'filtered values (lowpass; 10 Hz)': data.vf[c]}
        df = pd.DataFrame(data_dict)
        df = df[['timestamps', 'values', 'filtered values (lowpass; 10 Hz)']]
        df.to_csv(filename)

    # Now save all files as compressed zip file.
    with ZipFile(zip_location, 'w') as f:
        for filename in files_to_compress:
            f.write(filename)

    # Copy the zipped file to the static web server.
    copy(zip_location, WEB_LOC)


def process_data():
    '''Process all data in the temporary directory.'''

    # Here is the total.
    biomonitor_regex = r"(B1)\s*(\d*)\s*(\w{0,8})\s*(\w*)"
    data_files = glob('{:s}/*.dat'.format(TEMP_LOC))

    # Verify that data files have been transferred.
    if len(data_files)>0:
        pid = get_pid(data_files[0])
        data = Vessel('{:s}/{:s}.dat'.format(ARXIV_LOC, pid))
        data.pid = pid
        data.uploaded_at = timestamp()
        data.t = {}
        data.v = {}
        data.vf = {}

        # Set up channels.
        for k in [0,1,2]:
            data.t[k] = []
            data.v[k] = []

        # Extract data from files.
        for itr, data_file in enumerate(data_files):
            data = read_data_file(data_file, data)

        # Sort the data based on time; low-pass filter that shit.
        for c in [0,1,2]:
            idx = np.argsort(data.t[c])
            data.t[c] = np.array(data.t[c])[idx]
            data.v[c] = np.array(data.v[c])[idx]
            data.t[c] = data.t[c] - data.t[c][0]
            data.t[c] = data.t[c] * 1e-6
            vf, _ = lowpass(data.t[c], data.v[c], freq_cutoff=10)
            data.vf[c] = np.array(vf)

        # Archive the data using Vessel format.
        data.duration = '{:0.2f}'.format(data.t[0].max()/60)
        data.save()

        # Write out CSV data and zip it up.
        create_csv(data)

        return data

