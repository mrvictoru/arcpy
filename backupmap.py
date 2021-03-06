import arcpy, sys, os, json

# call export asset package API
def UN2AP(utility_network, domain_networks, output_path, output_name, export_data):
    try:
        arcpy.pt.UtilityNetworkToAssetPackage(utility_network, 
                                            domain_networks, 
                                            output_path, 
                                            output_name, 
                                            export_data)
        arcpy.AddMessage("Export successed")

    except Exception as e:
        pmsg = "Unable to export UN to asset package, error: " + str(e)
        arcpy.AddError(pmsg)
        sys.exit(1)

# this function can only be used if the target path is a file geodatabase
def updateconnpropgdb(target_path, mapping_path, l):
    #check workspace:
    if "gdb" in target_path:
        workspace_factory = "File Geodatabase"
        conn_base = "database"
    else:
        arcpy.AddError("target is not Geodatabase")
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
            new_conn['connection_info']["database"] = target_path
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
            pmsg = str(layer.connectionProperties) + "updated"
            arcpy.AddMessage(pmsg)

# set script parameter
p = arcpy.mp.ArcGISProject('current') # set project to current project
m = p.activeMap # get current map name
layers = m.listLayers() # get layers in map
domain_networks = ["*"] #select all
export_data = "INCLUDE_DATA" #to load data from all working from all feature classes
output_name = arcpy.GetParameter(2) # get output file name
utility_network = arcpy.GetParameter(0) # get UN for creating asset package
output_path = arcpy.GetParameter(1) # get Destination path
dataset_map_path = arcpy.GetParameter(3) # get Dataset mapping json(s) folder path 


#export assetpackage
arcpy.AddMessage("Starting to create asset package...")
UN2AP(utility_network=utility_network, domain_networks=domain_networks, output_path=output_path, output_name=output_name, export_data=export_data)

# update connection properties
arcpy.AddMesage("Updating connection properties")
new = os.path.join(str(output_path),str(output_name) + ".gdb") # set New connection target to newly create asset package
updateconnpropgdb(target_path=new, mapping_path=dataset_map_path, l = layers) 


# create new backup project at output path
pmsg = "Creating new backup project at: " + str(output_path)
arcpy.AddMessage(pmsg)
output_project = os.path.join(str(output_path), output_name + ".aprx")
p.saveACopy(str(output_project)) # save project at output path