import os
import arcpy

class LicenseError(Exception):
    pass

def validate_parameters():
    # Get the Input Parameters
    SWIR_BandPath = arcpy.GetParameterAsText(0)
    RED_BandPath = arcpy.GetParameterAsText(1)
    NIR_BandPath = arcpy.GetParameterAsText(2)
    BLUE_BandPath = arcpy.GetParameterAsText(3)
    outRasPath = arcpy.GetParameterAsText(4)

    # Validate input raster paths
    raster_paths = [SWIR_BandPath, RED_BandPath, NIR_BandPath, BLUE_BandPath]
    for path in raster_paths:
        if not arcpy.Exists(path):
            arcpy.AddError(f"Input raster does not exist: {path}")
            raise FileNotFoundError(f"Input raster does not exist: {path}")
        if not path.lower().endswith(('.tif', '.img', '.jp2', '.png', '.jpg', '.bmp')):
            arcpy.AddError(f"Invalid raster file format: {path}")
            raise ValueError(f"Invalid raster file format: {path}")

    # Validate output path
    if not outRasPath:
        arcpy.AddError("Output raster path is required.")
        raise ValueError("Output raster path is required.")
    
    output_dir = os.path.dirname(outRasPath)
    if not os.path.exists(output_dir):
        arcpy.AddError(f"Output directory does not exist: {output_dir}")
        raise FileNotFoundError(f"Output directory does not exist: {output_dir}")
    
    # Determine output format
    output_format = ""
    if outRasPath.lower().endswith('.mdb'):
        output_format = "GRID"
    elif outRasPath.lower().endswith('.gdb'):
        output_format = "GRID"
    elif outRasPath.lower().endswith('.sde'):
        output_format = "GRID"
    elif outRasPath.lower().endswith('.tif'):
        output_format = "TIF"
    else:
        arcpy.AddError("Invalid output raster format. Supported formats are: .mdb, .gdb, .sde, .tif")
        raise ValueError("Invalid output raster format. Supported formats are: .mdb, .gdb, .sde, .tif")

    return SWIR_BandPath, RED_BandPath, NIR_BandPath, BLUE_BandPath, outRasPath, output_format

if __name__ == "__main__":
    try:
        SWIR_BandPath, RED_BandPath, NIR_BandPath, BLUE_BandPath, outRasPath, output_format = validate_parameters()
        arcpy.AddMessage("Parameters validated successfully.")

        # Place the main script logic here, using the validated parameters
        # For example:
        # main_processing(SWIR_BandPath, RED_BandPath, NIR_BandPath, BLUE_BandPath, outRasPath, output_format)

    except (FileNotFoundError, ValueError, LicenseError) as e:
        arcpy.AddError(str(e))
    except Exception as e:
        arcpy.AddError("An unexpected error occurred: " + str(e))
