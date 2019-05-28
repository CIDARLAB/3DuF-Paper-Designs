import json
import sys
import glob, os

typemap = dict()

def incrementComponentCount(key):
    if key in typemap.keys():
        value = typemap[key]
        typemap[key] = value + 1
    else:
        typemap[key] = 1


os.chdir(sys.argv[1])

for file in glob.glob("*.json"):
    f=open(file, "r")
    # print(file)
    text = f.read()
    y = json.loads(text)
    f.close()
    connectioncount = 0
    componentcount = 0

    for featurelayer in y['features']:
        features = featurelayer['features']
        for key in features:
            feature = features[key]
            if feature['macro'] == "Channel" or feature['macro'] == "Connection" or feature['macro'] == "RoundedChannel":
                connectioncount+=1
            elif feature['macro'] !="EDGE" and feature['macro'] !="Transition":
                componentcount+=1


    print(file + "," + str(componentcount) + "," + str(connectioncount))







