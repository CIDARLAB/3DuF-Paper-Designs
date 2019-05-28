import json
import sys
import glob, os
import csv

typemap = dict()

design_effort_3DuF = dict()
parametric_effort_3DuF = dict()

design_effort_other = dict()
parametric_effort_other = dict()

total_benchmarkcost_other = dict()
total_benchmarkcost_3DuF = dict()

design_benchmarkcost_3DuF = dict()
parametrization_benchmarkcost_3DuF = dict()

design_benchmarkcost_other = dict()
parametrization_benchmarkcost_other = dict()

def incrementComponentCount(key):
    if key in typemap.keys():
        value = typemap[key]
        typemap[key] = value + 1
    else:
        typemap[key] = 1

def incrementBenchmarkCost_3DuF(key, design_cost, parametrization_cost):
    if key in total_benchmarkcost_3DuF.keys():
        value = total_benchmarkcost_3DuF[key]
        total_benchmarkcost_3DuF[key] = value + design_cost + parametrization_cost
    else:
        total_benchmarkcost_3DuF[key] = design_cost + parametrization_cost

    if key in design_benchmarkcost_3DuF.keys():
        value = design_benchmarkcost_3DuF[key]
        design_benchmarkcost_3DuF[key] = value + design_cost
    else:
        design_benchmarkcost_3DuF[key] = design_cost 

    if key in parametrization_benchmarkcost_3DuF.keys():
        value = parametrization_benchmarkcost_3DuF[key]
        parametrization_benchmarkcost_3DuF[key] = value + parametrization_cost
    else:
        parametrization_benchmarkcost_3DuF[key] = parametrization_cost


def incrementBenchmarkCost_other(key, design_cost, parametrization_cost):
    if key in total_benchmarkcost_other.keys():
        value = total_benchmarkcost_other[key]
        total_benchmarkcost_other[key] = value + design_cost + parametrization_cost
    else:
        total_benchmarkcost_other[key] = design_cost + parametrization_cost

    if key in design_benchmarkcost_other.keys():
        value = design_benchmarkcost_other[key]
        design_benchmarkcost_other[key] = value + design_cost
    else:
        design_benchmarkcost_other[key] = design_cost 

    if key in parametrization_benchmarkcost_other.keys():
        value = parametrization_benchmarkcost_other[key]
        parametrization_benchmarkcost_other[key] = value + parametrization_cost
    else:
        parametrization_benchmarkcost_other[key] = parametrization_cost


#Begin reading the costs

with open('3DuF-PrimitivesEffort.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    firstline = True
    for row in csv_reader:
        if firstline:    #skip first line
            firstline = False
            continue
        newkey = row[0].replace(" ", "").lower()
        design_effort_3DuF[newkey] = float(row[2])
        parametric_effort_3DuF[newkey] = float(row[7])

with open('ACSW-PrimitiveEffort.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    firstline = True
    for row in csv_reader:
        if firstline:    #skip first line
            firstline = False
            continue
        newkey = row[0].replace(" ", "").lower()
        design_effort_other[newkey] = float(row[4])
        parametric_effort_other[newkey] = float(row[9])

print(design_effort_3DuF)
print(parametric_effort_3DuF)
print(design_effort_other)
print(parametric_effort_other)

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

            ####### Get the  component connection distributions
            if feature['macro'] == "Channel" or feature['macro'] == "Connection" or feature['macro'] == "RoundedChannel":
                connectioncount+=1
            else:
                incrementComponentCount(feature['macro'])
            
            ###### Compute the Efforts
            macro = feature["macro"].replace(" ", "").lower()

            if(macro == "chamber"):
                macro = "reactionchamber"
            elif macro == "roundedchannel" or macro == "connection":
                macro = "channel"
            
            if (macro in design_effort_3DuF) and (macro in parametric_effort_3DuF):
                
                design_cost = design_effort_3DuF[macro]
                parametrization_cost = parametric_effort_3DuF[macro]

                incrementBenchmarkCost_3DuF(file, design_cost, parametrization_cost)
            
            elif(macro == "pump"):
                design_cost = design_effort_3DuF["channel"]
                parametrization_cost = parametric_effort_3DuF["channel"]

                incrementBenchmarkCost_3DuF(file, design_cost, parametrization_cost)

            elif(macro == "pump_control"):
                design_cost = 3*design_effort_3DuF["valve"]
                parametrization_cost = 3*parametric_effort_3DuF["valve"]

                incrementBenchmarkCost_3DuF(file, design_cost, parametrization_cost)

            elif (macro == "mixer") or (macro == "curvedmixer"):
                design_cost = 1
                parametrization_cost = 8

                incrementBenchmarkCost_3DuF(file, design_cost, parametrization_cost)
            
            elif (macro == "tree"):
                design_cost = 1
                parametrization_cost = 8

                incrementBenchmarkCost_3DuF(file, design_cost, parametrization_cost)
            
            else:
                print("Could not find 3DuF component design cost:" + macro)


#####################################
            
            if (macro in design_effort_other) and (macro in parametric_effort_other):

                design_cost = design_effort_other[macro]
                parametrization_cost = parametric_effort_other[macro]

                incrementBenchmarkCost_other(file, design_cost, parametrization_cost)
              
            elif(macro == "pump"):
                design_cost = design_effort_other["channel"]
                parametrization_cost = parametric_effort_other["channel"]

                incrementBenchmarkCost_other(file, design_cost, parametrization_cost)

            elif(macro == "pump_control"):
                design_cost = design_effort_other["valve"]
                parametrization_cost = parametric_effort_other["valve"]

                incrementBenchmarkCost_other(file, design_cost, parametrization_cost)
  
            elif (macro == "mixer") or (macro == "curvedmixer"):
                params = feature["params"]
                
                scalefactor = float(params["numberOfBends"])
                # print("TODO: Add mixer calculate function", scalefactor)


                design_cost = 6 * scalefactor
                parametrization_cost = 40

                incrementBenchmarkCost_other(file, design_cost, parametrization_cost)

                
            elif (macro == "tree"):
                params = feature["params"]
                scalefactor = float(params["leafs"])
                # print("TODO: Add tree calculate function", scalefactor)
                
                design_cost = 4 * pow(scalefactor,2)/2
                parametrization_cost = 60

                incrementBenchmarkCost_other(file, design_cost, parametrization_cost)

            else:
                print("Could not find 3DuF component parametrization cost:" + macro)
        
    
    # print(total_benchmarkcost_3DuF)
    # print(total_benchmarkcost_other)
    # print(design_benchmarkcost_3DuF)
    # print(parametrization_benchmarkcost_3DuF)
    # print(design_benchmarkcost_other)
    # print(parametrization_benchmarkcost_other)

for key in total_benchmarkcost_3DuF:
    print(key, design_benchmarkcost_3DuF[key], parametrization_benchmarkcost_3DuF[key], total_benchmarkcost_3DuF[key], design_benchmarkcost_other[key], parametrization_benchmarkcost_other[key], total_benchmarkcost_other[key], sep=",")


    #print(file + "," + "Channel," + str(connectioncount))

    #Compute the Efforts









