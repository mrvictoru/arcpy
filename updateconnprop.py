import arcpy

# get script parameter
p = arcpy.mp.ArcGISProject('current')
m = p.activeMap
l = m.listLayers()
newconnprop = arcpy.GetParameterAsText(0)

# indicates current map name
pmsg = "Current map:" + m.name + "\n"
arcpy.AddMessage(pmsg)

# loop through the layers in the map
for layer in l:
    
    try:
        arcpy.AddMessage(layer.name)
        pmsg = str(layer.connectionProperties) + "updating"
        arcpy.AddMessage(pmsg)
        layer.updateConnectionProperties(layer.connectionProperties, newconnprop)
        pmsg = str(layer.connectionProperties + "updated")
        arcpy.AddMessage(pmsg)
    except:
        pmsg = str(layer.name) + "Layer Conn Prop Null"
        arcpy.AddMessage(pmsg)



