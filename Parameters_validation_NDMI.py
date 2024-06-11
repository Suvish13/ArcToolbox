import arcpy
from arcpy import env

def is_valid_raster(raster_path):
    try:
        # Check if the path exists and is a raster
        if arcpy.Exists(raster_path) and arcpy.Describe(raster_path).datasetType == 'RasterDataset':
            return True
        else:
            return False
    except:
        return False

def is_valid_output_path(output_path):
    try:
        # Check if the output path is writable
        test_path = arcpy.CreateUniqueName("test", output_path)
        arcpy.management.CreateFileGDB(output_path, test_path)
        arcpy.management.Delete(test_path)
        return True
    except:
        return False

def validate_parameters():
    SR_NIR_BandPath = arcpy.GetParameterAsText(0)
    SR_SWIR_BandPath = arcpy.GetParameterAsText(1)
    outRasPath = arcpy.GetParameterAsText(2)

    if not is_valid_raster(SR_NIR_BandPath):
        raise ValueError("Invalid NIR Band Path: Please provide a valid raster path.")

    if not is_valid_raster(SR_SWIR_BandPath):
        raise ValueError("Invalid SWIR Band Path: Please provide a valid raster path.")

    if not is_valid_output_path(outRasPath):
        raise ValueError("Invalid Output Path: Please provide a valid output path.")

# Run validation when the script is executed
validate_parameters()
