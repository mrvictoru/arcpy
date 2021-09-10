import arcpy, json, os

def updateconnprop(target_path, mapping_path):
    #check workspace:
    if "gdb" in target_path:
        workspace_factory = "File Geodatabase"

    # get dataset mapping json list
    jsonlist = []
    jlist = os.listdir(mapping_path)
    for jfile in jlist:
        jpath = os.path.join(mapping_path,jfile)
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
            new_conn["workspace_factory"] = workspace_factory
            pmsg = str(layer.connectionProperties) + " updating"
            arcpy.AddMessage(pmsg)
            pmsg = "to " + str(new_conn) + " new connection"
            arcpy.AddMessage(pmsg)
            layer.updateConnectionProperties(layer.connectionProperties, new_conn)
            pmsg = str(layer.connectionProperties + "updated")
            arcpy.AddMessage(pmsg)
        except:
            pmsg = str(layer.name) + "Layer Conn Prop Null"
            arcpy.AddMessage(pmsg)

# get script parameter
p = arcpy.mp.ArcGISProject('current')
m = p.activeMap
l = m.listLayers()
target = arcpy.GetParameterAsText(0)
mapping = arcpy.GetParameterAsText(1)

updateconnprop(target_path=target, mapping_path=mapping)


