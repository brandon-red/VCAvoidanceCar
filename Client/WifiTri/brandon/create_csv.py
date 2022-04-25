"""
How to Run:

1. Place Raspberry Pi at a beacon location and
determine which beacon it should be: A, B, or C.

2. Run this program for each location A, B and C.
    a. When asked to input name of location,
       specify which beacon it is: A, B or C. 

3. Place Raspberry Pi at any location and run this program
    a. When asked to input name of location, input any name,
       but remember it as it will be needed to get position

4. After completing step 3, run get_pos.py to obtain location
   of the Raspberry Pi in relation to the beacons.
"""
import os
import time
import itertools as iter
from csv import writer


WIFI_SCAN_CMD = 'sudo iwlist wlan0 scan | grep -E Address\\|Signal\\ level'
print('Gathering location data from Raspberry Pi...')
# write data from scan to text file
with open('data.txt', 'w') as f:
	sample = 0
	for i in range(60):
		scan_rst = os.popen(WIFI_SCAN_CMD).read()
		time.sleep(0.5)
		f.write(scan_rst)
		sample+=1

# ask user to input name of location to differentiate locations
location = input('Input name of location (A, B, C) or if unknown, input a name of your choice:')
# parse scan data and create csv file
with open('data.txt') as f:
	csv_file = location + "database.csv"
	with open(csv_file, 'w', newline='') as csv_f:
		csv_w = writer(csv_f)
		csv_w.writerow(['MAC', 'RSSI'])
		for line1,line2 in iter.zip_longest(*[f]*2):
			l1 = line1.strip()
			l2 = line2.strip()
			# gets index of where MAC address starts
			address = l1.split('Address: ')[1]
			# gets RSSI value
			rssi = l2.split(' ')[3].replace('level=', '')
			csv_w.writerow([address, rssi])
print('Data obtained and stored successfully.\nIf location is "unk" run get_pos.py to determine location of Raspberry Pi.')
print('If location is A, B, or C, continue gathering data for preset locations until ready.')