import arcpy, os
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""

  def __init__(self):
    """Setup arcpy and the list of tool parameters."""
    self.params = arcpy.GetParameterInfo()

  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened."""
    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""
    if self.params[0].value:
      if not self.params[2].altered:
        outWrkspcPath = arcpy.env.workspace
        outRasName = os.path.splitext(os.path.basename(str(self.params[0].value)))[0]
        self.params[2].value  = outWrkspcPath + "\\" + outRasName + "_SR_NDVI"

    if self.params[2].value:
      outRasName, extension = os.path.splitext(str(self.params[2].value))
      self.params[2].value  = outRasName
    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return
