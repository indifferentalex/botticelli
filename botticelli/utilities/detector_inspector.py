import botticelli

# The detector inspector ignores params returned by the detectors (no state flow),
# all cases should be written explicity

def inspect(scenes_and_params):
    for scene, all_params in scenes_and_params:
        if not all_params:
            print scene.name + ": " + str(scene.detected({})[0])
        else:
            for params in all_params:
                print scene.name + str(params) + ": " + str(scene.detected(params)[0])