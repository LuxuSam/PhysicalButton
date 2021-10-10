# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

from gpiozero import Button
import time
import threading
import subprocess

buttonList = []
latestFilePath = None

class PhysicalbuttonPlugin(octoprint.plugin.AssetPlugin,
                           octoprint.plugin.EventHandlerPlugin,
                           octoprint.plugin.SettingsPlugin,
                           octoprint.plugin.ShutdownPlugin,
                           octoprint.plugin.StartupPlugin,
                           octoprint.plugin.TemplatePlugin
                           ):

    ########################################_Helper functions_########################################
    def setupButtons(self):
        global buttonList
        for button in self._settings.get(["buttons"]):
            if button.get("gpio") == "none":
                continue
            buttonGPIO = int(button.get("gpio"))
            buttonMode = button.get("buttonMode")
            newButton = Button(buttonGPIO, pull_up=True, bounce_time=None)
            if buttonMode == "Normally Open (NO)":
                newButton.when_pressed = self.reactToInput
            if buttonMode == "Normally Closed (NC)":
                newButton.when_released = self.reactToInput
            buttonList.append(newButton)
        self._logger.debug('Added Buttons: %s' %buttonList)

    def removeButtons(self):
        global buttonList
        self._logger.debug('Buttons to remove: %s' %buttonList)
        for button in buttonList:
            button.close()
        buttonList.clear()

    def thread_react(self, pressedButton):
        #save value of button (pushed or released)
        buttonValue = pressedButton.value

        #search for pressed button
        for btn in self._settings.get(["buttons"]):
            if btn.get("gpio") == "none":
                continue
            if int(btn.get("gpio")) == pressedButton.pin.number:
                button = btn
                break

        waitTime = int(button.get("buttonTime"))
        time.sleep(waitTime/1000)

        if pressedButton.value == buttonValue:
            self._logger.debug("Reacting to button %s:" %button.get("buttonName"))
            #execute actions for button in order
            for activity in button.get("activities"):
                exitCode = 0
                self._logger.debug("Sending activity with identifier '%s' ..." %activity.get("identifier"))
                if activity.get("type") == "action":
                    #send specified action
                    exitCode = self.sendAction(activity.get("execute"))
                if activity.get("type") == "gcode":
                    #send specified gcode
                    exitCode = self.sendGcode(activity.get("execute"))
                if activity.get("type") == "system":
                    #send specified system
                    exitCode = self.runSystem(activity.get("execute"))
                if activity.get("type") == "file":
                    #select the file at the given location
                    exitCode = self.selectFile(activity.get("execute"))
                #Check if an executed activity failed
                if exitCode == 0:
                    self._logger.debug("The activity with identifier '%s' was executed successfully!" %activity.get("identifier"))
                if exitCode == -1:
                    self._logger.error("The activity with identifier '%s' failed! Aborting follwing activities!" %activity.get("identifier") )
                    break

    def reactToInput(self, pressedButton):
        t = threading.Thread(target=self.thread_react, args=(pressedButton,))
        t.start()

    def sendGcode(self, gcodetxt):
        if not self._printer.is_operational():
            self._logger.error("Your machine is not operational!")
            return -1
        #split gcode lines in single commands without comment and add to list
        commandList = []
        for temp in gcodetxt.splitlines():
            commandList.append(temp.split(";")[0].strip())
        #send commandList to printer
        self._printer.commands(commandList, force = False)
        return 0

    def sendAction(self, action):
        if action == "connect":
            self._printer.connect()
            return 0
        if action == "disconnect":
            self._printer.disconnect()
            return 0
        if action == "home":
            self._printer.home(["x","y","z"])
            return 0
        if action == "pause":
            self._printer.pause_print()
            return 0
        if action == "resume":
            self._printer.resume_print()
            return 0
        if action == 'toggle pause-resume':
            self._printer.toggle_pause_print()
            return 0
        if action == "start":
            self._printer.start_print()
            return 0
        if action == "start newest":
            return self.start_newest()
        if action == "cancel":
            self._printer.cancel_print()
            return 0
        if action == 'toggle start-cancel':
            self.toggle_cancel_print()
            return 0
        self._logger.debug("No action selected or action (yet) unknown")
        return 0

    def runSystem(self, commands):
        # split commands lines and execute one by one, unless there is an error
        for command in commands.splitlines():
            self._logger.info("Executing system command '%s'" % (command))

            try:
                # send command to Pi
                ret = subprocess.check_output(command,
                    stderr=subprocess.STDOUT, shell=True)
                # log output
                self._logger.info("Command '%s' returned: %s" %
                    (command, ret.decode("utf-8")))
                return 0
            except subprocess.CalledProcessError as e:
                # return exception and stop further processing
                self._logger.error("Error [%d] executing command '%s': %s" %
                    (e.returncode, command, e.output.decode("utf-8")))
                return -1

    def selectFile(self, path):
        try:
            if not self._printer.is_ready():
                self._logger.error("Your machine is not ready to select a file!")
                return -1
            if '@sd:' in path:
                path = path.replace('@sd:','').strip()
                self._printer.select_file(path, True, printAfterSelect = False)
                self._logger.debug("Selecting SD-file '%s'" %path )
            else:
                path = path.strip()
                self._printer.select_file(path, False, printAfterSelect = False)
                self._logger.debug("Selecting file '%s'" %path )
            return 0
        except (octoprint.printer.InvalidFileType, octoprint.printer.InvalidFileLocation) as e:
            self._logger.error(e)
            return -1

    def updateLatestFilePath(self):
        global latestFilePath

        files = self._file_manager.list_files(recursive = True)
        localFileDict = self.getLatestPath(files.get("local"), None, 0)
        pathLocal = localFileDict.get("path")
        latestFilePath = pathLocal

    def getLatestPath(self, files, latestPath, latestDate):
        for file in files:
            file = files.get(file)
            if file.get("type") == "folder":
                fileDict = self.getLatestPath(file.get("children"), latestPath, latestDate)
                latestPath = fileDict.get("path")
                latestDate = fileDict.get("date")

            if file.get("type") == "machinecode":
                if file.get("date") > latestDate:
                    latestPath = file.get("path")
                    latestDate = file.get("date")

        return {
            "path" : latestPath,
            "date" : latestDate
        }

    ####################################_Custom actions_##############################################
    def toggle_cancel_print(self):
        if self._printer.is_ready():
            self._printer.start_print()
        else:
            self._printer.cancel_print()

    def start_newest(self):
        self._logger.debug("Start newest: test debug message")
        self._logger.debug("latestFilePath: %s" %latestFilePath)
        self._logger.debug("self._file_manager.file_exists(latestFilePath) = %s" %self._file_manager.file_exists(latestFilePath))
        if (latestFilePath is None) or (not self._file_manager.file_exists(latestFilePath)):
            self._logger.debug("latestFilePath not set yet, start search")
            self.updateLatestFilePath()

        if latestFilePath is None:
            self._logger.error('No files found!')
            return -1

        if self.selectFile(latestFilePath) == -1:
            return -1

        self._printer.start_print()
        return 0


    ####################################_OctoPrint Functions_#########################################
    def on_event(self, event, payload):
        if event == "FileAdded":
            global latestFilePath
            latestFilePath = payload.get("path")
            self._logger.debug("Added new file: %s" %latestFilePath)

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
        octoprint.plugin.SettingsPlugin.on_settings_cleanup(self)

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
__plugin_pythoncompat__ = ">=3,<4" # python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PhysicalbuttonPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
	   "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
