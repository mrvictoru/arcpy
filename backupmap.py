import arcpy, sys, os

# set script parameter
p = arcpy.mp.ArcGISProject('current') # set project to current project
m = p.activeMap # get current map name
domain_networks = ["*"] #select all
export_data = "INCLUDE_DATA" #to load data from all working from all feature classes
output_name = arcpy.GetParameter(2)

# indicate Current Project and Map
pmsg = "Current Project: " + str(p.filePath) + " Current Map: " + str(m_name)
arcpy.AddMessage(pmsg)

# get UN for creating asset package
utility_network = arcpy.GetParameter(0)
pmsg = "Utility Network: " + str(utility_network)
arcpy.AddMessage(pmsg)

# get Destination path
output_path = arcpy.GetParameter(1)
pmsg = "Output: " + str(output_path)
arcpy.AddMessage(pmsg)

#export assetpackage
arcpy.AddMessage("Starting to create asset package...")

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

# update connection properties
pmsg = "Updating connection properties in " + str(m.name) + "..."
arcpy.AddMesage(pmsg)

new = os.path.join(str(output_path),str(output_name) + ".gdb")
l = m.listLayers()

# loop through the layers in the map
for layer in l:
    try:
        arcpy.AddMessage(layer.name)
        pmsg = str(layer.connectionProperties) + "updating"
        new_conn = layer.connectionProperties
        new_conn['connection_info'] = new
        arcpy.AddMessage(pmsg)
        layer.updateConnectionProperties(layer.connectionProperties, new_conn)
        pmsg = str(layer.connectionProperties + "updated")
        arcpy.AddMessage(pmsg)
    except:
        pmsg = str(layer.name) + "Layer Conn Prop Null"
        arcpy.AddMessage(pmsg)


# create new backup project at output path
pmsg = "Creating new backup project at: " + str(output_path)
arcpy.AddMessage(pmsg)
output_project = os.path.join(str(output_path), output_name + ".aprx")
p.saveACopy(str(output_project)) # save project at output path