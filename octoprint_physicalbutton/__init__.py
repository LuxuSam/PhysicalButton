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
        NO = []
        NC = []
        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            buttonMode = button.get("buttonMode")
            buttonTime = int(button.get("buttonTime"))
            GPIO.setup(buttonGPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            if buttonMode == "Normally Open (NO)" and buttonGPIO not in NO:
                GPIO.add_event_detect(buttonGPIO, GPIO.FALLING, callback=self.reactToInput, bouncetime=buttonTime)
                NO.append(buttonGPIO)
            if buttonMode == "Normally Closed (NC)" and buttonGPIO not in NC :
                GPIO.add_event_detect(buttonGPIO, GPIO.RISING, callback=self.reactToInput, bouncetime=buttonTime)
                NC.append(buttonGPIO)
        NO.clear()
        NC.clear()
        self._logger.info("Buttons have been set up!")


    def on_shutdown(self):
        self._logger.info("Cleaning up used GPIOs before shutting down ...")
        GPIO.setmode(GPIO.BCM)
        for button in self._settings.get(["buttons"]):
            GPIO.remove_event_detect(int(button.get("gpio")))
        GPIO.cleanup()
        self._logger.info("Done!")


    def on_settings_save(self, data):
        GPIO.setmode(GPIO.BCM)

        ##Handle old configuration (remove old interrupts)
        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            GPIO.remove_event_detect(buttonGPIO)
            GPIO.cleanup(buttonGPIO)
        self._logger.info("Removed old button configuration")

        ##Save new settings
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        ##Handle new configuration
        NO = []
        NC = []
        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            buttonMode = button.get("buttonMode")
            buttonTime = int(button.get("buttonTime"))
            GPIO.setup(buttonGPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            if buttonMode == "Normally Open (NO)" and buttonGPIO not in NO:
                GPIO.add_event_detect(buttonGPIO, GPIO.FALLING, callback=self.reactToInput, bouncetime=buttonTime)
                NO.append(buttonGPIO)
            if buttonMode == "Normally Closed (NC)" and buttonGPIO not in NC :
                GPIO.add_event_detect(buttonGPIO, GPIO.RISING, callback=self.reactToInput, bouncetime=buttonTime)
                NC.append(buttonGPIO)
        NO.clear()
        NC.clear()
        self._logger.info("Added new button configuration")


    def get_settings_defaults(self):
        return dict(
            buttons = []
        )


	##~~ Softwareupdate hook
    def get_update_information(self):
        return {
            "physicalbutton": {
                "displayName" : "Physical Button",
                "displayVersion" : self._plugin_version,
                "type" : "github_release",
                "user" : "LuxuSam",
                "repo" : "PhysicalButton",
                "current" : self._plugin_version,
                "pip" : "https://github.com/LuxuSam/PhysicalButton/archive/{target_version}.zip",
                "stable_branch": {
                    "name": "Stable",
                    "branch": "master",
                    "comittish": ["master"],
                },
                "prerelease_branches": [
                    {
                        "name": "Development Releases",
                        "branch": "development",
                        "comittish": ["development", "master"],
                    }
                ]
            }
        }


    def get_template_configs(self):
        return [
            dict(type = "settings", custom_bindings = True)
        ]


    def get_assets(self):
        return dict(js=["js/physicalbutton.js"])


    def reactToInput(self, channel):
        #remove event detect so callback is not called more than once at a time
        GPIO.remove_event_detect(channel)

        if GPIO.input(channel) == 1:
            rising = True
        else:
            rising = False

        #get triggered buttons
        reactButtons = []
        for button in self._settings.get(["buttons"]):
            if int(button.get("gpio")) == channel:
                #add button for corresponding edge detection
                if rising and button.get("buttonMode") == "Normally Closed (NC)":
                    reactButtons.append(button)
                if not rising and button.get("buttonMode") == "Normally Open (NO)":
                    reactButtons.append(button)
        #debounce button / wait until active
        button = reactButtons[0]
        bounceTime = int(button.get("buttonTime"))

        buttonState = 0
        if button.get("buttonMode") == "Normally Open (NO)":
            buttonState = 0
        else:
            buttonState = 1
        react = False

        #Wait time specified by user until recheck the button state
        time.sleep(bounceTime/1000)
        if GPIO.input(channel) == buttonState:
            react = True


        #execute activity specified by triggered buttons
        if react:
            for button in reactButtons:
                self._logger.info("Reacting to button: %s ..." %button.get("buttonname"))
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

                #Give user time to release button again
                time.sleep(0.75)

        #re-add event detect so callback can be called again
        if buttonState == 0:
            GPIO.add_event_detect(channel, GPIO.FALLING, callback=self.reactToInput, bouncetime=bounceTime)
        else:
            GPIO.add_event_detect(channel, GPIO.RISING, callback=self.reactToInput, bouncetime=bounceTime)


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
