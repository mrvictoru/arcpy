import arcpy
import os

#DB paths and setup
exportFromDB = arcpy.GetParameterAsText(0)
toDB = arcpy.GetParameterAsText(1)
saveFilesToPath = arcpy.GetParameterAsText(2)

#Export attribute rules from the database
arcpy.env.workspace = exportFromDB
featureclasses = arcpy.ListFeatureClasses()

for fc in featureclasses:
    if(arcpy.Describe(fc).attributeRules):
        pmsg = "Exporting attribute rules for " + str(fc)
        arcpy.AddMessage(pmsg)
        outputPath = os.path.join(saveFilesToPath, fc + "_AttributeRules.csv")
        arcpy.ExportAttributeRules_management(fc, outputPath)

#Import attribute rules to new database
arcpy.env.workspace = toDB
attributerules = os.listdir(saveFilesToPath)

for file in attributerules:
    if(file.endswith(".csv")):
        fc = file.split("_")[0]
        pmsg = "Importing attribute rules for " + str(fc)
        arcpy.AddMessage(pmsg)
        inputPath = os.path.join(saveFilesToPath, file)
        arcpy.ImportAttributeRules_management(fc, inputPath)