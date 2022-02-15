import arcpy

def init():
    p = arcpy.mp.ArcGISProject('current') # set project to current project
    m = p.activeMap # get current map
    layers = m.listLayers() # get layers in map
    return layers

def updateconnprop(target_path, mapping_path, layers):
    for layer in layers:
        if layer.supports("CONNECTIONPROPERTIES"):
            layer.updateConnectionProperties(target_path, mapping_path)

def main():
    layers = init()
    target = arcpy.GetParameterAsText(0) # get database target path (gdb or url)
    mapping = arcpy.GetParameterAsText(1) # get mapping file path
    updateconnprop(target_path=target, mapping_path=mapping, layers=layers)

main()
        