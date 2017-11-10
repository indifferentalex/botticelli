import time

# configuration start
refresh_rate = 0.1 # how often to check scene, in milliseconds
# configuration end

class Scene:
  def __init__(self, scene_name):
    self.name = scene_name

  def detected(self):
    return True # for now

class Action:
  def __init__(self, routine, callback, wait_for, triggers, bailout):
    self.routine = routine
    self.callback = callback
    self.wait_for = wait_for
    self.triggers = triggers
    self.bailout = bailout
 
  def run_routine(self, params):
    params = self.routine(params)

    if "wait" in params and params["wait"]:
      return params

    started_at = time.time()

    while (time.time() - started_at < self.wait_for):
      for trigger in self.triggers:
        if trigger.scene.detected():
          return trigger.action.perform(params)

      time.sleep(refresh_rate)

    params["timed_out"] = True

    return params

  def run_callback(self, params):
    return self.callback(params)

  def perform(self, params):
    params = self.run_routine(params)

    return self.run_callback(params)

class Trigger:
  def __init__(self, scene, action):
    self.scene = scene
    self.action = action

def example_routine(params):
  print("hello world")

  return params

def example_callback(params):
  print("goodbye world")

  return params

def example_bailout(params):
  print("bailing out")

  return params

second_action = Action(example_routine, example_callback, 1, [], example_bailout)
first_action = Action(example_routine, example_callback, 1, [Trigger(Scene("example_scene"), second_action)], example_bailout)

params = {}

first_action.perform(params)