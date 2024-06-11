import arcpy
from arcpy.sa import *
import re
from validation import validate_parameters, LicenseError

# Allow ArcPy to overwrite outputs
arcpy.env.overwriteOutput = True

# Get the Input Parameters
SR_NIR_BandPath = arcpy.GetParameterAsText(0)
SR_BLUE_BandPath = arcpy.GetParameterAsText(1)
outRasPath = arcpy.GetParameterAsText(2)

try:
    # Validate parameters
    validate_parameters(SR_NIR_BandPath, SR_BLUE_BandPath, outRasPath)
    arcpy.AddMessage("Parameter validation passed.")

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

    # Check out the ArcGIS Spatial Analyst extension
    arcpy.CheckOutExtension("Spatial")
    arcpy.AddMessage("Checked out \"Spatial\" Extension")

    # Load input rasters
    arcpy.AddMessage(f"Loading Input Raster(s): {SR_NIR_BandPath}, {SR_BLUE_BandPath}")
    SR_NIR_Ras = Raster(SR_NIR_BandPath)
    SR_BLUE_Ras = Raster(SR_BLUE_BandPath)

    # Calculate Soil Carbonate Index
    arcpy.AddMessage("Calculating Soil Carbonate Index")
    outRas_SoilCarbonate = SR_BLUE_Ras / SR_NIR_Ras

    # Determine the output format based on the output workspace
    if output_format == "TIF":
        outRasPath = outRasPath + ".tif"

    arcpy.AddMessage(f"Saving raster to: {outRasPath}")
    # Save raster to desired output folder or workspace
    outRas_SoilCarbonate.save(outRasPath)

except LicenseError as e:
    arcpy.AddError(str(e))
except ValueError as e:
    arcpy.AddError(str(e))
except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
finally:
    # Check in the ArcGIS Spatial Analyst extension
    arcpy.AddMessage("Checked in \"Spatial\" Extension")
    arcpy.CheckInExtension("Spatial")
