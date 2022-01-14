import arcpy, csv

class featurenode():
    def __init__(self):
        self.nodename = None
        self.nodebranches = []
        self.defquery = None
        self.recordcount = 0
    
    def getnode(self,layer):
        temp = layer.longName.split('\\')
        self.nodename = temp[-1]
        self.nodebranches = temp[::-1][:-1]
        self.defquery = layer.definitionQuery
        self.recordcount = arcpy.management.GetCount(layer)

def writeheader(writer):
    writer.writerow(['LayerName', 'RecordCount', 'DefinitionQuery', 'NodePath'])

def main():
    project = arcpy.GetParameterAsText(0)
    output = arcpy.GetParameterAsText(1)
    layers = arcpy.mp.ArcGISProject(project).listMaps()[0].listLayers()
    with open(output, 'w', newline='') as csvfile:
        writeheader(csv.writer(csvfile))
    
    for layer in layers:
        if layer.isFeatureLayer:
            node = featurenode()
            node.getnode(layer)
            with open(output, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([node.nodename, node.recordcount, node.defquery, '\\'.join(node.nodebranches)])

main()

