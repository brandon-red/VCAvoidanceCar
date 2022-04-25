"""
How to run:

1. Ensure that all 3 beacons (A, B, C) have been initialized
   by running create_csv.py at all 3

2. After running create_csv.py on arbitrary location, run this program

3. Input name that you inputted when running create_csv.py when prompted
"""
import csv
import numpy as np

def parse_csv(loc_name, data):
	"""
	Returns a dictionary containing data from
	csv file based on name of location
	"""
	data[loc_name] = dict()
	filename = loc_name + 'database.csv'
	with open(filename) as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['MAC'] not in data[loc_name]:
				data[loc_name][row['MAC']] = []
				data[loc_name][row['MAC']].append(int(row['RSSI']))
			else:
				data[loc_name][row['MAC']].append(int(row['RSSI']))
	return data

def data_avg(data):
	"""
	Returns a dataset containing the avg rssi from each MAC
	address for each location
	"""
	avg_rssi_data = dict()
	for key in data:
		avg_rssi_data[key] = dict()
		for mac in data[key]:
			avg_rssi_data[key][mac] = sum(data[key][mac])/len(data[key][mac])
	return avg_rssi_data
	
def get_intersection(unk_name, loc_name, data_avg):
	"""
	Returns the similar MACs between an unknown location
	and a preset location
	"""
	intersection = list(set(data_avg[unk_name].keys()).intersection(set(data_avg[loc_name].keys())))
	return intersection
	
def get_euc_dist(unk_d, loc_name, data_avg):
	"""
	Returns the euclidian distance between unknown location and a given preset
	based name of unknown location, name of preset location
	and database holding avg rssi for each mac from all locations
	"""
	inter = get_intersection(unk_name, loc_name, data_avg)
	unk_rssi = np.array([])
	loc_rssi = np.array([])
	for item in inter:
		unk_rssi = np.append(unk_rssi, data_avg[unk_name][item])
		loc_rssi = np.append(loc_rssi, data_avg[loc_name][item])
	subtracted = np.zeros(len(inter))
	np.subtract(unk_rssi, loc_rssi, subtracted)
	euc_dist = np.linalg.norm(subtracted)
	print('Distance between {} and {} is {}'.format(unk_name, loc_name, euc_dist))
	return euc_dist

unk_name = input('What did you name the unknown location?')
print('Determining if {} is located nearest to A, B, or C...')

# initialize database	
data = dict()
locs = ['A', 'B', 'C']
for loc in locs:
	new_data = parse_csv(loc, data)
	data.update(new_data)

# obtain data for unknown location
newloc = parse_csv(unk_name, data)
data.update(newloc)

# setup calculations to determine location
rssi_comp = {'A': 0, 'B':0, 'C':0}
for loc in locs:
	rssi_comp[loc]=get_euc_dist(unk_name, loc, data_avg(data))	
closest_rssi = min(rssi_comp['A'], rssi_comp['B'], rssi_comp['C'])
print("Raspberry Pi located at {}".format(list(rssi_comp.keys())[list(rssi_comp.values()).index(closest_rssi)])) 


