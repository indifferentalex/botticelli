"""
The canvas is a utility module that provides a series of helper functions to
interact with the current workspace. Reader functions can be used to detect
what is going on (they work by considering the screen as a XY plane of RGB
values) and writer functions (simulating mouse and keyboard input).
"""

# reader libraries
from PIL import ImageGrab

# writer libraries
from pymouse import PyMouse
from pykeyboard import PyKeyboard

# other imports
import time
from datetime import datetime
import sys
import random
import sqlite3
import math

if sys.platform == "darwin":
  from AppKit import NSScreen
elif sys.platform == "win32":
  from win32api import GetSystemMetrics

def detect_screen_size():
  if sys.platform == "darwin":
    scaling_factor = NSScreen.mainScreen().backingScaleFactor()
    return NSScreen.mainScreen().frame().size.width * scaling_factor, NSScreen.mainScreen().frame().size.height * scaling_factor, NSScreen.mainScreen().backingScaleFactor()
  elif sys.platform == "win32":
    scaling_factor = 1.0
    return GetSystemMetrics(0), GetSystemMetrics(1), scaling_factor
  else:
    raise OSError("Incompatible platform")

screen_width, screen_height, scaling_factor = detect_screen_size()

mouse = PyMouse()
keyboard = PyKeyboard()      

refresh_rate = 0.1 # how often to refresh screen in seconds
last_refresh = datetime.now()
current_screen = ImageGrab.grab()

def refresh_screen():
  global current_screen, last_refresh

  if (datetime.now() - last_refresh).total_seconds() > refresh_rate:
    current_screen = ImageGrab.grab()
    last_refresh = datetime.now()

def coords_parser(x, y):
  if not ((isinstance(x, int) or isinstance(x, float)) and (isinstance(y, int) or isinstance(y, float))):
    raise ValueError

  if isinstance(x, float):
    x = int(screen_width * 1.0 * x)

  if isinstance(y, float):
    y = int(screen_height * 1.0 * y)

  return x, y

def mouse_position(relative = False):
  if relative:
    return { "x": mouse.position()[0] / screen_width, "y": mouse.position()[1] / screen_height }
  else:
    return { "x": int(mouse.position()[0]), "y": int(mouse.position()[1]) }

def color_at(x, y):
  refresh_screen()

  x, y = coords_parser(x, y)

  color = current_screen.getpixel((x, y))

  return { "r": color[0], "g": color[1], "b": color[2] }

def check_for_color(xs, ys, xe, ye, r, g, b):
  refresh_screen()

  xs, ys = coords_parser(xs, ys)
  xe, ye = coords_parser(xe, ye)

  for i in range(xs, xe + 1, 1):
    for j in range(ys, ye + 1, 1):
      color = current_screen.getpixel((i, j))

      if (color[0] == r) and (color[1] == g) and (color[2] == b):
        return (i, j)

  return False

def only_contains_color(xs, ys, xe, ye, r, g, b):
  refresh_screen()

  xs, ys = coords_parser(xs, ys)
  xe, ye = coords_parser(xe, ye)

  for i in range(xs, xe + 1, 1):
    for j in range(ys, ye + 1, 1):
      color = current_screen.getpixel((i, j))

      if (color[0] != r) or (color[1] != g) or (color[2] != b):
        return False

  return True

def first_and_last_instances_of_color_in_area(xs, ys, xe, ye, r, g, b):
  refresh_screen()

  xs, ys = coords_parser(xs, ys)
  xe, ye = coords_parser(xe, ye)

  matched_coords = []

  for i in range(xs, xe + 1, 1):
    for j in range(ys, ye + 1, 1):
      color = current_screen.getpixel((i, j))

      if (color[0] == r) and (color[1] == g) and (color[2] == b):
        matched_coords.append((i, j))

  all_x = map(lambda coords: coords[0], matched_coords)
  all_y = map(lambda coords: coords[1], matched_coords)

  if len(matched_coords) == 0:
    return False
  else:
    return [(min(all_x), min(all_y)), (max(all_x), max(all_y))]

