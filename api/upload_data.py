import numpy as np
import os
from shutil import copy2 as copy
from glob import glob
from vessel import Vessel
from filters import *
import re
from ipdb import set_trace as debug
import pandas as pd
from zipfile import ZipFile
from datetime import datetime
from os.path import expanduser
from datetime import datetime
import json


DOCKER = True

# Temporary data file location.
if DOCKER:
    TEMP_LOC = '/app/api/data/tmp'
    ARXIV_LOC = '/app/api/data/arxiv'
    CSV_LOC = '/app/api/data/csv'
    ZIP_LOC = '/app/api/data/zip'
    WEB_LOC = '/app/dist/static/zipped/'
else:
    TEMP_LOC = './data/tmp'
    ARXIV_LOC = './data/arxiv'
    CSV_LOC = './data/csv'
    ZIP_LOC = './data/zip'
    WEB_LOC = '../static/zipped/'

MAXVAL = 2**24-1
MAXREF = 2.5
COVFAC = MAXREF*(1/MAXVAL)


def get_board_name(volume_name):
    '''Extract the board name from the volume name.'''
    color = volume_name[9:]
    return 'bio_{:s}'.format(color.lower())


def build_and_merge(volume_name, annotation_file):
    '''Build and merge the data.'''

    # Name that board!
    board_name = get_board_name(volume_name)

    # Extract annotations.
    annotations, time_syncs, time_delta = \
            process_annotation_file(annotation_file, board_name)

    # Grab the data from the SD card.
    upload_data()

    # Process data in the temporary folder; create CSV files, too.
    process_data(time_delta, annotations, volume_name)


def process_annotation_file(annotation_filename, board_name):
    '''Process annotation file in ~/Downloads.'''
    text = open(annotation_filename, 'r').read()
    data = json.loads(text)

    # Extract annotations.
    board_data = data[board_name]
    print(board_data)
    annotations = {'content': [], 'datetime': [], 'unix_time': []}
    time_syncs = []
    for entry in board_data:
        if entry['content'] != '!':
            # A legit annotation.
            annotations['content'].append(entry['content'])
            annotations['unix_time'].append(entry['start_time'])
            annotations['datetime'].append(datetime.fromtimestamp(entry['start_time']).\
                    strftime('%Y-%m-%d %H:%M:%S'))
        else:
            # Extract time syncs.
            sync = {'datetime': entry['date']}
            sync['start_tick'] = entry['start_tick']
            sync['start_time'] = entry['start_time']
            time_syncs.append(sync)

    mean_delta = np.mean([(s['start_time']-s['start_tick']) for\
            s in time_syncs])

    print(time_syncs, mean_delta)
    return annotations, time_syncs, mean_delta


def timestamp():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


def extract_pid(volume_name):
    '''Extract PID from the config.old file.'''
    rgx = 'PID: (\d+)'
    config = open('{:s}/config.old'.format(volume_name)).readline()
    pid = re.search(rgx, config)
    pid = pid[1] if pid else None
    return pid


def find_sd_cards():
    '''Find valid SD cards.'''
    # Define valid SD cards.
    valid_volumes = ['YELLOW', 'ORANGE', 'PINK', 'WHITE', 'PURPLE']
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


def create_csv(data, annotations):
    '''Create CSV files containing the data.'''
    files_to_compress = []
    zip_location = '{:s}/{:s}.zip'.format(ZIP_LOC, data.pid)
    for c, channel_name in enumerate(['PZT', 'PPG', 'IMP']):
        filename = '{:s}/{:s}_{:s}.csv'.format(CSV_LOC, data.pid, channel_name)
        files_to_compress.append(filename)
        data_dict = {'timestamps': data.t[c], 'datetime': data.datetime[c],
                'values': data.v[c], 'filtered values (lowpass; 10 Hz)':
                data.vf[c]}
        df = pd.DataFrame(data_dict)
        df = df[['timestamps', 'datetime', 'values',\
                'filtered values (lowpass; 10 Hz)']]
        df.to_csv(filename)

    # Now save the annotations
    annot_filename = '{:s}/{:s}_annotations.csv'.format(CSV_LOC, data.pid)
    files_to_compress.append(annot_filename)
    data_dict = annotations
    df = pd.DataFrame(data_dict)
    df = df[['unix_time', 'datetime', 'content']]
    df.to_csv(annot_filename)

    # Now save all files as compressed zip file.
    with ZipFile(zip_location, 'w') as f:
        for filename in files_to_compress:
            f.write(filename)

    # Copy the zipped file to the static web server.
    copy(zip_location, WEB_LOC)


def format_date(unix_time):
    '''Convert unix time to datetime string.'''
    return datetime.fromtimestamp(unix_time).\
            strftime('%Y-%m-%d %H:%M:%S')


def process_data(time_offset, annotations, volume_name):
    '''Process all data in the temporary directory.'''

    # Here is the total.
    biomonitor_regex = r"(B1)\s*(\d*)\s*(\w{0,8})\s*(\w*)"
    data_files = glob('{:s}/*.dat'.format(TEMP_LOC))

    # Verify that data files have been transferred.
    if len(data_files)>0:
        pid = extract_pid(volume_name)
        data = Vessel('{:s}/{:s}.dat'.format(ARXIV_LOC, pid))
        data.pid = pid
        data.uploaded_at = timestamp()
        data.t_ = {}
        data.datetime = {}
        data.t = {}
        data.v = {}
        data.vf = {}

        # Set up channels.
        for k in [0,1,2]:
            data.t[k] = []
            data.t_[k] = []
            data.datetime[k] = []
            data.v[k] = []

        # Extract data from files.
        for itr, data_file in enumerate(data_files):
            data = read_data_file(data_file, data)

        # Sort the data based on time; low-pass filter that shit.
        for c in [0,1,2]:
            idx = np.argsort(data.t[c])
            data.t[c] = np.array(data.t[c])[idx]
            data.v[c] = np.array(data.v[c])[idx]
            data.t[c] = data.t[c]
            data.t[c] = data.t[c] * 1e-6
            data.t_[c] = data.t[c] + time_offset
            data.datetime[c] = [format_date(ts) for ts in data.t_[c]]
            vf, _ = lowpass(data.t[c], data.v[c], freq_cutoff=10)
            data.vf[c] = np.array(vf)

        # Archive the data using Vessel format.
        data.duration = '{:0.2f}'.format(data.t[0].max()/60)
        data.save()

        # Write out CSV data and zip it up.
        create_csv(data, annotations)
        for dfile in data_files:
            os.remove(dfile)

        return data


if __name__ == '__main__':

    annotation_filename = '/Users/mjl/Downloads/annotations.txt'
    volume_name = '/Volumes/ORANGE'

    # out = process_annotation_file(annotation_filename, board_name)
    build_and_merge(volume_name, annotation_filename)

