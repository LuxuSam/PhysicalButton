import time
import threading


def thread_react(printer, pressed_button):
    # save value of button (pushed or released)
    button_value = pressed_button.value

    # search for pressed button
    for btn in printer._settings.get(["buttons"]):
        if btn.get('gpio') == "none":
            continue
        if int(btn.get('gpio')) == pressed_button.pin.number:
            button = btn
            break

    wait_time = int(button.get('buttonTime'))
    time.sleep(wait_time / 1000)

    if pressed_button.value == button_value:
        printer._logger.debug(f"Reacting to button {button.get('buttonName')}")
        # execute actions for button in order
        for activity in button.get('activities'):
            exit_code = 0
            printer._logger.debug(f"Sending activity with identifier '{activity.get('identifier')}' ...")
            if activity.get('type') == "action":
                # send specified action
                exit_code = printer.sendAction(activity.get('execute'))
            elif activity.get('type') == "gcode":
                # send specified gcode
                exit_code = printer.sendGcode(activity.get('execute'))
            elif activity.get('type') == "system":
                # send specified system
                exit_code = printer.runSystem(activity.get('execute'))
            elif activity.get('type') == "file":
                # select the file at the given location
                exit_code = printer.selectFile(activity.get('execute'))
            elif activity.get('type') == "output":
                # generate output for given amount of time
                exit_code = printer.generateOutput(activity.get('execute'))
            elif activity.get('type') == "plugin":
                exit_code = printer.sendPluginAction(activity.get('execute'))
            else:
                printer._logger.debug(
                    f"The activity with identifier '{activity.get('identifier')}' is not known (yet)!")
                continue
            # Check if an executed activity failed
            if exit_code == 0:
                printer._logger.debug(
                    f"The activity with identifier '{activity.get('identifier')}' was executed successfully!")
                continue
            if exit_code == -1:
                printer._logger.error(
                    f"The activity with identifier '{activity.get('identifier')}' failed! Aborting follwing activities!")
                break
            if exit_code == -2:
                printer._logger.error(
                    f"The activity with identifier '{activity.get('identifier')}' failed! No GPIO specified!")
                continue


def react_to_input(self, pressed_button):
    t = threading.Thread(target=self.thread_react, args=(pressed_button,))
    t.start()
