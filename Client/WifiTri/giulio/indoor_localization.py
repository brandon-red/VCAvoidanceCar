from fileinput import close
import json
import data_collect
import math
import sys

NUM_LOCATIONS = 3 #Constant number of locations at which we measure create an fingeprint table


def l2norm(vector):
    d = 0
    for entry in vector: d += entry**2
    return math.sqrt(d)

def subtract_all_signatures(table, common_signatures):
    # returns distance between received signature and all known locations
    # return is a list of tuples
    # each tuple contains (name of known location, the distance vector between received signature and known location)
    temp = []
    
    for MAC in common_signatures:
        dist = common_signatures[MAC] - table[MAC]
        temp.append(dist)
    return temp


if __name__ == "__main__":

    table_list = []

    # Read in all fingerprint tables and store them in an array
    for i in range(0, NUM_LOCATIONS):
        print("Enter the name of the fingerprint table with the following format <name of location>_table.json")
        print("<name of location> should be a letter of the alphabet and it should be different for all entries")
        filename = str(input())
        letter = filename[0:1].upper()
        f = open(filename)
        table = json.loads(f.read())
        table_list.append((letter, table)) # store fingerprint table and its corresponding location name
        f.close()

# obtain common MAC addresses between RSSI of all known locations
keys_list = []
for tup in table_list: keys_list.append(set(tup[1].keys()))
common_keys = keys_list[0].intersection(*keys_list)

current_table = dict()
current_table = data_collect.do_scan(current_table) # get fingerprint table at new location

# Must remove signatures from current position that are not in common with all other locations
# Instead of removing entries that are not in common with known locations we just create a new dictionary with all common entries

current_table_common = dict()
for MAC in current_table:
    if MAC in common_keys: current_table_common[MAC] = current_table[MAC]

# Compute the distance between current location and each RSSI signature from known location
distance_vector = [] 
for tup in table_list:
    name = tup[0]
    table = tup[1]
    temp = subtract_all_signatures(table, current_table_common)
    distance_vector.append((name, temp))

# Compute l2 norm using distance vectors computed above
estimates = []
for tup in distance_vector:
    name = tup[0]
    distance = tup[1]
    norm = l2norm(distance)
    estimates.append((name, norm))

# Go through all estimates and determine the smallest one making sure to remember the name of the location with smallest value
closest_location = ""
sign = sys.maxsize
for entry in estimates:
    if(entry[1] < sign):
        sign = entry[1]
        closest_location = entry[0]

# Print estimated location
print("Your current location is close to point {0}".format(closest_location))
    
