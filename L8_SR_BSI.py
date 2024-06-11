
class LicenseError(Exception):
    pass
# Set desktop license used to Basic (keyword is arcview)

import os, sys, string, math, re
from posixpath import pardir
import arcpy
from arcpy import arc
from arcpy.sa import *
try:
    # Validate parameters
    SWIR_BandPath, RED_BandPath, NIR_BandPath, BLUE_BandPath, outRasPath, output_format = validate_parameters()

    # Check for ArcGIS Spatial Analyst extension
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        arcpy.AddMessage("Checked out \"Spatial\" Extension")
    else:
        # Raise a custom exception
        raise LicenseError

    arcpy.AddMessage("Loading Input Raster(s): {0}, {1}, {2}, {3}".format(SWIR_BandPath, RED_BandPath, NIR_BandPath, BLUE_BandPath))
    SWIR_Ras = Raster(SWIR_BandPath)
    RED_Ras = Raster(RED_BandPath)
    NIR_Ras = Raster(NIR_BandPath)
    BLUE_Ras = Raster(BLUE_BandPath)

    arcpy.AddMessage("Calculating Bare Soil Index (BSI)")
    # The algorithm to calculate Bare Soil Index (BSI)
    # BSI = ((SWIR + RED) - (NIR + BLUE)) / ((SWIR + RED) + (NIR + BLUE))
    outRas_BSI = ((SWIR_Ras + RED_Ras) - (NIR_Ras + BLUE_Ras)) / ((SWIR_Ras + RED_Ras) + (NIR_Ras + BLUE_Ras))

    # Determine the output format based on the output workspace
    if output_format == "TIF":
        outRasPath = outRasPath + ".tif"

    arcpy.AddMessage("Saving raster to: {0}".format(outRasPath))
    # Save raster to desired output folder or workspace
    outRas_BSI.save(outRasPath)

except LicenseError:
    arcpy.AddMessage("ArcGIS Spatial Analyst license is unavailable")
except arcpy.ExecuteError:
    arcpy.AddMessage(arcpy.GetMessages(2))
except (FileNotFoundError, ValueError) as e:
    arcpy.AddError(str(e))
except Exception as e:
    arcpy.AddError("An unexpected error occurred: " + str(e))
finally:
    # Check in the ArcGIS Spatial Analyst extension
    arcpy.AddMessage("Checked in \"Spatial\" Extension")
    arcpy.CheckInExtension("Spatial")
