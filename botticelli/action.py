import time

class Action:
  def __init__(self, routine, callback, wait_for, triggers, bailout):
    self.routine = routine
    self.callback = callback
    self.wait_for = wait_for
    self.triggers = triggers
    self.bailout = bailout
 
  def run_routine(self, params):
    params = self.routine(params)

    if not "wait" in params or not params["wait"]:
      return params

    started_at = time.time()

    while (time.time() - started_at < self.wait_for):
      for trigger in self.triggers:
        if trigger.scene.detected():          
          return trigger.action.perform(params)

      time.sleep(0.1)

    params["timed_out"] = True

    return params

  def run_callback(self, params):
    return self.callback(params)

  def perform(self, params):
    while params["run"]:
      params = self.run_routine(params)

      params = self.run_callback(params)

    return params