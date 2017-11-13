import time

class Action:
  """
  An action is initiliazed with a routine, a callback, a wait_for duration,
  an array of triggers and a bailout. An action is performed by calling the
  perform function, passing in a params hash. The params hash _must_ contain
  the keys: run, wait and timed_out and boolean values for each of them.

  Functions provided as the routine, callback and bailout (as well as those
  of subsequent actions in the triggers) must maintain these three keys.

  Attributes:
    routine (function): A function that will run when action is performed.
    callback (function): A function that will run after the main routine and
      and any detected triggers are finished executing.
    wait_for (float): Seconds to wait for any triggers to be detected.
    triggers (array of pairs of botticelli.Action): An array of triggers,
      which are pairs of actions, the first of which detects certain states
      and the second is the action to be performed if that state is detected.
    bailout (function): A function to run in the case of something going
      wrong (incompatible state detected, action returning an error, etc.).
      Bailouts are not currently implemented.
  """
  def __init__(self, routine, callback, wait_for, triggers, bailout):
    self.routine = routine
    self.callback = callback
    self.wait_for = wait_for
    self.triggers = triggers
    self.bailout = bailout
 
  def run_routine(self, params):
    params = self.routine(params)

    if not params["wait"]:
      return params

    started_at = time.time()

    while (time.time() - started_at < self.wait_for):
      for trigger in self.triggers:
        params = trigger[0].perform(params)

        if params["detected"]: 
          return trigger[1].perform(params)

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