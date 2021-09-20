# Import required modules
import arcpy, csv, os

utility_network = arcpy.GetParameterAsText(0) # get Utility network
output_path = arcpy.GetParameterAsText(1) # get Destination path
name = "AssetGroup_Code_Name_mapping.csv"
d = arcpy.Describe(utility_network)

field = ["Code", "Name"]
rows = []

# Domain Network properties
domnets = d.domainNetworks
for dom in domnets:

    # Edge Source Properties
    for edgeSource in dom.edgeSources:

        # Asset Group Properties
        for ag in edgeSource.assetGroups:
            row = [ag.assetGroupCode, ag.assetGroupName]
            rows.append(row)

with open(os.path.join(output_path,name), "w") as f:
    csvwriter = csv.writer(f)

    csvwriter.writerow(field)

    csvwriter.writerows(rows)