# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from gpiozero import Button
import time

buttonList = []

class PhysicalbuttonPlugin(octoprint.plugin.StartupPlugin,
                           octoprint.plugin.SettingsPlugin,
                           octoprint.plugin.TemplatePlugin,
                           octoprint.plugin.AssetPlugin,
                           octoprint.plugin.ShutdownPlugin
                           ):

    ######################################## Helper functions ########################################
    def setupButtons(self):
        global buttonList
        for button in for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            existsAlready = bool(filter(lambda button: button.pin.number() == buttonGPIO, buttonList))
            if existsAlready:
                continue
            buttonMode = button.get("buttonMode")
            buttonTime = int(button.get("buttonTime"))
            newButton = Button(buttonGPIO, pull_up=True, bounce_time=0.05,hold_repeat=False,hold_time=0)
            if buttonMode == "Normally Open (NO)":
                newButton.when_pressed = reactToInput(newButton.pin.number())
            if buttonMode == "Normally Closed (NC)":
                newButton.when_released = reactToInput(newButton.pin.number())
            buttonList.append(newButton)
    def removeButtons(self):
        global buttonList
        for button in buttonList:
            if not button.closed():
                button.close()
        buttonList.clear()
    ##################################################################################################


    def on_after_startup(self):
        if self._settings.get(["buttons"]) == None or self._settings.get(["buttons"]) == []:
            self._logger.info("No buttons to initialize!")
            return
        self._logger.info("Setting up buttons ...")
        self.setupButtons()
        self._logger.info("Buttons have been set up!")

    def on_shutdown(self):
        if self._settings.get(["buttons"]) == None or self._settings.get(["buttons"]) == []:
            self._logger.info("No buttons to clean up ...")
            return
        self._logger.info("Cleaning up used GPIOs before shutting down ...")
        self.removeButtons()
        self._logger.info("Done!")

    def on_settings_save(self, data):
        #Handle old configuration:
        if self._settings.get(["buttons"]) != None and self._settings.get(["buttons"]) != []:
            self.removeButtons()
            self._logger.info("Removed old button configuration")
        #Save new Settings
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        #Handle new configuration
        if self._settings.get(["buttons"]) != None and self._settings.get(["buttons"]) != []:
            self.setupButtons()
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


    def reactToInput(self, pressedButton):
        #Filter which buttons have to react
        if pressedButton.is_pressed():
            reactButtons = list(filter(lambda button: button.get("buttonMode") == "Normally Closed (NC)" and int(button.get("gpio")) == pressedButton.pin.number(), self._settings.get(["buttons"])))
        else:
            reactButtons = list(filter(lambda button: button.get("buttonMode") == "Normally Open (NO)" and int(button.get("gpio")) == pressedButton.pin.number(), self._settings.get(["buttons"])))
        button = reactButtons[0]
        waitTime = int(button.get("buttonTime"))

        if button.get("buttonMode") == "Normally Open (NO)":
            buttonState = 1
        else:
            buttonState = 0
            react = False

        #Wait time specified by user until recheck the button state
        time.sleep(waitTime/1000)
        if pressedButton.value() == buttonState:
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

    global callbackIsRunning
    callbackIsRunning = False
