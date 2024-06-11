class LicenseError(Exception):
    pass
# Set desktop license used to Basic (keyword is arcview)

import os, sys, string, math, re
from posixpath import pardir
import arcpy
from arcpy import arc
from arcpy.sa import *

# Allow ArcPy to overwrite outputs
arcpy.env.overwriteOutput = True

# Get the Input Parameters
SR_NIR_BandPath = arcpy.GetParameterAsText(0)
SR_VR_BandPath = arcpy.GetParameterAsText(1)

# Set the default output path from parameter validation script
outRasPath = arcpy.GetParameterAsText(2)

try:
    # Define Output Format Based On Output Workspace
    output_format = ""
    if re.search( r'.mdb', outRasPath):
        # Final Raster Output - FGDB Raster 
        arcpy.AddMessage ("Output Format: PersonalGeodatabase Raster")
        output_format = "GRID"
    elif re.search( r'.gdb', outRasPath):
        # Final Raster Output - FGDB Raster 
        arcpy.AddMessage ("Output Format: FileGeodatabase Raster")
        output_format = "GRID"  
    elif re.search( r'.sde', outRasPath):
        # Final Raster Output - SDE Raster 
        arcpy.AddMessage ("Output Format: SDE Raster")
        output_format = "GRID"
    else:
        # Final Raster Output - Folder therfore GeoTIFF
        arcpy.AddMessage ("Output Format: GeoTIFF file")
        output_format = "TIF"

    # Check for ArcGIS Spatial Analyst extension
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        arcpy.AddMessage ("Checked out \"Spatial\" Extension")
    else:
        # Raise a custom exception
        raise LicenseError
    
    # arcpy.env.workspace = ""
    arcpy.AddMessage("Loading Input Raster(s): {0}, {1}".format(SR_NIR_BandPath, SR_VR_BandPath))
    SR_NIR_Ras = Raster(SR_NIR_BandPath)
    SR_VR_Ras = Raster(SR_VR_BandPath)
    
    arcpy.AddMessage("calculating Normalized Difference Vegetation Index (NDVI)")
    # The algorithm to calculate Normalized Difference Vegetation Index (NDVI)
    # NDVI = (NIR - VR) / (NIR + R)
    outRas_NDVI = (SR_NIR_Ras - SR_VR_Ras) / (SR_NIR_Ras + SR_VR_Ras)
    
    # Determine the output format based on the output workspace
    if output_format == "TIF":
        outRasPath = outRasPath + ".tif"
    
    arcpy.AddMessage("Saving raster to: {0}".format(outRasPath))
    # Save raster to desired output folder or workspace
    outRas_NDVI.save(outRasPath)
    
except LicenseError:
    arcpy.AddMessage("ArcGIS Spatial Analyst license is unavailable")
except arcpy.ExecuteError:
    arcpy.AddMessage(arcpy.GetMessages(2))
finally:
    # Check in the ArcGIS Spatial Analyst extension
    arcpy.AddMessage("Checked in \"Spatial\" Extension")
    arcpy.CheckInExtension("Spatial")