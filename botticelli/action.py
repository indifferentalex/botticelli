import time

class Action:
  """
  An action is initiliazed with a routine, a callback, a wait_for duration and
  an array of triggers. An action is performed by calling the
  perform function, passing in a params hash.

  Attributes:
    name (string): The name of the action, for better orientation when building
    routine (function): A function that will run when action is performed.
    callback (function): A function that will run after the main routine and
      and any detected triggers are finished executing.
    wait_for (float): Seconds to wait for any triggers to be detected.
    triggers (array of botticelli.Trigger): An array of triggers, which consist
      of a scene and an action. When the scene is detected, the corresponding
      action gets performed.
  """
  def __init__(self, name, routine, callback, wait_for, triggers):
    self.name = name
    self.routine = routine
    self.callback = callback
    self.wait_for = wait_for
    self.triggers = triggers
 
  def run_routine(self, params):
    params = self.routine(params)

    if not params["wait"]:
      return params

    if len(self.triggers) > 0:
      params["timed_out"] = False

      started_at = time.time()

      while (time.time() - started_at < self.wait_for):
        for trigger in self.triggers:
          if trigger.state.detected(params): 
            return trigger.action.perform(params)

        time.sleep(0.1)

      params["timed_out"] = True

    return params

  def run_callback(self, params):
    return self.callback(params)

  def perform(self, params):
    while True:
      params = self.run_routine(params)

      params = self.run_callback(params)

      if not params["run"]:
        break

    return params