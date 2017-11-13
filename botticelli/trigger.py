class Trigger:
  """
  A trigger is simply a state/action pair that can be passed in to actions
  (along with other triggers if required).

  Attributes:
    state (botticelli.State): A state that will trigger the accompanying
    action.
    action (botticelli.Action): An action that will be triggered if the
    accompanying state is detected.
  """
  def __init__(self, state, action):
    self.state = state
    self.action = action