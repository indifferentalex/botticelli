class Scene:
  """
  A scene has a name and a detector function, which returns true if the scene is
  detected, false otherwise.

  Attributes:
    name (string): A descriptive name of what the scene consists of.
    detector (function): A function that checks if that scene is present.
  """
  def __init__(self, name, detector):
    self.name = name
    self.detector = detector

  def detected(self, params):
    detected, params = self.detector(params)
    
    return (detected, params)