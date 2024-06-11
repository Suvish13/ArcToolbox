import os
import re
import arcpy
from arcpy.sa import *

class LicenseError(Exception):
    pass

# Allow ArcPy to overwrite outputs
arcpy.env.overwriteOutput = True

# Get the Input Parameters
SR_SWIR1_BandPath = arcpy.GetParameterAsText(0)
SR_SWIR2_BandPath = arcpy.GetParameterAsText(1)
SR_NIR_BandPath = arcpy.GetParameterAsText(2)
outRasPath = arcpy.GetParameterAsText(3)

try:
    # Define Output Format Based On Output Workspace
    output_format = ""
    if re.search(r'.mdb', outRasPath):
        arcpy.AddMessage("Output Format: PersonalGeodatabase Raster")
        output_format = "GRID"
    elif re.search(r'.gdb', outRasPath):
        arcpy.AddMessage("Output Format: FileGeodatabase Raster")
        output_format = "GRID"
    elif re.search(r'.sde', outRasPath):
        arcpy.AddMessage("Output Format: SDE Raster")
        output_format = "GRID"
    else:
        arcpy.AddMessage("Output Format: GeoTIFF file")
        output_format = "TIF"

    # Check for ArcGIS Spatial Analyst extension
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        arcpy.AddMessage("Checked out \"Spatial\" Extension")
    else:
        raise LicenseError

    arcpy.AddMessage("Loading Input Raster(s): {0}, {1}, {2}".format(SR_SWIR1_BandPath, SR_SWIR2_BandPath, SR_NIR_BandPath))
    SR_SWIR1_Ras = Raster(SR_SWIR1_BandPath)
    SR_SWIR2_Ras = Raster(SR_SWIR2_BandPath)
    SR_NIR_Ras = Raster(SR_NIR_BandPath)
    
    arcpy.AddMessage("Calculating Soil Salinity")
    outRas_SoilSalinity = (SR_SWIR1_Ras * SR_SWIR2_Ras) / (SR_SWIR1_Ras * SR_NIR_Ras)
    
    if output_format == "TIF":
        outRasPath = outRasPath + ".tif"
    
    arcpy.AddMessage("Saving raster to: {0}".format(outRasPath))
    outRas_SoilSalinity.save(outRasPath)
    
except LicenseError:
    arcpy.AddMessage("ArcGIS Spatial Analyst license is unavailable")
except arcpy.ExecuteError:
    arcpy.AddMessage(arcpy.GetMessages(2))
finally:
    arcpy.AddMessage("Checked in \"Spatial\" Extension")
    arcpy.CheckInExtension("Spatial")
