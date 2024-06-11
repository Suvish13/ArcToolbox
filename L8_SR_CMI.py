class LicenseError(Exception):
    pass

# Set desktop license used to Basic (keyword is arcview)
import os
import re
import arcpy
from arcpy.sa import *

# Allow ArcPy to overwrite outputs
arcpy.env.overwriteOutput = True

# Get the Input Parameters
SWIR1_BandPath = arcpy.GetParameterAsText(0)
SWIR2_BandPath = arcpy.GetParameterAsText(1)

# Set the default output path from parameter validation script
outRasPath = arcpy.GetParameterAsText(2)

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

    arcpy.AddMessage("Loading Input Raster(s): {0}, {1}".format(SWIR1_BandPath, SWIR2_BandPath))
    SWIR1_Ras = Raster(SWIR1_BandPath)
    SWIR2_Ras = Raster(SWIR2_BandPath)

    arcpy.AddMessage("Calculating Clay Mineral Index (CMI)")
    # The algorithm to calculate Clay Mineral Index (CMI)
    # CMI = SWIR1 / SWIR2
    outRas_CMI = SWIR1_Ras / SWIR2_Ras

    # Determine the output format based on the output workspace
    if output_format == "TIF":
        outRasPath = outRasPath + ".tif"

    arcpy.AddMessage("Saving raster to: {0}".format(outRasPath))
    # Save raster to desired output folder or workspace
    outRas_CMI.save(outRasPath)

except LicenseError:
    arcpy.AddMessage("ArcGIS Spatial Analyst license is unavailable")
except arcpy.ExecuteError:
    arcpy.AddMessage(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(str(e))
finally:
    # Check in the ArcGIS Spatial Analyst extension
    arcpy.AddMessage("Checked in \"Spatial\" Extension")
    arcpy.CheckInExtension("Spatial")
