import arcpy
import os

def validate_input_params(SWIR1_BandPath, SWIR2_BandPath, outRasPath):
    errors = []

    # Validate SWIR1 Band Path
    if not os.path.exists(SWIR1_BandPath):
        errors.append("SWIR1 Band path does not exist.")
    
    # Validate SWIR2 Band Path
    if not os.path.exists(SWIR2_BandPath):
        errors.append("SWIR2 Band path does not exist.")
    
    # Validate Output Raster Path
    out_dir = os.path.dirname(outRasPath)
    if not os.path.exists(out_dir):
        errors.append("Output directory does not exist.")
    
    # Output Format Validation
    if not (outRasPath.endswith('.tif') or outRasPath.endswith('.img') or outRasPath.endswith('.gdb') or outRasPath.endswith('.mdb') or outRasPath.endswith('.sde')):
        errors.append("Output raster path must be a valid raster format (TIF, IMG, GDB, MDB, SDE).")

    return errors

# Get Parameters
SWIR1_BandPath = arcpy.GetParameterAsText(0)
SWIR2_BandPath = arcpy.GetParameterAsText(1)
outRasPath = arcpy.GetParameterAsText(2)

# Validate Parameters
validation_errors = validate_input_params(SWIR1_BandPath, SWIR2_BandPath, outRasPath)
if validation_errors:
    for error in validation_errors:
        arcpy.AddError(error)
    raise arcpy.ExecuteError
