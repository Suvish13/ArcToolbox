import os
import re
import arcpy

class LicenseError(Exception):
    pass

def validate_parameters(SR_NIR_BandPath, SR_BLUE_BandPath, outRasPath):
    """
    Validate input parameters for the ArcPy script.

    :param SR_NIR_BandPath: Path to the NIR band raster
    :param SR_BLUE_BandPath: Path to the BLUE band raster
    :param outRasPath: Output path for the result raster
    :return: None
    :raises: ValueError, LicenseError
    """
    # Check if input raster files exist
    if not os.path.isfile(SR_NIR_BandPath):
        raise ValueError(f"NIR band raster file does not exist: {SR_NIR_BandPath}")
    
    if not os.path.isfile(SR_BLUE_BandPath):
        raise ValueError(f"BLUE band raster file does not exist: {SR_BLUE_BandPath}")
    
    # Check if the output directory is valid
    output_dir = os.path.dirname(outRasPath)
    if not os.path.isdir(output_dir):
        raise ValueError(f"Output directory does not exist: {output_dir}")

    # Check for valid output file extension
    if not re.search(r'.(gdb|mdb|sde|tif|tiff)$', outRasPath, re.IGNORECASE):
        raise ValueError("Output path must have one of the following extensions: .gdb, .mdb, .sde, .tif, .tiff")

    # Check for ArcGIS Spatial Analyst extension
    if arcpy.CheckExtension("Spatial") != "Available":
        raise LicenseError("ArcGIS Spatial Analyst license is unavailable")

if __name__ == "__main__":
    # Example usage of the validate_parameters function for testing
    try:
        validate_parameters("path_to_nir_band", "path_to_blue_band", "output_path")
        print("Parameter validation passed.")
    except Exception as e:
        print(f"Parameter validation failed: {e}")
