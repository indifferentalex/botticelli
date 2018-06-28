from context import botticelli
from botticelli.utilities import canvas
from botticelli.utilities import detector_inspector

# The detector inspector ignores params returned by the detectors,
# all cases should be written explicity

def detect_green(params):
    return (canvas.color_present(
            166,
            226,
            46,
            0.3,
            0.5,
            0.2,
            0.4),
        params)

def sublime_text(params):
    sublime_text_open = canvas.color_present(
            166,
            226,
            46,
            0.3,
            0.5,
            0.2,
            0.4) &&
            canvas.color_present(
                166,
                226,
                46,
                0.3,
                0.5,
                0.2,
                0.4)

    return (sublime_text_open, params)    

green_screen = botticelli.Scene("Detect green", detect_green)
sublime_text = botticelli.Scene("Detect green", detect_green)

detector_inspector.inspect([
    (green_screen_scene, []),
    (scene, []),
])

# print canvas.color_present(
#             166,
#             126,
#             46,
#             0.0,
#             0.0,
#             1.0,
#             1.0)