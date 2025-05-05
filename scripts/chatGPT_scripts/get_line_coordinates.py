import arcpy, json, os, sys

# Connect to the ArcGIS Pro project
if os.path.basename(sys.executable) in ['ArcGISPro.exe', 'ArcSOC.exe']:
    aprx = arcpy.mp.ArcGISProject("CURRENT")
else:
    aprx = arcpy.mp.ArcGISProject(R"C:\Users\chrism\OneDrive - Esri\ArcGIS_Pro_Projects\TFGP_mock_up_data_3\TFGP_mock_up_data_3.aprx")

# Get the feature layer
if arcpy.GetParameter(0):
    layer = arcpy.GetParameter(0)
else:
    layer = aprx.listMaps("PROD TFGP")[0].listLayers("links")[0]

# Loop through the selected features
for row in arcpy.da.SearchCursor(layer, ["SHAPE@JSON"]):
    # Parse the JSON representation of the feature's geometry
    feature_json = row[0]
    feature_dict = json.loads(feature_json)
    geometry = feature_dict["paths"][0]

    # Get the beginning and end coordinates of the line
    start_coord = geometry[0]
    end_coord = geometry[-1]

    arcpy.AddMessage("Start coordinate: {}".format(start_coord))
    arcpy.AddMessage("End coordinate: {}".format(end_coord))
