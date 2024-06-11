import arcpy
from arcpy.sa import *

# Custom exception for license errors
class LicenseError(Exception):
    pass

# Allow ArcPy to overwrite outputs
arcpy.env.overwriteOutput = True

# Get the Input Parameters
SR_NIR_BandPath = arcpy.GetParameterAsText(0)
SR_SWIR_BandPath = arcpy.GetParameterAsText(1)
outRasPath = arcpy.GetParameterAsText(2)

try:
    # Check for ArcGIS Spatial Analyst extension
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        arcpy.AddMessage("Checked out \"Spatial\" Extension")
    else:
        # Raise a custom exception
        raise LicenseError

    arcpy.AddMessage("Loading Input Raster(s): {0}, {1}".format(SR_NIR_BandPath, SR_SWIR_BandPath))
    SR_NIR_Ras = Raster(SR_NIR_BandPath)
    SR_SWIR_Ras = Raster(SR_SWIR_BandPath)

    arcpy.AddMessage("Calculating Normalized Difference Moisture Index (NDMI)")
    # Calculate NDMI
    outRas_NDMI = (SR_NIR_Ras - SR_SWIR_Ras) / (SR_NIR_Ras + SR_SWIR_Ras)

    arcpy.AddMessage("Saving raster to: {0}".format(outRasPath))
    # Save raster to desired output folder or workspace
    outRas_NDMI.save(outRasPath)

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
