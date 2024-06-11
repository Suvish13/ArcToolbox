import os
import arcpy

def validate_parameters(SWIR_BandPath, NIR_BandPath, outRasPath):
    # Check if SWIR_BandPath is a valid file
    if not os.path.isfile(SWIR_BandPath):
        raise ValueError(f"SWIR_BandPath is not a valid file: {SWIR_BandPath}")
    
    # Check if NIR_BandPath is a valid file
    if not os.path.isfile(NIR_BandPath):
        raise ValueError(f"NIR_BandPath is not a valid file: {NIR_BandPath}")

    # Check if outRasPath is a writable directory or a valid file path for output
    outRasDir = os.path.dirname(outRasPath)
    if not os.path.isdir(outRasDir) or not os.access(outRasDir, os.W_OK):
        raise ValueError(f"Output path is not writable: {outRasDir}")
    
    arcpy.AddMessage("All input parameters are valid.")
    return True
