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
        alreadyAdded = []
        if self._settings.get(["buttons"]) == None or self._settings.get(["buttons"]) == []:
            self._logger.info("No buttons to initialize!")
            return

        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            if buttonGPIO in alreadyAdded:
                continue
            buttonMode = button.get("buttonMode")
            buttonTime = int(button.get("buttonTime"))
            GPIO.setup(buttonGPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            if buttonMode == "Normally Open (NO)":
                GPIO.add_event_detect(buttonGPIO, GPIO.FALLING, callback=self.reactToInput, bouncetime=100)
                alreadyAdded.append(buttonGPIO)
            if buttonMode == "Normally Closed (NC)":
                GPIO.add_event_detect(buttonGPIO, GPIO.RISING, callback=self.reactToInput, bouncetime=100)
                alreadyAdded.append(buttonGPIO)
        alreadyAdded.clear()
        self._logger.info("Buttons have been set up!")


    def on_shutdown(self):
        if self._settings.get(["buttons"]) == None or self._settings.get(["buttons"]) == []:
            self._logger.info("No buttons to clean up ...")
            return

        self._logger.info("Cleaning up used GPIOs before shutting down ...")
        GPIO.setmode(GPIO.BCM)
        alreadyRemoved = []
        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            if buttonGPIO not in alreadyRemoved:
                GPIO.remove_event_detect(buttonGPIO)
                alreadyRemoved.append(buttonGPIO)
        alreadyRemoved.clear()
        GPIO.cleanup()
        self._logger.info("Done!")


    def on_settings_save(self, data):
        GPIO.setmode(GPIO.BCM)

        if self._settings.get(["buttons"]) != None and self._settings.get(["buttons"]) != []:
            ##Handle old configuration (remove old interrupts)
            alreadyRemoved = []
            for button in self._settings.get(["buttons"]):
                buttonGPIO = int(button.get("gpio"))
                if buttonGPIO not in alreadyRemoved:
                    GPIO.remove_event_detect(buttonGPIO)
                    GPIO.cleanup(buttonGPIO)
                    alreadyRemoved.append(buttonGPIO)
            self._logger.info("Removed old button configuration")
            alreadyRemoved.clear()
                ##Save new settings
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        if self._settings.get(["buttons"]) != None and self._settings.get(["buttons"]) != []:
            ##Handle new configuration
            alreadyAdded = []
            for button in self._settings.get(["buttons"]):
                buttonGPIO = int(button.get("gpio"))
                if buttonGPIO in alreadyAdded:
                    continue
                buttonMode = button.get("buttonMode")
                buttonTime = int(button.get("buttonTime"))
                GPIO.setup(buttonGPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                if buttonMode == "Normally Open (NO)" and buttonGPIO not in alreadyAdded:
                    GPIO.add_event_detect(buttonGPIO, GPIO.FALLING, callback=self.reactToInput, bouncetime=100)
                    alreadyAdded.append(buttonGPIO)
                if buttonMode == "Normally Closed (NC)" and buttonGPIO not in alreadyAdded :
                    GPIO.add_event_detect(buttonGPIO, GPIO.RISING, callback=self.reactToInput, bouncetime=100)
                    alreadyAdded.append(buttonGPIO)
            alreadyAdded.clear()
            self._logger.info("Added new button configuration")


    def get_settings_defaults(self):
        return dict(
            buttons = [],
            debug = False
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
        return dict(
            js=["js/physicalbutton.js"],
            css=["css/physicalbutton.css"],
            less=["less/physicalbutton.less"]
        )


    def reactToInput(self, channel):
        #remove event detect so callback is not called more than once at a time
        GPIO.remove_event_detect(channel)

        if GPIO.input(channel) == 1:
            rising = True
            reactButtons = list(filter(lambda button: button.get("buttonMode") == "Normally Closed (NC)", self._settings.get(["buttons"])))
        else:
            rising = False
            reactButtons = list(filter(lambda button: button.get("buttonMode") == "Normally Open (NO)", self._settings.get(["buttons"])))

        #debounce button / wait until active
        if not reactButtons:
            if rising:
                GPIO.add_event_detect(channel, GPIO.RISING, callback=self.reactToInput, bouncetime=100)
            else:
                GPIO.add_event_detect(channel, GPIO.FALLING, callback=self.reactToInput, bouncetime=100)
            return

        button = reactButtons[0]
        bounceTime = int(button.get("buttonTime"))

        if button.get("buttonMode") == "Normally Open (NO)":
            buttonState = 0
            eventDetectMode = GPIO.FALLING
        else:
            buttonState = 1
            eventDetectMode = GPIO.RISING
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
        GPIO.add_event_detect(channel, eventDetectMode, callback=self.reactToInput, bouncetime=100)


    def sendGcode(self, gcodeCommand):
        self._printer.commands(gcodeCommand, force = False)


    def sendAction(self, action):
        if action == "cancel":
            self._printer.cancel_print()
            return
        if action == "connect":
            self._printer.connect()
            return
        if action == "disconnect":
            self._printer.disconnect()
            return
        if action == "home":
            self._printer.home(["x","y","z"])
            return
        if action == "pause":
            self._printer.pause_print()
            return
        if action == "resume":
            self._printer.resume_print()
            return
        if action == "start":
            self._printer.start_print()
            return
        if action == "debug":
            self._logger.info("This is a debug message for testing purposes!")
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
