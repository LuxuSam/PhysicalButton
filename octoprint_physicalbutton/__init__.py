# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from gpiozero import Button
import time
import threading

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
        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            buttonMode = button.get("buttonMode")
            newButton = Button(buttonGPIO, pull_up=True, bounce_time=None)
            if buttonMode == "Normally Open (NO)":
                newButton.when_pressed = self.reactToInput
            if buttonMode == "Normally Closed (NC)":
                newButton.when_released = self.reactToInput
            buttonList.append(newButton)

    def removeButtons(self):
        global buttonList
        for button in buttonList:
            button.close()
        buttonList.clear()

    def thread_react(self, pressedButton):
        #save value of button (pushed or released)
        buttonValue = pressedButton.value

        #search for pressed button
        for x in self._settings.get(["buttons"]):
            if int(x.get("gpio")) == pressedButton.pin.number:
                button = x
                break

        waitTime = int(button.get("buttonTime"))
        time.sleep(waitTime/1000)

        if pressedButton.value == buttonValue:
            self._logger.debug("Reacting to button: %s ..." %button.get("buttonname"))

            #execute actions for button in order
            for activity in button.get("activities"):
                if activity.get("type") == "action":
                    #send specified action
                    self.sendAction(button.get("execute"))
                if activity.get("type") == "gcode":
                    #send specified gcode
                    self.sendGcode(button.get("execute"))

    def reactToInput(self, pressedButton):
        t = threading.Thread(target=self.thread_react, args=(pressedButton,))
        t.start()

    def sendGcode(self, gcodetxt):
        #split gcode lines in single commands without comment and add to list
        commandList = []
        for temp in gcodetxt.splitlines():
            commandList.append(temp.split(";")[0].strip())
        #send commandList to printer
        self._printer.commands(commandList, force = False)

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
        self._logger.debug("No action selected or action (yet) unknown")
    ##################################################################################################

    def on_after_startup(self):
        if self._settings.get(["buttons"]) == None or self._settings.get(["buttons"]) == []:
            self._logger.debug("No buttons to initialize!")
            return
        self._logger.debug("Setting up buttons ...")
        self.setupButtons()
        self._logger.info("Buttons have been set up!")

    def on_shutdown(self):
        if self._settings.get(["buttons"]) == None or self._settings.get(["buttons"]) == []:
            self._logger.debug("No buttons to clean up ...")
            return
        self._logger.info("Cleaning up used GPIOs before shutting down ...")
        self.removeButtons()
        self._logger.info("Done!")

    def on_settings_save(self, data):
        #Handle old configuration:
        if self._settings.get(["buttons"]) != None and self._settings.get(["buttons"]) != []:
            self.removeButtons()
            self._logger.debug("Removed old button configuration")
        #Save new Settings
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        #Handle new configuration
        if self._settings.get(["buttons"]) != None and self._settings.get(["buttons"]) != []:
            self.setupButtons()
            self._logger.debug("Added new button configuration")

    def on_settings_cleanup(self):
        self.removeButtons()
        octoprint.plugin.SettingsPlugin.on_settings_cleanup()

    def get_settings_defaults(self):
        return dict(
            buttons = []
        )

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

__plugin_name__ = "Physical Button"
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PhysicalbuttonPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
	   "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
