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
        self.nodebranches = temp[::-1][1:]
        if layer.supports("DEFINITIONQUERY"):
            self.defquery = layer.definitionQuery
            self.recordcount = arcpy.management.GetCount(layer)
    
    def getemptynode(self,layer):
        temp = layer.longName.split('\\')
        self.nodebranches = temp[::-1]

def writeheader(writer):
    writer.writerow(['LayerName', 'RecordCount', 'DefinitionQuery', 'NodePath'])

def writecsv(writer,node):
    writer.writerow([node.nodename, node.recordcount, node.defquery, '\\'.join(node.nodebranches)])

def main():
    # get project file path as input parameter
    project = arcpy.GetParameterAsText(0)
    # get output csv file path as input parameter
    output = arcpy.GetParameterAsText(1)
    # get feature layers from project
    layers = arcpy.mp.ArcGISProject(project).listMaps()[0].listLayers()
    # write csv header
    with open(output, 'w', newline='') as csvfile:
        writeheader(csv.writer(csvfile))
    
    # loop through feature layers
    for layer in layers:
        # skip annotation class 1 feature layer
        if layer.name == 'Class 1':
            continue
        # print out layer name on console
        arcpy.AddMessage(layer.longName)
        # check if layer is feature layer
        if layer.isFeatureLayer:
            # create feature node object
            node = featurenode()
            # get feature node from layer
            node.getnode(layer)
            # write feature node to csv file
            with open(output, 'a', newline='') as csvfile:
                writecsv(csv.writer(csvfile),node)
        # check if layer is group layer without sublayers
        elif not(len(layer.listLayers()) > 0):
                # create feature node object
                node = featurenode()
                # get feature node from layer
                node.getemptynode(layer)
                # write feature node to csv file
                with open(output, 'a', newline='') as csvfile:
                    writecsv(csv.writer(csvfile),node)

main()

