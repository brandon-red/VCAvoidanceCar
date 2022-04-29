import os
import json
 
def do_scan(fingerprint):
    WIFI_SCAN_CMD = 'sudo iwlist wlan0 scan | grep -E Address\|Signal\ level'
    scan_rst = os.popen(WIFI_SCAN_CMD).read()

    #Parse entries in the list
    scan_list = scan_rst.split('\n')
    for i in range(0, len(scan_list)-1, 2):
        MAC = scan_list[i].strip()[19:36]
        strength = int(scan_list[i+1].strip()[28:31])
        if MAC in fingerprint: fingerprint[MAC] += strength
        else: fingerprint[MAC] = strength
    return fingerprint
    
    
if __name__ == "__main__":

    print("Enter the name of the file you will write to with the following format <name of location>_table.json")
    print("<name of location> should be a letter of the alphabet and it should be different for all entries")
    filename = str(input())
    
    fingerprint = dict()
    # scan the same location 60 times
    i = 0
    while(i<60):
        fingerprint = do_scan(fingerprint)
        i += 1
    # Compute average RSSI signature at current location
    for entry in fingerprint: fingerprint[entry] /= 60
    f = open(filename,'w')

    f.write(json.dumps(fingerprint))
    f.close()
            


