from botticelli import utilities as canvas
from pymouse import PyMouseEvent
import webcolors
import time

mouse_position = canvas.mouse_position()
color_at_mouse = canvas.get_color_at(
    int(mouse_position["x"]), int(mouse_position["y"]))


# https://stackoverflow.com/a/9694246
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0])**2
        gd = (g_c - requested_colour[1])**2
        bd = (b_c - requested_colour[2])**2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


def set_mouse_pos():
    global mouse_position, color_at_mouse

    mouse_position = canvas.mouse_position()
    color_at_mouse = canvas.get_color_at(
        int(abs_pos()["x"]), int(abs_pos()["y"]))


def abs_pos():
    return mouse_position


def rel_pos():
    return {
        "x": round(abs_pos()["x"] / (1.0 * canvas.screen_width), 3),
        "y": round(abs_pos()["y"] / (1.0 * canvas.screen_height), 3)
    }


def formatted_color():
    return "X: " + str(abs_pos()["x"]) + "/" + str(
        rel_pos()["x"]) + " Y: " + str(abs_pos()["y"]) + "/" + str(
            rel_pos()["y"]) + " RGB: " + str(color_at_mouse["r"]) + ", " + str(
                color_at_mouse["g"]) + ", " + str(color_at_mouse["b"])


def named_color():
    actual_name, closest_name = get_colour_name(
        (color_at_mouse["r"], color_at_mouse["g"], color_at_mouse["b"]))

    return closest_name


def detailed_information():
    return formatted_color() + " - " + named_color()


def absolute_parameters():
    return "    abs: (" + str(abs_pos()["x"]) + ", " + str(
        abs_pos()["y"]) + ", " + str(color_at_mouse["r"]) + ", " + str(
            color_at_mouse["g"]) + ", " + str(color_at_mouse["b"]) + ")"


def relative_parameters():
    return "    rel: (" + str(rel_pos()["x"]) + ", " + str(
        rel_pos()["y"]) + ", " + str(color_at_mouse["r"]) + ", " + str(
            color_at_mouse["g"]) + ", " + str(color_at_mouse["b"]) + ")"


def print_click_information():
    print detailed_information()
    print absolute_parameters()
    print relative_parameters()


class ColorPicker(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        if button == 1:
            if press:
                set_mouse_pos()
                print_click_information()
        else:
            self.stop()


color_picker = ColorPicker()
color_picker.run()

while True:
    a = 5
