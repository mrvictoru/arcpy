import arcpy

# get script parameter
p = arcpy.mp.ArcGISProject('current')
m = p.activeMap
l = m.listLayers()
newconnprop = arcpy.GetParameterasText(0)

# indicates current map name
pmsg = "Current map:" + m.name
arcpy.AddMessage(pmsg)

# loop through the layers in the map
for layer in l:
    arcpy.AddMessage(layer.name)
    try:
        print(layer.connectionProperties)
        layer.updateConnectionProperties(layer.connectionProperties, newconnprop)
    except:
        print



