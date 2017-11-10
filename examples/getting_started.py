from context import botticelli

def example_routine(params):
  params["depth"] += 1

  print("hello world from depth " + str(params["depth"]))  

  return params

def example_callback(params):
  print("goodbye world from depth " + str(params["depth"]))

  params["run"] = False # only run once

  params["depth"] -= 1

  return params

def example_bailout(params):
  print("bailing out")

  return params

def example_scene_detector():
  return True # pretend scene was detected

second_action = botticelli.Action(example_routine,
    example_callback,
    1,
    [],
    example_bailout)

first_action = botticelli.Action(example_routine,
    example_callback,
    1,
    [
      botticelli.Trigger(
        botticelli.Scene("example_scene", example_scene_detector),
        second_action)
    ],
    example_bailout)

# required keys (and their boolean values) to work: run, wait, and timed_out
params = { "run": True, "wait": True, "timed_out": False, "depth": 0 }

first_action.perform(params)