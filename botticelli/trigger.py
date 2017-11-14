class Trigger:
  """
  A trigger is simply a scene/action pair that can be passed in to actions
  (along with other triggers if required).

  Attributes:
    scene (botticelli.Scene): A scene that will trigger the accompanying
    action.
    action (botticelli.Action): An action that will be performed if the
    accompanying scene is detected.
  """
  def __init__(self, scene, action):
    self.scene = scene
    self.action = action