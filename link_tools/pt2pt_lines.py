#-------------------------------------------------------------------------------
# Name:        pt2pt_lines.py
# Purpose:     Takes points from an input point feature class/layer and creates a
#              line between every point and every other point. 
#
# Parameters:
#   Input (Endpoints) Layer - A point layer that has "event_id" field.
#   Workspace for output - any
#   Output FC Name - any
#   Event ID - an Integer that matches the event_id value(s) in the Input (Endpoints) Layer
#   Spatial Reference - any
#   
# Author:      chrism
# Created:     02/23/2023
# Copyright:   (c) Esri 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, os, sys

arcpy.env.overwriteOutput = True

if os.path.basename(sys.executable) in ['ArcGISPro.exe', 'ArcSOC.exe']:
    aprx = arcpy.mp.ArcGISProject(R"CURRENT")
    map = aprx.activeMap  # aprx.listMaps()[0]  # 
    arcpy.AddMessage("Map: %s" % (map.name))
    lyr_points = arcpy.GetParameter(0)  #
    desc = arcpy.Describe(lyr_points)
    ws = desc.path  # arcpy.env.workspace  # Workspace for output
    output_fc = arcpy.GetParameter(1)  # Result link lines written here
    sr = arcpy.Describe(output_fc).spatialReference  # Spatial Reference
    
else:   # for debugging in IDE
    aprx = arcpy.mp.ArcGISProject(R"C:\Users\chrism\OneDrive - Esri\ArcGIS_Pro_Projects\MyRFScanning\MyRFScanning.aprx")
    map = aprx.listMaps()[0]
    lyr_points = R"C:\Users\chrism\OneDrive - Esri\ArcGIS_Pro_Projects\MyRFScanning\MyRFScanning.gdb\antenna_points"
    ws = R"C:\Users\chrism\OneDrive - Esri\ArcGIS_Pro_Projects\MyRFScanning\MyRFScanning.gdb"
    output_fc = os.path.join(ws, "my_links")
    sr = arcpy.Describe(output_fc).spatialReference

for field in arcpy.ListFields(lyr_points):
    print(field.name)

arcpy.management.CreateTable(arcpy.env.scratchGDB,"endpoints")
tbl_endpoints = os.path.join(arcpy.env.scratchGDB,"endpoints")

arcpy.AddMessage("Created %s" % (tbl_endpoints))
arcpy.management.AddField(tbl_endpoints, "begin_oid", "LONG", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')
arcpy.management.AddField(tbl_endpoints, "begin_x", "DOUBLE", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')
arcpy.management.AddField(tbl_endpoints, "begin_y", "DOUBLE", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

arcpy.management.AddField(tbl_endpoints, "end_oid", "LONG", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')
arcpy.management.AddField(tbl_endpoints, "end_x", "DOUBLE", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')
arcpy.management.AddField(tbl_endpoints, "end_y", "DOUBLE", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

fields = ['objectid','shape@X','shape@Y']
expression = f'OBJECTID > 0'
count = 0

arcpy.AddMessage("Processing %s" % (lyr_points))
listfields = [fld.name for fld in arcpy.ListFields(lyr_points)]
arcpy.AddMessage("Fields: %s" % (listfields))
try:
    my_points = [row for row in arcpy.da.SearchCursor(lyr_points,fields,expression)]
except RuntimeError as e:
    arcpy.AddError(f"Error: {e}")
    sys.exit(1)
    arcpy.AddMessage("Error: %s" % (e))
cfields = ["begin_oid","begin_x", "begin_y","end_oid","end_x", "end_y"]

with arcpy.da.InsertCursor(tbl_endpoints, cfields) as icursor:
    
    pt_pairs = []

    # this little block of code, with double for-loop was written so that only
    # one line is written between two points. Without the "if" logic, two lines
    # will be created between the two points (one using one point as origin and
    # another using the other point as an origin), The code prevents that. 
    for pt1 in my_points:
        for pt2 in my_points:
            #arcpy.AddMessage("comparing pt1 %i with pt2 %i" % (pt1[0],pt2[0]))
            if not pt1[0] == pt2[0] and f'{pt1[0]}-{pt2[0]}' not in pt_pairs:
                #print(f"{pt1[0]} -> {pt2[0]}")
                icursor.insertRow((pt1[0],pt1[1],pt1[2],pt2[0],pt2[1],pt2[2]))
                pt_pairs.append(f"{pt2[0]}-{pt1[0]}")
                count += 1
            
print(f"Point Count: {len(my_points)}")
print(f"Pair Count: {count}")

# replace the output so delete it first
if arcpy.Exists(os.path.join(ws,"tmp_output_links")):
    arcpy.management.Delete(os.path.join(ws,"tmp_output_links"))

# convert the table of coordinate end points to a line feature class
# Consider using the "Construct Sight Lines" tool if the observer location is defined by point features and the visibility target is represented by data stored in a different feature class.
arcpy.management.XYToLine(tbl_endpoints, os.path.join(ws,"tmp_output_links"), "begin_x", "begin_y", "end_x", "end_y", "GEODESIC", "end_oid", sr, "NO_ATTRIBUTES")

arcpy.Append_management(os.path.join(ws,"tmp_output_links"), output_fc, "NO_TEST")

#
# the rest of this code is for using the tool in ArcGIS Pro to create and add the result as a layer in the project.
# outlayer = "links"  # % (event_id)
# tmp_layer = os.path.join(arcpy.env.scratchFolder, outlayer)

# result  = arcpy.management.MakeFeatureLayer(os.path.join(ws,output_fc), "tmp_layer")
# arcpy.AddMessage(result)
# new_layer = result.getOutput(0)
# new_layer.name = outlayer
# result = map.addLayer(new_layer)

# arcpy.management.Delete(os.path.join(ws,"tmp_output_links"))