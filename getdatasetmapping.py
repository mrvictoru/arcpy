import arcpy, json

p = arcpy.mp.ArcGISProject('current')
m = p.activeMap
l = m.listLayers()
output_path = arcpy.GetParameter(0) # get Destination path

xlist = []

for layer in l:
    try:
        print(layer.connectionProperties['dataset'])
        if len(xlist) == 0:
            setdict = {
                "dataset": None,
                "feature": []
            }
            xlist.append(setdict)
        else:
            print("push new dict")
            print("set: " + setdict["dataset"])
            print(setdict["feature"])
            setdict = {
                "dataset": None,
                "feature": []
            }
            xlist.append(setdict)
        setdict["dataset"] = layer.connectionProperties['dataset']

    except:
        setdict["feature"].append(layer.name)

for x in xlist:
    json_object = json.dumps(x, indent = 4)
    name = x["dataset"] + ".json"
    with open(name, "w") as outfile:
        outfile.write(json_object)