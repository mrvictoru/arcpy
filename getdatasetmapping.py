import arcpy, json, os

p = arcpy.mp.ArcGISProject('current')
m = p.activeMap
l = m.listLayers()
output_path = arcpy.GetParameterAsText(0) # get Destination path

xlist = []

for layer in l:
    layerlist = layer.listLayers
    if len(layerlist) > 1:
        setdict = {
            "dataset": layer.name,
            "feature": []
        }
        
        for sublayer in layerlist:
            setdict["feature"].append(sublayer.name)
        xlist.append(setdict)
        

for x in xlist:
    json_object = json.dumps(x, indent = 4)
    name = x["dataset"] + ".json"
    with open(os.path.join(output_path,name), "w") as outfile:
        outfile.write(json_object)