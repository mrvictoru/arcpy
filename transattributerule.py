import arcpy
import os

#DB paths and setup
exportFromDB = arcpy.GetParameterAsText(0)
toDB = arcpy.GetParameterAsText(1)
saveFilesToPath = arcpy.GetParameterAsText(2)
arcpy.env.workspace = exportFromDB
featureclasses = arcpy.ListFeatureClasses()

#Export attribute rules from the database
for fc in featureclasses:
    if(arcpy.Describe(fc).attributeRules):
        print("Exporting attribute rules for " + fc)
        outputPath = saveFilesToPath + fc + "_AttributeRules.csv"
        arcpy.ExportAttributeRules_management(fc, outputPath)

arcpy.env.workspace = toDB
featureclasses = arcpy.ListFeatureClasses()

#Import attribute rules to new database
for fc in featureclasses:
    if(arcpy.Describe(fc).attributeRules):
        print("Importing attribute rules for " + fc)
        inputPath = saveFilesToPath + fc + "_AttributeRules.csv"
        arcpy.ImportAttributeRules_management(fc, inputPath)