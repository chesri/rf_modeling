#
import os
import arcpy
# 
arcpy.env.overwriteOutput = True

if arcpy.GetParameter(0):
    input_lines = arcpy.GetParameter(0)
    input_points = arcpy.GetParameter(0)
    
elevation  = arcpy.GetParameter(1)
ws = arcpy.GetParameter(2)
arcpy.env.workspace = arcpy.GetParameter(2)

arcpy.AddMessage(f"Scratch: {arcpy.env.scratchGDB}")
linesofsight = os.path.join(arcpy.env.scratchGDB, "LineOfSight") 
sightlines = os.path.join(arcpy.env.scratchGDB, "SightLines") 

observers = os.path.join(arcpy.env.scratchGDB, "Observers") 
targets = os.path.join(arcpy.env.scratchGDB, "Targets")

for l in linesofsight, sightlines, observers, targets:
    arcpy.AddMessage(f"{l}")

#arcpy.AddMessage(f'arcpy.defense.LinearLineOfSight({input_points}, {input_points}, {elevation}, {linesofsight}, {sightlines}, {observers}, {targets}, None, 10, 10, "ADD_PROFILE_GRAPH")')
# arcpy.defense.LinearLineOfSight(in_observer_features, in_target_features, in_surface, out_los_feature_class, out_sight_line_feature_class, out_observer_feature_class, out_target_feature_class, {in_obstruction_features}, {observer_height_above_surface}, {target_height_above_surface}, {add_profile_attachment})
#arcpy.defense.LinearLineOfSight(input_points, input_points, elevation, linesofsight, sightlines, observers, targets, None, 10, 10, "ADD_PROFILE_GRAPH")

arcpy.ddd.LineOfSight(
    in_surface=elevation,
    in_line_feature_class=input_lines,
    out_los_feature_class=os.path.join(arcpy.env.workspace,"out_los_feature_class"),
    out_obstruction_feature_class=None,
    use_curvature="NO_CURVATURE",
    use_refraction="NO_REFRACTION",
    refraction_factor=0.13,
    pyramid_level_resolution=0,
    in_features=None
)