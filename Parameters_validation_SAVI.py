import arcpy

def validate_parameters():
    try:
        # Validate the first parameter: SR_NIR_BandPath
        SR_NIR_BandPath = arcpy.GetParameterAsText(0)
        if not arcpy.Exists(SR_NIR_BandPath):
            raise ValueError("The NIR Band path does not exist: {}".format(SR_NIR_BandPath))
        
        # Validate the second parameter: SR_VR_BandPath
        SR_VR_BandPath = arcpy.GetParameterAsText(1)
        if not arcpy.Exists(SR_VR_BandPath):
            raise ValueError("The VR Band path does not exist: {}".format(SR_VR_BandPath))

        # Validate the third parameter: L factor for SAVI
        L = arcpy.GetParameterAsText(2)
        try:
            L = float(L)
        except ValueError:
            raise ValueError("The L factor must be a numeric value between 0 and 1")
        if not (0 <= L <= 1):
            raise ValueError("The L factor must be a value between 0 and 1")
        
        # Validate the fourth parameter: outRasPath
        outRasPath = arcpy.GetParameterAsText(3)
        if not outRasPath:
            raise ValueError("Output raster path cannot be empty")

    except Exception as e:
        arcpy.AddError(str(e))

if __name__ == "__main__":
    validate_parameters()
