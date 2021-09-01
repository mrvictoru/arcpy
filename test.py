import arcpy, os

# get script parameter
p = arcpy.mp.ArcGISProject('current')
m = p.activeMap
utility_network = arcpy.GetParameter(0)
pmsg = "UN: " + str(utility_network)
arcpy.AddMessage(pmsg)

dest_path = arcpy.GetParameter(1)
pmsg = "destination: " + str(dest_path)
arcpy.AddMessage(pmsg)

output_name = arcpy.GetParameter(2)
dest_project = os.path.join(str(dest_path), output_name + ".aprx")
p.saveACopy(str(dest_project))

p = arcpy.mp.ArcGISProject(str(dest_project))
pmsg = "New Project: " + str(p.filePath)
arcpy.AddMessage(pmsg)
