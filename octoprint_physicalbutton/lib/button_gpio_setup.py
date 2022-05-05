from gpiozero import Button, OutputDevice


def setup_buttons(self):
    global button_list
    for button in self._settings.get(["buttons"]):
        if button.get('gpio') == "none":
            continue
        button_gpio = int(button.get('gpio'))
        button_mode = button.get('buttonMode')
        new_button = Button(button_gpio, pull_up=True, bounce_time=None)
        if button_mode == "Normally Open (NO)":
            new_button.when_pressed = self.reactToInput
        if button_mode == "Normally Closed (NC)":
            new_button.when_released = self.reactToInput
        button_list.append(new_button)
        self.setup_output_pins(button)
    self._logger.debug(f"Added Buttons: {button_list}")
    self._logger.debug(f"Added Output devices: {output_list}")


def setup_output_pins(self, button):
    global output_list
    for activity in list(filter(lambda a: a.get('type') == "output", button.get('activities'))):
        output_gpio = activity.get('execute').get('gpio')
        # check if gpio has to be setup
        if output_gpio == 'none' or int(output_gpio) in list(map(lambda oD: oD.pin.number, output_list)):
            continue
        output_device = OutputDevice(int(output_gpio))
        initial_value = activity.get('execute').get('initial')
        if initial_value == "HIGH":
            output_device.on()
        output_list.append(output_device)


def remove_buttons(self):
    global button_list
    self._logger.debug(f"Buttons to remove: {button_list}")
    for button in button_list:
        button.close()
    button_list.clear()


def remove_outputs(self):
    global output_list
    self._logger.debug(f"Output devices to remove: {output_list}")
    for output_device in output_list:
        output_device.close()
    output_list.clear()
