import arcpy
import os

#DB paths and setup
exportFromDB = arcpy.GetParameterAsText(0) #Get the path to the database to export attribute rule from
toDB = arcpy.GetParameterAsText(1) #Get the path to the database to import attribute rule to
saveFilesToPath = arcpy.GetParameterAsText(2) #Get the path to save the files to

#Export attribute rules from the database
arcpy.env.workspace = exportFromDB
featureclasses = arcpy.ListFeatureClasses()

#loop through each feature class
for fc in featureclasses:
    #check if the feature class has attribute rules
    if(arcpy.Describe(fc).attributeRules):
        pmsg = "Exporting attribute rules for " + str(fc)
        arcpy.AddMessage(pmsg)
        outputPath = os.path.join(saveFilesToPath, fc + "_AttributeRules.csv")
        arcpy.ExportAttributeRules_management(fc, outputPath)

#Import attribute rules to new database
arcpy.env.workspace = toDB
attributerules = os.listdir(saveFilesToPath)

#loop through each attribute rule
for file in attributerules:
    #check if the file end with csv
    if(file.endswith(".csv")):
        fc = file.split("_")[0] #get the feature class name from the file name
        pmsg = "Importing attribute rules for " + str(fc)
        arcpy.AddMessage(pmsg)
        inputPath = os.path.join(saveFilesToPath, file)
        arcpy.ImportAttributeRules_management(fc, inputPath)