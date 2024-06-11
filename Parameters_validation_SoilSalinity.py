import arcpy
import os
import re

def validate_parameters():
    """
    This function validates the input parameters provided to the script.
    """
    SR_SWIR1_BandPath = arcpy.GetParameterAsText(0)
    SR_SWIR2_BandPath = arcpy.GetParameterAsText(1)
    SR_NIR_BandPath = arcpy.GetParameterAsText(2)
    outRasPath = arcpy.GetParameterAsText(3)

    messages = []

    # Check if input raster paths exist
    if not arcpy.Exists(SR_SWIR1_BandPath):
        messages.append("SWIR1 Band Path does not exist: {}".format(SR_SWIR1_BandPath))
    if not arcpy.Exists(SR_SWIR2_BandPath):
        messages.append("SWIR2 Band Path does not exist: {}".format(SR_SWIR2_BandPath))
    if not arcpy.Exists(SR_NIR_BandPath):
        messages.append("NIR Band Path does not exist: {}".format(SR_NIR_BandPath))

    # Check if output path is valid
    output_format = ""
    if re.search(r'.mdb', outRasPath):
        output_format = "GRID"
    elif re.search(r'.gdb', outRasPath):
        output_format = "GRID"
    elif re.search(r'.sde', outRasPath):
        output_format = "GRID"
    else:
        output_format = "TIF"
        # Check if the directory exists
        if not os.path.exists(os.path.dirname(outRasPath)):
            messages.append("Output directory does not exist: {}".format(os.path.dirname(outRasPath)))

    return messages

if __name__ == "__main__":
    validation_errors = validate_parameters()
    if validation_errors:
        for error in validation_errors:
            arcpy.AddError(error)
        raise arcpy.ExecuteError("Parameter validation failed.")
    else:
        arcpy.AddMessage("All parameters are valid.")
