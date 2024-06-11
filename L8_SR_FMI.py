import os
import re
import arcpy
from arcpy.sa import *
from parameter_validation import validate_parameters # type: ignore

class LicenseError(Exception):
    pass

# Allow ArcPy to overwrite outputs
arcpy.env.overwriteOutput = True

# Get the Input Parameters
SWIR_BandPath = arcpy.GetParameterAsText(0)
NIR_BandPath = arcpy.GetParameterAsText(1)
outRasPath = arcpy.GetParameterAsText(2)

try:
    # Validate input parameters
    validate_parameters(SWIR_BandPath, NIR_BandPath, outRasPath)
    
    # Define Output Format Based On Output Workspace
    output_format = ""
    if re.search(r'.mdb', outRasPath):
        # Final Raster Output - PersonalGeodatabase Raster 
        arcpy.AddMessage("Output Format: PersonalGeodatabase Raster")
        output_format = "GRID"
    elif re.search(r'.gdb', outRasPath):
        # Final Raster Output - FileGeodatabase Raster 
        arcpy.AddMessage("Output Format: FileGeodatabase Raster")
        output_format = "GRID"  
    elif re.search(r'.sde', outRasPath):
        # Final Raster Output - SDE Raster 
        arcpy.AddMessage("Output Format: SDE Raster")
        output_format = "GRID"
    else:
        # Final Raster Output - Folder therefore GeoTIFF
        arcpy.AddMessage("Output Format: GeoTIFF file")
        output_format = "TIF"

    # Check for ArcGIS Spatial Analyst extension
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        arcpy.AddMessage("Checked out \"Spatial\" Extension")
    else:
        # Raise a custom exception
        raise LicenseError
    
    arcpy.AddMessage("Loading Input Raster(s): {0}, {1}".format(SWIR_BandPath, NIR_BandPath))
    SWIR_Ras = Raster(SWIR_BandPath)
    NIR_Ras = Raster(NIR_BandPath)
    
    arcpy.AddMessage("Calculating Ferrous Mineral Index (FMI)")
    # The algorithm to calculate Ferrous Mineral Index (FMI)
    # FMI = SWIR / NIR
    outRas_FMI = SWIR_Ras / NIR_Ras
    
    # Determine the output format based on the output workspace
    if output_format == "TIF":
        outRasPath = outRasPath + ".tif"
    
    arcpy.AddMessage("Saving raster to: {0}".format(outRasPath))
    # Save raster to desired output folder or workspace
    outRas_FMI.save(outRasPath)
    
except LicenseError:
    arcpy.AddMessage("ArcGIS Spatial Analyst license is unavailable")
except arcpy.ExecuteError:
    arcpy.AddMessage(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(f"Error: {str(e)}")
finally:
    # Check in the ArcGIS Spatial Analyst extension
    arcpy.AddMessage("Checked in \"Spatial\" Extension")
    arcpy.CheckInExtension("Spatial")
