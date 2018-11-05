#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar


#PORT_NAME = '/dev/ttyUSB0'


def run(PORT_NAME):
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    data = []
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for scan in lidar.iter_scans():
            print(scan)
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()

if __name__ == '__main__':
    run(sys.argv[1])
