#
import os
import arcpy
# 

def get_process_image(source_elevation):

    url_parts = str(source_elevation).rstrip('/').split('/')
    output_raster = url_parts[-2] if len(url_parts) >= 2 else None
    
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    map_view = aprx.activeView
    if isinstance(map_view, arcpy._mp.MapView):
        
        # Get the current extent of the map view
        extent = map_view.camera.getExtent()

        # Extract the coordinates from the extent
        xmin, ymin = extent.XMin, extent.YMin
        xmax, ymax = extent.XMax, extent.YMax

        # Define the four coordinates (in clockwise order)
        coordinates = [
            (xmin, ymin),
            (xmax, ymin),
            (xmax, ymax),
            (xmin, ymax)
        ]

        # Create an in-memory feature class
        in_memory_fc = "in_memory/tmp_extent"
        arcpy.management.CreateFeatureclass("in_memory", "tmp_extent", "POLYGON", spatial_reference=map_view.map.spatialReference)

        # Create an array object to hold the points
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        current_extent = map_view.camera.getExtent()
        aoi = f'"{current_extent.XMin} {current_extent.YMin} {current_extent.XMax} {current_extent.YMax}"'

        # Perform the clip operation
        arcpy.AddMessage(f'arcpy.management.Clip({source_elevation}, "#", {output_raster}, {aoi}, "#", "ClippingGeometry", "MAINTAIN_EXTENT")')
        arcpy.management.Clip(source_elevation, output_raster, aoi, "#", "ClippingGeometry", "MAINTAIN_EXTENT")
        return output_raster
    

arcpy.env.overwriteOutput = True


input_points = R"C:\Users\chrism\OneDrive - Esri\ArcGIS_Pro_Projects\Pt2Pt_Links\Pt2Pt_Links.gdb\candidate_ssites"
elevation = R"https://tsmoage.esri.com/hosted/rest/services/DEMS/ImageServer"
ws = R"C:\Users\chrism\OneDrive - Esri\ArcGIS_Pro_Projects\Pt2Pt_Links\Pt2Pt_Links.gdb"

if arcpy.GetParameter(0):

    input_points = arcpy.GetParameter(0)
    
if arcpy.GetParameter(1):
    elevation  = arcpy.GetParameter(1)
    arcpy.AddMessage(f"elevation: {elevation}, type: {type(elevation)}")
    
elevation  = get_process_image(elevation) # clip the image to the current extent

if arcpy.GetParameter(3):
    ws = arcpy.GetParameter(3)

arcpy.env.workspace = ws
arcpy.AddMessage(f"Scratch: {arcpy.env.scratchGDB}")
linesofsight = os.path.join(arcpy.env.scratchGDB, "LineOfSight") 
sightlines = os.path.join(arcpy.env.scratchGDB, "SightLines") 

observers = os.path.join(arcpy.env.scratchGDB, "Observers") 
targets = os.path.join(arcpy.env.scratchGDB, "Targets")

for l in linesofsight, sightlines, observers, targets:
    arcpy.AddMessage(f"{l}")

#arcpy.AddMessage(f'arcpy.defense.LinearLineOfSight({input_points}, {input_points}, {elevation}, {linesofsight}, {sightlines}, {observers}, {targets}, None, 10, 10, "ADD_PROFILE_GRAPH")')
# arcpy.defense.LinearLineOfSight(in_observer_features, in_target_features, in_surface, out_los_feature_class, out_sight_line_feature_class, out_observer_feature_class, out_target_feature_class, {in_obstruction_features}, {observer_height_above_surface}, {target_height_above_surface}, {add_profile_attachment})
arcpy.defense.LinearLineOfSight(input_points, input_points, elevation, linesofsight, sightlines, observers, targets, None, 10, 10, "ADD_PROFILE_GRAPH")

# arcpy.ddd.LineOfSight(
#     in_surface=elevation,
#     in_line_feature_class=input_lines,
#     out_los_feature_class=os.path.join(arcpy.env.workspace,"out_los_feature_class"),
#     out_obstruction_feature_class=None,
#     use_curvature="NO_CURVATURE",
#     use_refraction="NO_REFRACTION",
#     refraction_factor=0.13,
#     pyramid_level_resolution=0,
#     in_features=None
# )