def mouse_in_area(xs, ys, xe, ye):
  xs, ys = coords_parser(xs, ys)
  xe, ye = coords_parser(xe, ye)

  return (mouse_position()["x"] > xs and mouse_position()["x"] < xe and mouse_position()["y"] > ys and mouse_position()["y"] < ye)

def point_in_area(xs, ys, xe, ye):
  xs, ys = coords_parser(xs, ys)
  xe, ye = coords_parser(xe, ye)

  x = random.randrange(xs, xe + 1, 1)
  y = random.randrange(ys, ye + 1, 1)

  return (x, y)  

def wait_for(amount):
  if amount == "very_little":
    time.sleep(random.uniform(0.05, 0.1))
  elif amount == "little":
    time.sleep(random.uniform(0.08, 0.25))
  elif amount == "pause":
    time.sleep(random.uniform(0.4, 0.8))
  elif amount == "medium":
    time.sleep(random.uniform(1.0, 2.0))
  elif amount == "varied":
    time.sleep(random.uniform(2.0, 10.0))
  elif amount == "long_and_random":
    time.sleep(random.uniform(30.0, 600.0))
  else:
    time.sleep(amount)

def move_mouse(end_x, end_y, method):
  end_x, end_y = coords_parser(end_x, end_y)

  end_x /= scaling_factor
  end_y /= scaling_factor

  iteration_duration = 0.002

  start_x = mouse.position()[0]
  start_y = mouse.position()[1]

  distance = math.sqrt(math.pow(math.fabs(start_x - end_x), 2) + math.pow(math.fabs(start_y - end_y), 2))

  delta_y = start_y - end_y
  delta_x = start_x - end_x

  angle = math.degrees(math.atan2(delta_x, delta_y))

  nodes = method(start_x, start_y, end_x, end_y)

  i = 0

  while i < len(nodes):
    mouse.move(nodes[i][0], nodes[i][1])

    time.sleep(iteration_duration)

    i += 1

def jumper_mouse(start_x, start_y, end_x, end_y):
  return [(end_x, end_y)]

def banal_mouse(start_x, start_y, end_x, end_y):
  nodes = []

  delta_x = math.fabs(start_x - end_x)
  delta_y = math.fabs(start_y - end_y)

  # each iteration moves across largest dimension by about 4 pixels
  iterations_count = delta_x / 4.0 if delta_x > delta_y else delta_y / 4.0

  iteration_delta_x = float(start_x - end_x) * -1 / iterations_count
  iteration_delta_y = float(start_y - end_y) * -1 / iterations_count

  i = 0

  while i < iterations_count:
    nodes.append((int(start_x + i * iteration_delta_x), int(start_y + i * iteration_delta_y)))

    i += 1

  return nodes

def move_mouse_to_area(xs, ys, xe, ye):
  x, y = point_in_area(xs, ys, xe, ye)

  move_mouse(x, y)

def move_mouse_to_color_area(xs, ys, xe, ye, r, g, b):
  color_area = first_and_last_color_in_area(xs, ys, xe, ye, r, g, b)

  if color_area:
    x, y = point_in_area(color_area[0][0], color_area[0][1], color_area[1][0], color_area[1][1])

    move_mouse(x, y)

    return True
  else:
    return False

def scroll_down(amount):
  mouse.scroll(-1 * amount);

  wait_for("pause")

def scroll_up(amount):
  mouse.scroll(amount);

  wait_for("pause")

def click():
  mouse.press(int(mouse.position()[0]), int(mouse.position()[1]), 1)

  wait_for("little")

  mouse.release(int(mouse.position()[0]), int(mouse.position()[1]), 1)

def press_keys(keys):
  if len(keys) > 0:
    key = keys.pop(0)

    keyboard.press_key(key)

    wait_for("little")

    press_keys(keys)

    wait_for("very_little")

    keyboard.release_key(key)