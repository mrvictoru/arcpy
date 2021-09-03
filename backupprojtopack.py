import arcpy, sys, os

# set script parameter
p = arcpy.mp.ArcGISProject('current') # set project to current project
m= p.activeMap # get current map name
output_name = arcpy.GetParameter(2)

# indicate Current Project and Map
pmsg = "Current Project: " + str(p.filePath) + " Current Map: " + str(m.name)
arcpy.AddMessage(pmsg)

# get Target asset package path
asset_package = arcpy.GetParameter(0)
pmsg = "Target package: " + str(asset_package)
arcpy.AddMessage(pmsg)

# get Destination path
output_path = arcpy.GetParameter(1)
pmsg = "Output: " + str(output_path)
arcpy.AddMessage(pmsg)

# update connection properties
pmsg = "Updating connection properties in " + str(m.name) + "..."
arcpy.AddMessage(pmsg)

# loop through the layers in the map
l = m.listLayers()
for layer in l:
    try:
        arcpy.AddMessage(layer.name)
        pmsg = str(layer.connectionProperties) + "updating"
        arcpy.AddMessage(pmsg)
        layer.updateConnectionProperties(layer.connectionProperties, asset_package)
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