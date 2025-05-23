# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# generate_rasters.py
# Created on: 2020-07-29 11:53:56.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: generate_rasters <platform_location> <elev_terrain> <Output_raster>
# Description:
# Generates a Euclidean Distance raster. Why? To derive DISTANCE from an antenna (origin), euclidean distance will provide that.
#
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, os
from arcpy import env
from arcpy.sa import *

def LULC_Reclass(input_raster, output_lulc):  # Reclassify LULC for RF Impedence

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("spatial")

    #with arcpy.EnvManager(extent='451020.2144 3404181.0008 531702.6596 3501557.6516 PROJCS["WGS_1984_UTM_Zone_15N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-93.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'):
    out_raster = arcpy.sa.Reclassify(
        in_raster=input_raster,
        reclass_field="Value",
        remap="0 NODATA;1 NODATA;2 NODATA;3 NODATA;4 NODATA;5 NODATA;6 NODATA;7 NODATA;8 NODATA;9 NODATA;10 1;11 1;12 1;13 NODATA;14 NODATA;15 NODATA;16 NODATA;17 NODATA;18 NODATA;19 NODATA;20 NODATA;21 5;22 5;23 10;24 10;25 NODATA;26 NODATA;27 NODATA;28 NODATA;29 NODATA;30 NODATA;31 1;32 NODATA;33 NODATA;34 NODATA;35 NODATA;36 NODATA;37 NODATA;38 NODATA;39 NODATA;40 NODATA;41 10;42 10;43 10;44 NODATA;45 NODATA;46 NODATA;47 NODATA;48 NODATA;49 NODATA;50 NODATA;51 1;52 1;53 NODATA;54 NODATA;55 NODATA;56 NODATA;57 NODATA;58 NODATA;59 NODATA;60 NODATA;61 NODATA;62 NODATA;63 NODATA;64 NODATA;65 NODATA;66 NODATA;67 NODATA;68 NODATA;69 NODATA;70 NODATA;71 1;72 1;73 1;74 NODATA;75 NODATA;76 NODATA;77 NODATA;78 NODATA;79 NODATA;80 NODATA;81 1;82 1;83 NODATA;84 NODATA;85 NODATA;86 NODATA;87 NODATA;88 NODATA;89 NODATA;90 10;91 NODATA;92 NODATA;93 NODATA;94 NODATA;95 5;96 NODATA;97 NODATA;98 NODATA;99 NODATA;100 NODATA;101 NODATA;102 NODATA;103 NODATA;104 NODATA;105 NODATA;106 NODATA;107 NODATA;108 NODATA;109 NODATA;110 NODATA;111 NODATA;112 NODATA;113 NODATA;114 NODATA;115 NODATA;116 NODATA;117 NODATA;118 NODATA;119 NODATA;120 NODATA;121 NODATA;122 NODATA;123 NODATA;124 NODATA;125 NODATA;126 NODATA;127 NODATA;128 NODATA;129 NODATA;130 NODATA;131 NODATA;132 NODATA;133 NODATA;134 NODATA;135 NODATA;136 NODATA;137 NODATA;138 NODATA;139 NODATA;140 NODATA;141 NODATA;142 NODATA;143 NODATA;144 NODATA;145 NODATA;146 NODATA;147 NODATA;148 NODATA;149 NODATA;150 NODATA;151 NODATA;152 NODATA;153 NODATA;154 NODATA;155 NODATA;156 NODATA;157 NODATA;158 NODATA;159 NODATA;160 NODATA;161 NODATA;162 NODATA;163 NODATA;164 NODATA;165 NODATA;166 NODATA;167 NODATA;168 NODATA;169 NODATA;170 NODATA;171 NODATA;172 NODATA;173 NODATA;174 NODATA;175 NODATA;176 NODATA;177 NODATA;178 NODATA;179 NODATA;180 NODATA;181 NODATA;182 NODATA;183 NODATA;184 NODATA;185 NODATA;186 NODATA;187 NODATA;188 NODATA;189 NODATA;190 NODATA;191 NODATA;192 NODATA;193 NODATA;194 NODATA;195 NODATA;196 NODATA;197 NODATA;198 NODATA;199 NODATA;200 NODATA;201 NODATA;202 NODATA;203 NODATA;204 NODATA;205 NODATA;206 NODATA;207 NODATA;208 NODATA;209 NODATA;210 NODATA;211 NODATA;212 NODATA;213 NODATA;214 NODATA;215 NODATA;216 NODATA;217 NODATA;218 NODATA;219 NODATA;220 NODATA;221 NODATA;222 NODATA;223 NODATA;224 NODATA;225 NODATA;226 NODATA;227 NODATA;228 NODATA;229 NODATA;230 NODATA;231 NODATA;232 NODATA;233 NODATA;234 NODATA;235 NODATA;236 NODATA;237 NODATA;238 NODATA;239 NODATA;240 NODATA;241 NODATA;242 NODATA;243 NODATA;244 NODATA;245 NODATA;246 NODATA;247 NODATA;248 NODATA;249 NODATA;250 NODATA;251 NODATA;252 NODATA;253 NODATA;254 NODATA;255 NODATA",
        missing_values="DATA"
    )
    if arcpy.Exists(output_lulc):
        arcpy.management.Delete(output_lulc)
    out_raster.save(output_lulc)
    
    return output_lulc

