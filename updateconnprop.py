import arcpy, json, os

# get script parameter
p = arcpy.mp.ArcGISProject('current')
m = p.activeMap
l = m.listLayers()
target_path = arcpy.GetParameterAsText(0)
mapping_path = arcpy.GetParameterAsText(1)

# get dataset mapping json list
jsonlist = []
jlist = os.listdir(mapping_path)
for jfile in jlist:
    jpath = os.path.join(jlist,jfile)
    with open(jpath) as f:
        data = json.load(f)
        jsonlist.append(data)

# indicates current map name
pmsg = "Current map:" + m.name + "\n"
arcpy.AddMessage(pmsg)

# loop through the layers in the map
for layer in l:
    try:
        arcpy.AddMessage(layer.name)
        new_conn = layer.connectionProperties
        new_conn['connection_info'] = target_path
        for jmapping in jsonlist:
            if layer.name in jmapping["feature"]:
                new_conn["dataset"] = jmapping["dataset"]
                break
        pmsg = str(layer.connectionProperties) + "updating"
        arcpy.AddMessage(pmsg)
        layer.updateConnectionProperties(layer.connectionProperties, new_conn)
        pmsg = str(layer.connectionProperties + "updated")
        arcpy.AddMessage(pmsg)
    except:
        pmsg = str(layer.name) + "Layer Conn Prop Null"
        arcpy.AddMessage(pmsg)



