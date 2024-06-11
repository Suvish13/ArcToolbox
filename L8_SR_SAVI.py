import os
import re
import arcpy
from arcpy.sa import *

class LicenseError(Exception):
    pass

# Allow ArcPy to overwrite outputs
arcpy.env.overwriteOutput = True

# Get the Input Parameters
SR_NIR_BandPath = arcpy.GetParameterAsText(0)
SR_VR_BandPath = arcpy.GetParameterAsText(1)
L = float(arcpy.GetParameterAsText(2))  # The L factor for SAVI, typically a value between 0 and 1
outRasPath = arcpy.GetParameterAsText(3)

try:
    # Define Output Format Based On Output Workspace
    output_format = ""
    if re.search(r'.mdb', outRasPath):
        # Final Raster Output - FGDB Raster 
        arcpy.AddMessage("Output Format: PersonalGeodatabase Raster")
        output_format = "GRID"
    elif re.search(r'.gdb', outRasPath):
        # Final Raster Output - FGDB Raster 
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
    
    arcpy.AddMessage("Loading Input Raster(s): {0}, {1}".format(SR_NIR_BandPath, SR_VR_BandPath))
    SR_NIR_Ras = Raster(SR_NIR_BandPath)
    SR_VR_Ras = Raster(SR_VR_BandPath)
    
    arcpy.AddMessage("Calculating Soil-Adjusted Vegetation Index (SAVI)")
    # The algorithm to calculate Soil-Adjusted Vegetation Index (SAVI)
    # SAVI = (NIR - VR) / (NIR + VR + L) * (1 + L)
    outRas_SAVI = ((SR_NIR_Ras - SR_VR_Ras) / (SR_NIR_Ras + SR_VR_Ras + L)) * (1 + L)
    
    # Determine the output format based on the output workspace
    if output_format == "TIF":
        outRasPath = outRasPath + ".tif"
    
    arcpy.AddMessage("Saving raster to: {0}".format(outRasPath))
    # Save raster to desired output folder or workspace
    outRas_SAVI.save(outRasPath)
    
except LicenseError:
    arcpy.AddError("ArcGIS Spatial Analyst license is unavailable")
except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddError(str(e))
finally:
    # Check in the ArcGIS Spatial Analyst extension
    arcpy.AddMessage("Checked in \"Spatial\" Extension")
    arcpy.CheckInExtension("Spatial")
