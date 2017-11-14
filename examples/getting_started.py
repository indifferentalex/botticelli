from context import botticelli

# write any routines to run

def dig(params):
  params["depth"] += 1

  print("hello world from depth " + str(params["depth"]))  

  return params

def climb(params):
  print("goodbye world from depth " + str(params["depth"]))

  params["depth"] -= 1

  return params

# write scene detectors for triggering other actions

def keep_digging_detector(params):
  return params["depth"] < 2

def keep_climbing_detector(params):
  return params["depth"] > 0

def stop_digging_detector(params):
  return params["depth"] == 2

# create all the actions and triggers for them

climb_up = botticelli.Action(
  "climb up",
  climb,
  1,
  [],
  None)

climb_up.add_trigger(
  botticelli.Trigger(
    botticelli.Scene("keep climbing detector", keep_climbing_detector),
    climb_up))

dig_down = botticelli.Action(
  "dig down",
  dig,
  1,
  [],
  None)

dig_down.add_trigger(
  botticelli.Trigger(
    botticelli.Scene("keep digging detector", keep_digging_detector),
    dig_down))

dig_down.add_trigger(
  botticelli.Trigger(
    botticelli.Scene("target depth detector", stop_digging_detector),
    climb_up))

# choose the first action, create a params dictionary and start the main loop

action_to_run = dig_down
params = { "depth": 0 }

while action_to_run:
  action_to_run, params = action_to_run.perform(params)
