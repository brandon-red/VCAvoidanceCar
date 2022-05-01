import math

def l2norm(vector):
    d = 0
    for entry in vector: d += entry**2
    return math.sqrt(d)

def subtract_all_signatures(fingerprint, signature, common_keys):
    # returns distance between received signature and all known locations
    # return is a list of tuples
    # each tuple contains (name of known location, the distance vector between received signature and known location)
    temp = []
    
    for MAC in common_keys:
        dist = signature[MAC] - fingerprint[MAC]
        temp.append(dist)
    return temp