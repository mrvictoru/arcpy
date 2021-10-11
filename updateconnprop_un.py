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

# this function can only be used if the target path is a file geodatabase
def updateconnprop(target_path, mapping_path, l, codenamemap):
    #check workspace:
    if "gdb" in target_path:
        workspace_factory = "File Geodatabase"
        conn_base = "database"
        arcpy.AddMessage("Target Path is a gdb")
    elif "http" in target_path:
        workspace_factory = "FeatureService"
        conn_base = "url"
        arcpy.AddMessage("Target Path is an url")
    elif "sde" in target_path:
        arcpy.AddError("Does not support SDE")
        sys.exit(0)
    else:
        arcpy.AddError("Target Path invalid")
        sys.exit(0)

    # get dataset mapping json list
    jsonlist = []
    jlist = os.listdir(mapping_path)
    for jfile in jlist:
        jpath = os.path.join(mapping_path,jfile)
        with open(jpath) as f:
            data = json.load(f)
            jsonlist.append(data)

    # loop through the layers in the map
    for layer in l:
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


# get script parameter
p = arcpy.mp.ArcGISProject('current') # set project to current project
m = p.activeMap # get current map
layers = m.listLayers() # get layers in map
target = arcpy.GetParameterAsText(0) # get database target path (gdb or url)
mapping = arcpy.GetParameterAsText(1) # get mapping file path
un = arcpy.GetParameterAsText(2) # get Utility network

# update connection properties
updateconnprop(target_path=target, mapping_path=mapping, l=layers, codenamemap = un_assetgroup_code_name(utility_network=un))


