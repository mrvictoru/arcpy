import arcpy, json, os, sys

# this function check if this feature belong in a particular dataset
def checknameinjmap(jmapping, layer, codemap):
    isdef = False
    if layer.supports("definitionQuery"):
        deftext = layer.definitionQuery
        defquery = deftext.split(' And ')

        # extract assetgroup code from defintion query
        for defintion in defquery:
            if "ASSETGROUP" in defintion:
                isdef = True
                if " = " in defintion:
                    code = defintion.split(" = ")[1]
                else:
                    group = defintion.split(" IN ")[1]
                    group = group.replace('(', '')
                    group = group.replace(')', '')
                    code = group.split(",")[0]

    if isdef:                
        name = codemap.get(code)
    else:
        name = layer.name

    if name.lower() in (string.lower() for string in jmapping["feature"]):
        return True
    else:
        return False

# this function get the assetgroup code and name mapping in a dict. Code being key and Name being value
def un_assetgroup_code_name(utility_network):
    d = arcpy.Describe(utility_network)
    rows = {}
    # Domain Network properties
    domnets = d.domainNetworks
    for dom in domnets:
        # Edge Source Properties
        for edgeSource in dom.edgeSources:
            # Asset Group Properties
            for ag in edgeSource.assetGroups:
                rows.update({ag.assetGroupCode: ag.assetGroupName})
                
    return rows

# return the correct workspace for the target database
def checkworkspace(path):
    if "gdb" in path:
        arcpy.AddMessage("Target Path is a gdb")
        return ("File Geodatabase", "database")
    elif "http" in path:
        arcpy.AddMessage("Target Path is an url")
        return ("FeatureService", "url")
    elif "sde" in path:
        arcpy.AddError("Does not support SDE")
        sys.exit(0)
    else:
        arcpy.AddError("Target Path invalid")
        sys.exit(0)
    
# get network dataset mapping from mapping json file
def jsonlist(path):
    jsonlist = []
    jlist = os.listdir(path)
    for jfile in jlist:
        jpath = os.path.join(path,jfile)
        with open(jpath) as f:
            data = json.load(f)
            jsonlist.append(data)
    return jsonlist

def ifnonnetwork(layer):
    if layer.name

def updateconnprop(target_network_path, target_nonnetwork_path, mappinglist, layers, codemap):
    #check workspace for network:
    (network_workspace_factory, network_conn_base) = checkworkspace(target_network_path)
    (nonnetwork_workspace_factory, nonnetwork_conn_base) = checkworkspace(target_nonnetwork_path)

    # loop through the layers in the map
    for layer in layers:
        pmsg = "Layer name: " + str(layer.name)
        arcpy.AddMessage(pmsg)
        if layer.supports("CONNECTIONPROPERTIES"):
            new_conn = layer.connectionProperties
            if new_conn is not None:
                # set new connection info to database
                new_conn['connection_info'] = {}
                new_conn['connection_info'][conn_base] = target_path
                # check for dataset mapping and set appropriate dataset
                for jmapping in jsonlist:
                    # for UN feature layer
                    if checknameinjmap(jmapping=jmapping, layer=layer, codemap = codenamemap):
                        new_conn["dataset"] = jmapping["dataset"]
                        break
                # set to appropriate workspace factory
                new_conn["workspace_factory"] = workspace_factory
                arcpy.AddMessage(layer.name)
                pmsg = str(layer.connectionProperties) + " updating"

                arcpy.AddMessage(pmsg)
                layer.updateConnectionProperties(layer.connectionProperties, new_conn,True,False,False)
                pmsg = str(layer.connectionProperties) + " updated"
                arcpy.AddMessage(pmsg)
            else:
                pmsg = "Connection for layer is None"
                arcpy.AddMessage(pmsg)





def main():
    # get script parameter
    p = arcpy.mp.ArcGISProject('current') # set project to current project
    m = p.activeMap # get current map
    layers = m.listLayers() # get layers in map
    target_network = arcpy.GetParameterAsText(0) # get database target path (gdb or url)
    target_nonnetwork = arcpy.GetParameterAsText(1) # get database target path (gdb or url)
    mapping = arcpy.GetParameterAsText(2) # get mapping file path
    un = arcpy.GetParameterAsText(3) # get Utility network

    # update connection properties
    updateconnprop(target_network, target_nonnetwork, jsonlist(mapping), layers, un_assetgroup_code_name(un))

main()