import json
import sys
import glob, os

os.chdir(sys.argv[1])

for file in glob.glob("*.json"):
    f=open(file, "r")
    # print(file)
    text = f.read()
    y = json.loads(text)
    f.close()
    valvecount = 0

    for featurelayer in y['features']:
        if featurelayer['name'] == "control":
            features = featurelayer['features']
            for key in features:
                feature = features[key]
                if feature['macro'] == "Valve" or feature['macro'] == "Valve3D":
                    valvecount+=1

    print(file + "," + str(valvecount))