def sendMessage(message, indent=0):

    if indent == 0:
        string = message
    if indent > 0 :
        string = "{} {}".format(R" " * indent,message)

    arcpy.AddMessage(string)
    
# ##################################################################
# START
# ##################################################################
# Script arguments

platform_location = arcpy.GetParameter(0)
if platform_location == '#' or not platform_location:
    platform_location = R"C:\arcgispro_projects\TFGP_RF_propagation\TFGP_RF_propagation.gdb\antenna_location" # provide a default value if unspecified
sendMessage(f"Set the location of the antenna (mounted on a platform) to {platform_location}")

elev_terrain = arcpy.GetParameter(1)
if elev_terrain == '#' or not elev_terrain:
    elev_terrain = 'C:\\arcgispro_projects\\TFGP_RF_propagation\\TFGP_RF_propagation.gdb\\DTED'
sendMessage(f"Set the elevation raster to {elev_terrain}")

# C:\Users\chrism\OneDrive - Esri\ArcGIS_Pro_Projects\scratch\scratch.gdb
if arcpy.GetParameter(2):
    arcpy.env.workspace = arcpy.GetParameter(2)
else: 
    arcpy.env.workspace = R"C:\arcgispro_projects\scratch\scratch.gdb"
sendMessage(f"Workspace: {arcpy.env.workspace}")

broadcast_frequency = arcpy.GetParameterAsText(3)
if broadcast_frequency == '#' or not broadcast_frequency:
    broadcast_frequency = 147.23

tx_gain = arcpy.GetParameterAsText(4)
if tx_gain == '#' or not tx_gain:
    tx_gain = 0

# land_cover_raster = arcpy.GetParameterAsText(5)
# if not land_cover_raster:
#     arcpy.management.MakeRasterLayer(R"\\clt-str-syn-p01\Charlotte Defense Services\data\NLCD\nlcd_2019_land_cover_l48_20210604\nlcd_2019_land_cover_l48_20210604.img","tmp_nlcd")  # R"C:\Users\chrism\OneDrive - Esri\ArcGIS_Pro_Projects\scratch\nlcd_2019.lyrx"
#     land_cover_raster = "tmp_nlcd"
# sendMessage(f"Land Cover Raster: {land_cover_raster}")
    
Output_viewshed = arcpy.GetParameterAsText(5)
Output_distance = arcpy.GetParameterAsText(6)
Output_fspl = arcpy.GetParameterAsText(7)

arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"

# fetch map extent (use display for now)
aprx = arcpy.mp.ArcGISProject(R"C:\arcgispro_projects\TFGP_RF_propagation\TFGP_RF_propagation.aprx")
# mv = aprx.activeView
# arcpy.env.extent =  mv.camera.getExtent()

# Process 1 : Viewshed
# Viewshed2(in_raster, in_observer_features, {out_agl_raster}, {analysis_type}, {vertical_error}, {out_observer_region_relationship_table}, {refractivity_coefficient}, {surface_offset}, {observer_elevation}, {observer_offset}, {inner_radius}, {inner_radius_is_3d}, {outer_radius}, {outer_radius_is_3d}, {horizontal_start_angle}, {horizontal_end_angle}, {vertical_upper_angle}, {vertical_lower_angle}, {analysis_method}, {analysis_target_device})
sendMessage(f"Processing data to create VIEWSHED...")
# set local variables
inRaster = elev_terrain
inObservers = platform_location
outAGL = ""
analysisType = "OBSERVERS"
verticalError = ""
outAnalysisRelationTable = "#"
refractCoeff = ""
surfaceOffset = "#"
observerElevation = "#"
observerOffset = "offseta"
innerRadius = 0
innerIs3D = "GROUND"
outerRadius = "#"
outerIs3D = "#"
horizStartAngle = "azimuth1"
horizEndAngle = "azimuth2"
vertUpperAngle = "vert1"
vertLowerAngle = "vert2"
analysisMethod = "ALL_SIGHTLINES"
# Execute Viewshed2

out_raster = arcpy.sa.Viewshed(
    in_raster=inRaster,
    in_observer_features=platform_location,
    z_factor=1,
    curvature_correction="FLAT_EARTH",
    refractivity_coefficient=0.13,
    out_agl_raster=None)

