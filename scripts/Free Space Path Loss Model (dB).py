# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2021-08-23 13:10:09
"""
import arcpy
from arcpy.sa import *

def freespacepathlossmodel():  # Free Space Path Loss Model (dB)

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("ImageAnalyst")

    polk_ed = arcpy.Raster("C:\\OneDrive - Esri\\Documents\\ArcGIS\\Projects\\RF_Propagation\\scratch.gdb\\polk_ed")

    # Process: Raster Calculator (Raster Calculator) (sa)
    fspl_01 = "C:\\OneDrive - Esri\\Documents\\ArcGIS\\Projects\\RF_Propagation\\scratch.gdb\\fspl_01"
    Raster_Calculator = fspl_01
    with arcpy.EnvManager(extent="443904.049346349 3403278.07911942 544146.298030229 3484387.95796131"):
        fspl_01 = 20*Log10(polk_ed) + 20*Log10(147.23) + 20*Log10((4*3.141592654)/300) 
        fspl_01.save(Raster_Calculator)


if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(extent="-11876025.0770848 3732665.31561857 -11761125.0770848 3884865.31561857", outputCoordinateSystem="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]],VERTCS['WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]]", scratchWorkspace=r"C:\OneDrive - Esri\Documents\ArcGIS\Projects\RF_Propagation\RF_Propagation.gdb", 
                          workspace=r"C:\OneDrive - Esri\Documents\ArcGIS\Projects\RF_Propagation\RF_Propagation.gdb"):
        freespacepathlossmodel()
