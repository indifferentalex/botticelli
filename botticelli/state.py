class State:
  """
  A state has a name and a detector function, which returns true if the state is
  detected, false otherwise.

  Attributes:
    name (string): A descriptive name of what the state consists of.
    detector (function): A function that checks if that state is present.
  """
  def __init__(self, name, detector):
    self.name = name
    self.detector = detector

  def detected(self, params):
    return self.detector(params)