#out_raster.save(r"C:\Temp\rf_modeling\flick.gdb\viewshed_00002")

#outViewshed2 = Viewshed2(inRaster, inObservers)
                        # , outAGL, analysisType,
                        #  verticalError, outAnalysisRelationTable, refractCoeff,
                        #  surfaceOffset, observerElevation, observerOffset,
                        #  innerRadius, innerIs3D)
# Save the output
out_raster.save(Output_viewshed)
# if arcpy.Exists(Output_viewshed):
#     arcpy.management.Delete(Output_viewshed)
#arcpy.management.Rename(outViewshed2.name,Output_viewshed)
sendMessage(f"Viewshed {Output_viewshed} created.")


# Process 2: Distance Accumulation 

# DistanceAccumulation(in_source_data, {in_barrier_data}, {in_surface_raster}, {in_cost_raster}, {in_vertical_raster}, 
#                     {vertical_factor}, {in_horizontal_raster}, {horizontal_factor}, {out_back_direction_raster}, {out_source_direction_raster}, {out_source_location_raster}, {source_initial_accumulation}, {source_maximum_accumulation}, {source_cost_multiplier}, {source_direction}, {distance_method})
sendMessage(f"Running Distance Accumulation...")
in_source_data=platform_location
in_barrier_data="#"
in_surface_raster=inRaster
in_cost_raster="#"
in_vertical_raster="#"
vertical_factor="#"
in_horizontal_raster="#"
horizontal_factor="#"
out_back_direction_raster="#"
out_source_direction_raster="#"
out_source_location_raster="#"
source_initial_accumulation="0"
source_maximum_accumulation="8000"
source_cost_multiplier="1"
source_direction="FROM_SOURCE"
distance_method="#"
                                
out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation(
    in_source_data=platform_location,
    in_barrier_data=None,
    in_surface_raster=inRaster,
    in_cost_raster=None,
    in_vertical_raster=None,
    vertical_factor="BINARY 1 -30 30",
    in_horizontal_raster=None,
    horizontal_factor="BINARY 1 45",
    out_back_direction_raster=None,
    out_source_direction_raster=None,
    out_source_location_raster=None,
    source_initial_accumulation=None,
    source_maximum_accumulation=8000,
    source_cost_multiplier=None,
    source_direction="",
    distance_method="GEODESIC"
)
out_distance_accumulation_raster.save(Output_distance)

# out_ed = DistanceAccumulation(in_source_data, in_barrier_data, in_surface_raster, in_cost_raster, 
#                                 in_vertical_raster,  vertical_factor, in_horizontal_raster, horizontal_factor, 
#                                 out_back_direction_raster, out_source_direction_raster, out_source_location_raster, 
#                                 source_initial_accumulation, source_maximum_accumulation, source_cost_multiplier, 
#                                 source_direction, distance_method)
# #out_ed.save("output_distance")
# if arcpy.Exists(Output_distance):
#     arcpy.management.Delete(Output_distance)
# arcpy.management.Rename(out_ed.name,Output_distance)
sendMessage(f"Distance Accumulation {out_distance_accumulation_raster.name} complete.")

# Process 3: Free Space Path Loss (FSPL) using Raster Calculator
'''
    Free Space Path Loss (FSPL) calculations
    FSPL = 20 log10((4 * π * d * f) / c)
    or,
    FSPL = 20 log10(d) + 20 log10(f) + 20 log10 (4π/c) - GTx - GRx
    where:
    c  =  speed of light (in milliions of meters)
    f  = 	radiating frequency (MHz)
    d  = 	distance from antenna (meters)
    Gt =	transmit antenna gain (dB)
    Gr =	receive antenna gain (dB)

    more info: https://www.pasternack.com/t-calculator-fspl.aspx?gclid=Cj0KCQjw6uT4BRD5ARIsADwJQ1-fxetOMbeKDocslEB6Kv7_Gx6GFthonjlyWQOUnZ6lqZPbq43SxskaAucKEALw_wcB
'''
arcpy.gp.RasterCalculator_sa("20*Log10(\"" + Output_distance +"\") + 20*Log10(" + broadcast_frequency +") + 20*Log10((4*3.141592654)/300) + " + tx_gain, Output_fspl)


# Process 4: Land Use/Land Cover
''' Remap/Reclassify land use values to "cost" values for RF signal loss as it
intersects the various land uses.
'''
# with arcpy.EnvManager(scratchWorkspace=r"C:\OneDrive - Esri\Documents\ArcGIS\Projects\RF_Propagation\RF_Propagation.gdb", workspace=r"C:\OneDrive - Esri\Documents\ArcGIS\Projects\RF_Propagation\RF_Propagation.gdb"):
##LULC_Reclass(land_cover_raster,os.path.join(arcpy.env.workspace, "output_nlcd_reclass"))
