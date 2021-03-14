# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import RPi.GPIO as GPIO
import time

class PhysicalbuttonPlugin(octoprint.plugin.StartupPlugin,
                           octoprint.plugin.SettingsPlugin,
                           octoprint.plugin.TemplatePlugin,
                           octoprint.plugin.AssetPlugin,
                           octoprint.plugin.ShutdownPlugin
                           ):

    def on_after_startup(self):
        GPIO.setmode(GPIO.BCM)
        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            buttonMode = button.get("buttonMode")
            buttonTime = int(button.get("buttonTime"))
            #self._logger.info("Setting up GPIO %s" %buttonGPIO)
            GPIO.setup(buttonGPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            if buttonMode == "Normally Open (NO)" :
                GPIO.add_event_detect(buttonGPIO, GPIO.FALLING, callback=self.reactToInput)
            if buttonMode == "Normally Closed (NC)" :
                GPIO.add_event_detect(buttonGPIO, GPIO.RISING, callback=self.reactToInput)
            self._logger.info("Saved buttons have been initialized")

    def on_shutdown(self):
        self._logger.info("Cleaning up used GPIOs before shutting down ...")
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        for button in self._settings.get(["buttons"]):
            GPIO.remove_event_detect(int(button.get("gpio")))

    def on_settings_save(self, data):
        GPIO.setmode(GPIO.BCM)
        ##Handle old configuration (remove old interrupts)
        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            #self._logger.info("Removed event detect for button %s" %button.get("buttonname"))
            GPIO.remove_event_detect(buttonGPIO)
            GPIO.cleanup(buttonGPIO)

        ##Save new settings
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        ##Handle new configuration
        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            buttonMode = button.get("buttonMode")
            buttonTime = int(button.get("buttonTime"))
            GPIO.setup(buttonGPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            if buttonMode == "Normally Open (NO)" :
                GPIO.add_event_detect(buttonGPIO, GPIO.FALLING, callback=self.reactToInput, bouncetime=buttonTime)
            if buttonMode == "Normally Closed (NC)" :
                GPIO.add_event_detect(buttonGPIO, GPIO.RISING, callback=self.reactToInput, bounceTime=buttonTime)

    def get_settings_defaults(self):
        return dict(
            buttons = []
        )

	##~~ Softwareupdate hook
    def get_update_information(self):
        return dict(
        physicalbutton = dict(
        displayName = "Physical Button",
        displayVersion = self._plugin_version,
        type = "github_release",
        user = "LuxuSam",
        repo = "PhysicalButton",
        current = self._plugin_version,
        pip = "https://github.com/LuxuSam/PhysicalButton/archive/{target_version}.zip"
        )
        )


    def get_template_configs(self):
        return [
            dict(type = "settings", custom_bindings = True)
        ]

    def get_assets(self):
        return dict(js=["js/physicalbutton.js"])

    def reactToInput(self, channel):
        reactButtons = []
        #get triggered buttons
        for button in self._settings.get(["buttons"]):
            if int(button.get("gpio")) == channel:
                reactButtons.append(button)

        #debounce button / wait until active
        timePressedButton = time.time()
        buttonState = GPIO.input(channel)
        bounceTime = int(button.get("buttonTime"))
        while (time.time()*1000 < timePressedButton*1000 + bounceTime):
            pass

        if (buttonState != GPIO.input(channel)):
            return

        #execute activity specified by triggered buttons
        for button in reactButtons:
            if button.get("show") == "action" :
                #send specified action
                self.sendAction(button.get("action"))

            if button.get("show") == "gcode" :
                #split gcode lines in single commands without comment and add to list
                commandList = []
                for temp in button.get("gcode").splitlines():
                    commandList.append(temp.split(";")[0].strip())
                #send commandList to printer
                self.sendGcode(commandList)


    def sendGcode(self, gcodeCommand):
        self._printer.commands(gcodeCommand, force = False)

    def sendAction(self, action):
        if action == "cancel":
            self._printer.cancel_print()
            return
        if action ==  "connect":
            self._printer.connect()
            return
        if action ==  "disconnect":
            self._printer.disconnect()
            return
        if action ==  "home":
            self._printer.home(["x","y","z"])
            return
        if action ==  "pause":
            self._printer.pause_print()
            return
        if action ==  "resume":
            self._printer.resume_print()
            return
        if action ==  "start":
            self._printer.start_print()
            return
        self._logger.info("No action selected or action (yet) unknown")


__plugin_name__ = "Physical Button"
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PhysicalbuttonPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
