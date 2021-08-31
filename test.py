import arcpy

# get script parameter
p = arcpy.mp.ArcGISProject('current')
m = p.activeMap
l = m.listLayers()
newconnprop = arcpy.GetParameterasText(0)

# indicates current map name
pmsg = "Current map: " + m.name
arcpy.AddMessage(pmsg)

pmsg = "input: " + newconnprop
arcpy.AddMessage(pmsg)