import json
import sys
import glob, os

typemap = dict()
typelist = ["Connection"]
benchmarkdata = dict()

def incrementComponentCount(key):
    if key not in typelist:
        typelist.append(key)

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
    typemap = dict()

    for featurelayer in y['features']:
        features = featurelayer['features']
        for key in features:
            feature = features[key]
            if feature['macro'] == "Channel" or feature['macro'] == "Connection" or feature['macro'] == "RoundedChannel":
                connectioncount+=1
            elif feature['macro'] == "EDGE" or feature['macro'] == "Transition" or feature['macro'] == "Pump_control" or feature['macro'] == "Valve_control":
                continue
            elif feature['macro'] == "CurvedMixer":
                incrementComponentCount("Mixer")
            else:
                incrementComponentCount(feature['macro'])

    typemap["Connection"] = connectioncount

    benchmarkdata[file] = typemap

    # for key in typemap.keys():
    #     print(file + "," + key + "," + str(typemap[key]))

    # print(file + "," + "Channel," + str(connectioncount))

# print(benchmarkdata)
# print(typelist)
#Print header
print("Benchmark", end="")
for typename in typelist:
    print(",", end="")
    print(typename, end="")
print("")
for benchmark in benchmarkdata:
    print(benchmark + ", ", end="")
    benchmarkdict = benchmarkdata[benchmark]
    isfirst = True
    for typename in typelist:
        if not isfirst:
            print(", " , end="")
        else:
            isfirst = False
        if(typename in benchmarkdict):
            print(str(benchmarkdict[typename]), end="")
        else:
            print(0, end="")
    print("")










