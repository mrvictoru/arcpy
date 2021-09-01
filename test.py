import arcpy

# get script parameter
p = arcpy.mp.ArcGISProject('current')
m = p.activeMap
l = m.listLayers()
newconnprop = arcpy.GetParameterAsText(0)

# indicates current map name
pmsg = "Current map: " + m.name
arcpy.AddMessage(pmsg)

pmsg = "input: " + newconnprop
arcpy.AddMessage(pmsg)

# loop through the layers in the map
for layer in l:
    try:
        arcpy.AddMessage(layer.name)
        arcpy.AddMessage(str(layer.connectionProperties))
    except:
        arcpy.AddMessage(layer.name)
        arcpy.AddMessage("null conn")
