import time

class Action:
  """
  An action is initiliazed with a name, a routine, a wait for duration,
  an array of triggers and a recovery action. The action is performed
  by calling the perform function. Once the routine is run, the perform
  function will loop for all triggers checking if any of their scenes
  have been detected, in which case their corresponding action will be
  returned. If no triggers are activated then the recovery action will
  be returned.

  Attributes:
    name (string): The name of the action, for better orientation when building
    routine (function): A function that will run when action is performed.
    wait_for (object): Seconds to wait for any triggers to be detected, any
      object that can be cast to a float.
    triggers (array of botticelli.Trigger): An array of triggers, which consist
      of a scene and an action. When the scene is detected, the corresponding
      action gets performed.
    recovery (a botticelli.Action): The action to be performed if no triggers
      are activated and the wait loop times out.    
  """
  def __init__(self, name, routine, wait_for, triggers, recovery, options = {}):
    self.name = name
    self.routine = routine
    self.wait_for = wait_for
    self.triggers = triggers
    self.recovery = recovery
    self.options = options

  def perform(self, params):
    self.routine(params)

    started_at = time.time()
    wait_time = float(self.wait_for)

    while (time.time() - started_at < wait_time):
      for trigger in self.triggers:
        if trigger.scene.detected(params): 
          return (trigger.action, params)

      time.sleep(0.1)

    return (self.recovery, params)

  def set_recovery(self, recovery):
    self.recovery = recovery

  def add_trigger(self, trigger):
    self.triggers.append(trigger)
