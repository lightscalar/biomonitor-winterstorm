from glob import glob
import os


def configure_card(config):
    '''Configure SD card for Biomonitor data collections.'''
    config_filename = '{:s}/config.txt'.format(config['volume'])
    old_filename = '{:s}/config.old'.format(config['volume'])
    data_filenames = '{:s}/*.dat'.format(config['volume'])
    data_files = glob(data_filenames)
    pid = config['id']
    duration = config['duration']
    config_files = glob(config_filename)
    if len(config_files)>0:
        os.remove(config_filename)
    if len(data_files)>0:
        for datafile in data_files:
            os.remove(datafile)
    try:
        os.remove(old_filename)
    except:
        pass
    f = open(config_filename, 'w')
    f.write('PID: {:s}\n'.format(pid))
    f.write('NDS: {:d}\n'.format(int(duration*60*60/19.29)))
    f.write('DSD: 3\n')
    f.close()
