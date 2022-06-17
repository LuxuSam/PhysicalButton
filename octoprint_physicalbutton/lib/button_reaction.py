import time
import threading

from .. import button_globals as bg

from .activities.actions import send_action
from .activities.file import select_file
from .activities.gcode import send_gcode
from .activities.output import generate_output
from .activities.plugin_action import send_plugin_action
from .activities.system import run_system


def react_to_input(pressed_button):
    t = threading.Thread(target=thread_react, args=(pressed_button,))
    t.start()


def thread_react(pressed_button):
    # save value of button (pushed or released)
    button_value = pressed_button.value

    # search for pressed button
    for btn in bg.plugin._settings.get(["buttons"]):
        if btn.get('gpio') == "none":
            continue
        if int(btn.get('gpio')) == pressed_button.pin.number:
            button = btn
            break

    wait_time = int(button.get('buttonTime'))
    time.sleep(wait_time / 1000)

    if pressed_button.value == button_value:
        bg.plugin._logger.debug(f"Reacting to button {button.get('buttonName')}")
        # execute actions for button in order
        for activity in button.get('activities'):
            exit_code = 0
            bg.plugin._logger.debug(f"Sending activity with identifier '{activity.get('identifier')}' ...")
            if activity.get('type') == "action":
                exit_code = send_action(activity.get('execute'))
            elif activity.get('type') == "gcode":
                exit_code = send_gcode(activity.get('execute'))
            elif activity.get('type') == "system":
                exit_code = run_system(activity.get('execute'))
            elif activity.get('type') == "file":
                exit_code = select_file(activity.get('execute'))
            elif activity.get('type') == "output":
                exit_code = generate_output(activity.get('execute'))
            elif activity.get('type') == "plugin":
                exit_code = send_plugin_action(activity.get('execute'))
            else:
                bg.plugin._logger.debug(
                    f"The activity with identifier '{activity.get('identifier')}' is not known (yet)!")
                continue

            # Check if an executed activity failed
            if exit_code == 0:
                bg.plugin._logger.debug(
                    f"The activity with identifier '{activity.get('identifier')}' was executed successfully!")
                continue
            if exit_code == -1:
                bg.plugin._logger.error(f"The activity with identifier '{activity.get('identifier')}' failed! "
                                        f"Aborting following activities!")
                break
            if exit_code == -2:
                bg.plugin._logger.error(
                    f"The activity with identifier '{activity.get('identifier')}' failed! "
                    f"No GPIO specified!")
                continue
