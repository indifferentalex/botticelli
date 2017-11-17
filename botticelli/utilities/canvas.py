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

  r, g, b, a = current_screen.getpixel((x, y))

  return { "r": r, "g": g, "b": b }

def check_for_color(xs, ys, xe, ye, r, g, b):
  refresh_screen()

  xs, ys = coords_parser(xs, ys)
  xe, ye = coords_parser(xe, ye)

  for i in range(xs, xe, 1):
    for j in range(ys, ye, 1):
      color = current_screen.getpixel((i, j))

      if (color[0] == r) and (color[1] == g) and (color[2] == b):
        return (i, j)

  return False

def only_contains_color(xs, ys, xe, ye, r, g, b):
  refresh_screen()

  xs, ys = coords_parser(xs, ys)
  xe, ye = coords_parser(xe, ye)

  for i in range(xs, xe, 1):
    for j in range(ys, ye, 1):
      color = current_screen.getpixel((i, j))

      if (color[0] != r) or (color[1] != g) or (color[2] != b):
        return False

  return True

def first_and_last_color_in_area(xs, ys, xe, ye, r, g, b):
  refresh_screen()

  xs, ys = coords_parser(xs, ys)
  xe, ye = coords_parser(xe, ye)

  matched_coords = []

  # TODO optimize, start top left, as soon as first match is found
  # restart from bottom right until second match is found
  for i in range(xs, xe, 1):
    for j in range(ys, ye, 1):
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

  x = random.randrange(xs, xe, 1)
  y = random.randrange(ys, ye, 1)

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

def rotate_point(center_point, point, angle):
  angle = math.radians(angle)

  temp_point = point[0] - center_point[0], point[1] - center_point[1]
  temp_point = (temp_point[0] * math.cos(angle) - temp_point[1] * math.sin(angle), temp_point[0] * math.sin(angle) + temp_point[1] * math.cos(angle))
  temp_point = temp_point[0] + center_point[0], temp_point[1] + center_point[1]

  return temp_point

def move_mouse(end_x, end_y):
  end_x, end_y = coords_parser(end_x, end_y)

  iteration_duration = 0

  db = sqlite3.connect('C:/Development/apparition/paths/paths.sqlite')

  iterator = db.cursor()

  start_x = mouse.position()[0]
  start_y = mouse.position()[1]

  distance = math.sqrt(math.pow(math.fabs(start_x - end_x), 2) + math.pow(math.fabs(start_y - end_y), 2))

  delta_y = start_y - end_y
  delta_x = start_x - end_x

  angle = math.degrees(math.atan2(delta_x, delta_y))

  good_paths = []

  threshold = 5

  while not good_paths:
    iterator.execute("select * from paths")

    for path in iterator.fetchall():
      if (math.fabs(path[0] - distance) < threshold):
        good_paths.append(path)

    threshold += 5

  selected_path = good_paths[random.randint(0, len(good_paths) - 1)]

  angle_difference = angle - selected_path[1]

  nodes = str(selected_path[2])
  nodes = nodes.replace('[', '')
  nodes = nodes.replace(']', '')
  nodes = nodes.replace('), ', '|')
  nodes = nodes.replace('(', '')
  nodes = nodes.replace(', ', ',')

  nodes = nodes.split('|')
  nodes[-1] = nodes[-1].replace(')', '')

  i = 0

  if (len(nodes) > 2):
    for node in nodes:
      try:
        nodes[i] = node.split(',')
        nodes[i][0] = int(nodes[i][0])
        nodes[i][1] = int(nodes[i][1])
      except:
        raise ValueError
      
      i += 1

    try:
      total_x_translation = nodes[0][0] - start_x
      total_y_translation = nodes[0][1] - start_y
    except:
      raise ValueError

    prev_x = int(nodes[0][0])
    prev_y = int(nodes[0][1])

    translated_start_x = prev_x - total_x_translation
    translated_start_y = prev_y - total_y_translation

    i = 1

    while i < len(nodes):
      x = int(nodes[i][0])
      y = int(nodes[i][1])

      velocity = math.sqrt(math.pow(math.fabs(x - prev_x), 2) + math.pow(math.fabs(y - prev_y), 2))

      if velocity < 2:
        current_thickness = 1
      elif velocity < 3:
        current_thickness = 2
      elif velocity < 4:
        current_thickness = 3
      else:
        current_thickness = 4

      translated_x = x - total_x_translation
      translated_y = y - total_y_translation
      translated_prev_x = prev_x - total_x_translation
      translated_prev_y = prev_y - total_y_translation

      rotated_coords = rotate_point((translated_start_x, translated_start_y), (translated_x, translated_y), -angle_difference)

      rotated_x = rotated_coords[0]
      rotated_y = rotated_coords[1]

      rotated_coords = rotate_point((translated_start_x, translated_start_y), (translated_prev_x, translated_prev_y), -angle_difference)

      rotated_prev_x = rotated_coords[0]
      rotated_prev_y = rotated_coords[1]

      mouse.move(int(rotated_x), int(rotated_y))

      time.sleep(iteration_duration)

      prev_x = x
      prev_y = y

      i += 1

def move_mouse_to_area(xs, ys, xe, ye):
  x, y = point_in_area(xs, ys, xe, ye)

  move_mouse(x, y)

def move_mouse_to_color_area(xs, ys, xe, ye, r, g, b):
  color_area = first_and_last_color_in_area(xs, ys, xe, ye, r, g, b)

  if color_area:
    x, y = point_in_area(color_area[0][0], color_area[0][1], color_area[1][0] + 1, color_area[1][1] + 1)

    move_mouse(x, y)

    return True
  else:
    return False

def scrollDown(amount):
  mouse.scroll(-1 * amount);

  wait_for("pause")

def scrollUp(amount):
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