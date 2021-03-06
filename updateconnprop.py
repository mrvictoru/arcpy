import arcpy, json, os, sys

# this function can only be used if the target path is a file geodatabase
def updateconnprop(target_path, mapping_path, l):
    #check workspace:
    if "gdb" in target_path:
        workspace_factory = "File Geodatabase"
        conn_base = "database"
    elif "http" in target_path:
        workspace_factory = "FeatureService"
        conn_base = "url"
    elif "sde" in target_path:
        arcpy.AddError("Does not support SDE")
        sys.exit(0)
    else:
        arcpy.AddError("Target Path invalid")
        sys.exit(0)

    # get dataset mapping json list
    jsonlist = []
    jlist = os.listdir(mapping_path)
    for jfile in jlist:
        jpath = os.path.join(mapping_path,jfile)
        with open(jpath) as f:
            data = json.load(f)
            jsonlist.append(data)

    # loop through the layers in the map
    for layer in l:
        if layer.supports("CONNECTIONPROPERTIES"):
            new_conn = layer.connectionProperties
            # set new connection info to database
            new_conn['connection_info'] = {}
            new_conn['connection_info'][conn_base] = target_path
            # disregard lower case when check for dataset mapping
            for jmapping in jsonlist:
                if layer.name.lower() in (string.lower() for string in jmapping["feature"]):
                    new_conn["dataset"] = jmapping["dataset"]
                    break
            # set to appropriate workspace factory
            new_conn["workspace_factory"] = workspace_factory
            arcpy.AddMessage(layer.name)
            pmsg = str(layer.connectionProperties) + " updating"

            arcpy.AddMessage(pmsg)
            layer.updateConnectionProperties(layer.connectionProperties, new_conn,True,False,False)
            pmsg = str(layer.connectionProperties) + " updated"
            arcpy.AddMessage(pmsg)

# get script parameter
p = arcpy.mp.ArcGISProject('current') # set project to current project
m = p.activeMap # get current map
layers = m.listLayers() # get layers in map
target = arcpy.GetParameterAsText(0) # get database target path (gdb or url)
mapping = arcpy.GetParameterAsText(1) # get mapping file path

# update connection properties
updateconnprop(target_path=target, mapping_path=mapping, l=layers)


