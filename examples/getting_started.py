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

def example_state_detector(params):
  return True # pretend state was detected

second_action = botticelli.Action(
  "second action",
  example_routine,
  example_callback,
  1,
  [])

first_action = botticelli.Action(
  "first action",
  example_routine,
  example_callback,
  1,
  [
    botticelli.Trigger(
      botticelli.State("example_state_detector", example_state_detector),
      second_action
    )
  ])

# required keys (and their boolean values) to work: run, wait and timed_out,
# depth is an additional custom param used for this example.
params = { "run": True, "wait": True, "timed_out": False, "depth": 0 }

first_action.perform(params)