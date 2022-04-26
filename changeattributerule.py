# this python scrip with update attribute rule in batch by exporting attribute rule from csv file
import arcpy
import os
import csv
import re

#define an attribute rule class
class attributerule:
    def __init__(self, fc, rulename, expression):
        self.table = fc
        self.rulename = rulename
        self.expression = expression

#DB paths and setup
exportFromDB = arcpy.GetParameterAsText(0) #Get the path to the database to export attribute rule from
saveFilesToPath = arcpy.GetParameterAsText(1) #Get the path to save the files to

# Script execution code goes here
newtablename = "Colour"
#pattern in attribute rule to match and replacement pattern
pattern1 = "datastore,'\w+',"
pattern2 = "datastore,'{[\w-]+}','"
newpattern = "datastore,'{}',".format(newtablename)

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
    else:
        break
    
    #read csv file and create attributerule object
    with open(outputPath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        attributerules = []
        for row in reader:
            attributerules.append(attributerule(fc, row[0], row[9]))
    
    for rule in attributerules:
        if re.search(pattern1, rule.expression):
            #replace the pattern in the expression
            pmsg = "Updating " + rule.rulename + " in " + rule.table
            arcpy.AddMessage(pmsg)
            rule.expression = re.sub(pattern1, newpattern, rule.expression)
            #alter attribute rule
            arcpy.management.AlterAttributeRule(rule.table, rule.rulename, script_expression = rule.expression)
        elif re.search(pattern2, rule.expression):
            #replace the pattern in the expression
            pmsg = "Updating " + rule.rulename + " in " + rule.table
            arcpy.AddMessage(pmsg)
            rule.expression = re.sub(pattern2, newpattern, rule.expression)
            #alter attribute rule
        arcpy.management.AlterAttributeRule(rule.table, rule.rulename, script_expression = rule.expression)
    






