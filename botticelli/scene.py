class Scene:
  def __init__(self, name, detector):
    self.name = name
    self.detector = detector

  def detected(self):
    return self.detector()