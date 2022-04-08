# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

from gpiozero import Button,OutputDevice


# Set this to true if not programming on raspberry pi
debug = False
if debug:
    import gpiozero
    from gpiozero.pins.mock import MockFactory
    gpiozero.Device.pin_factory = MockFactory()

import time
import threading
import subprocess

buttonList = []
outputList = []
latestFilePath = None
sup_inst_plugins = {
    'installed': {},                        # identifier : [possible actions]
    'supported': {'SimplyPrint': '3.1.2',       # identifier : minimal version
                  }
}


class PhysicalbuttonPlugin(octoprint.plugin.AssetPlugin,
                           octoprint.plugin.EventHandlerPlugin,
                           octoprint.plugin.SettingsPlugin,
                           octoprint.plugin.ShutdownPlugin,
                           octoprint.plugin.StartupPlugin,
                           octoprint.plugin.TemplatePlugin
                           ):

    ##################################################################################################
    ########################################_GPIO Setup functions_####################################
    ##################################################################################################
    def setupButtons(self):
        global buttonList
        for button in self._settings.get(["buttons"]):
            if button.get('gpio') == "none":
                continue
            buttonGPIO = int(button.get('gpio'))
            buttonMode = button.get('buttonMode')
            newButton = Button(buttonGPIO, pull_up=True, bounce_time=None)
            if buttonMode == "Normally Open (NO)":
                newButton.when_pressed = self.reactToInput
            if buttonMode == "Normally Closed (NC)":
                newButton.when_released = self.reactToInput
            buttonList.append(newButton)
            self.setupOutputPins(button)
        self._logger.debug(f"Added Buttons: {buttonList}")
        self._logger.debug(f"Added Output devices: {outputList}")

    def setupOutputPins(self,button):
        global outputList
        for activity in list(filter(lambda a: a.get('type') == "output", button.get('activities'))):
            outputGPIO = activity.get('execute').get('gpio')
            #check if gpio has to be setup
            if outputGPIO == 'none' or int(outputGPIO) in list(map(lambda oD: oD.pin.number, outputList)):
                continue
            outputDevice = OutputDevice(int(outputGPIO))
            initialValue = activity.get('execute').get('initial')
            if initialValue == "HIGH":
                outputDevice.on()
            outputList.append(outputDevice)

    def removeButtons(self):
        global buttonList
        self._logger.debug(f"Buttons to remove: {buttonList}")
        for button in buttonList:
            button.close()
        buttonList.clear()

    def removeOutputs(self):
        global outputList
        self._logger.debug(f"Output devices to remove: {outputList}")
        for outputDevice in outputList:
            outputDevice.close()
        outputList.clear()

    ##################################################################################################
    ########################################_React to button_#########################################
    ##################################################################################################
    def thread_react(self, pressedButton):
        #save value of button (pushed or released)
        buttonValue = pressedButton.value

        #search for pressed button
        for btn in self._settings.get(["buttons"]):
            if btn.get('gpio') == "none":
                continue
            if int(btn.get('gpio')) == pressedButton.pin.number:
                button = btn
                break

        waitTime = int(button.get('buttonTime'))
        time.sleep(waitTime/1000)

        if pressedButton.value == buttonValue:
            self._logger.debug(f"Reacting to button {button.get('buttonName')}")
            # execute actions for button in order
            for activity in button.get('activities'):
                exitCode = 0
                self._logger.debug(f"Sending activity with identifier '{activity.get('identifier')}' ...")
                if activity.get('type') == "action":
                    #send specified action
                    exitCode = self.sendAction(activity.get('execute'))
                elif activity.get('type') == "gcode":
                    #send specified gcode
                    exitCode = self.sendGcode(activity.get('execute'))
                elif activity.get('type') == "system":
                    #send specified system
                    exitCode = self.runSystem(activity.get('execute'))
                elif activity.get('type') == "file":
                    #select the file at the given location
                    exitCode = self.selectFile(activity.get('execute'))
                elif activity.get('type') == "output":
                    #generate output for given amount of time
                    exitCode = self.generateOutput(activity.get('execute'))
                elif activity.type('type') == "plugin":
                    exitCode = self.sendPluginAction(activity.get('execute'))
                else:
                    self._logger.debug(f"The activity with identifier '{activity.get('identifier')}' is not known (yet)!")
                    continue
                # Check if an executed activity failed
                if exitCode == 0:
                    self._logger.debug(f"The activity with identifier '{activity.get('identifier')}' was executed successfully!")
                    continue
                if exitCode == -1:
                    self._logger.error(f"The activity with identifier '{activity.get('identifier')}' failed! Aborting follwing activities!")
                    break
                if exitCode == -2:
                    self._logger.error(f"The activity with identifier '{activity.get('identifier')}' failed! No GPIO specified!")
                    continue

    def reactToInput(self, pressedButton):
        t = threading.Thread(target=self.thread_react, args=(pressedButton,))
        t.start()

    ##################################################################################################
    ########################################_Activities_##############################################
    ##################################################################################################
    def sendGcode(self, gcodetxt):
        if not self._printer.is_operational():
            self._logger.error(f"Your machine is not operational!")
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
        if action == "start latest":
            return self.start_latest()
        if action == "cancel":
            self._printer.cancel_print()
            return 0
        if action == 'toggle start-cancel':
            return self.toggle_cancel_print()
        if action == 'toggle start latest-cancel':
            return self.toggle_cancel_start_latest()
        if action == 'unselect file':
            return self._printer.unselect_file()

        self._logger.debug(f"No action selected or action (yet) unknown")
        return 0

    def runSystem(self, commands):
        # split commands lines and execute one by one, unless there is an error
        for command in commands.splitlines():
            self._logger.info(f"Executing system command '{command}'")

            try:
                # send command to Pi
                ret = subprocess.check_output(command,
                    stderr=subprocess.STDOUT, shell=True)
                # log output
                self._logger.info(f"Command '{command}' returned: {ret.decode('utf-8')}")
                return 0
            except subprocess.CalledProcessError as e:
                # return exception and stop further processing
                self._logger.error(f"Error [{e.returncode}] executing command '{command}': {e.output.decode('utf-8')}")
                return -1

    def selectFile(self, path):
        try:
            if not self._printer.is_ready():
                self._logger.error(f"Your machine is not ready to select a file!")
                return -1
            if '@sd:' in path:
                path = path.replace('@sd:','').strip()
                self._printer.select_file(path, True, printAfterSelect = False)
                self._logger.debug(f"Selecting SD-file '{path}'")
            else:
                path = path.strip()
                self._printer.select_file(path, False, printAfterSelect = False)
                self._logger.debug(f"Selecting file '{path}'")
            return 0
        except (octoprint.printer.InvalidFileType, octoprint.printer.InvalidFileLocation) as e:
            self._logger.error(e)
            return -1

    def generateOutput(self, output):
        global outputList

        if output.get('gpio') == 'none':
            return -2

        gpio = int(output.get('gpio'))
        value = output.get('value')
        time = int(output.get('time'))

        outputDevice = next(iter(filter(lambda oD: oD.pin.number == gpio, outputList)))

        if output.get('async') == 'True':
            t = threading.Thread(target = self.setOutput, args=(value, time, outputDevice,))
            t.start()
        else:
            self.setOutput(value, time, outputDevice)
        return 0

    def sendPluginAction(self, plugin_action):
        plugin = plugin_action.get('plugin')
        action = plugin_action.get('action')
        if plugin not in self._plugin_manager.plugins:
            self._logger.error(f"The plugin with identifier {plugin} is not installed!")
            return -1
        plugin_info = self._plugin_manager.get_plugin_info(plugin)
        if not plugin_info.enabled:
            self._logger.error(f"The plugin with identifier {plugin} is not enabled!")
            return -1
        if not (plugin_info.version >= sup_inst_plugins.get('supported').get(plugin)):
            self._logger.error(f"The plugin with identifier {plugin} does not have minimal required version!")
            return -1

        # TODO: send specified action to plugin

    ##################################################################################################
    ########################################_Helper functions_########################################
    ##################################################################################################
    def updateLatestFilePath(self):
        global latestFilePath

        files = self._file_manager.list_files(recursive = True)
        localFileDict = self.getLatestPath(files.get('local'), None, -1)
        pathLocal = localFileDict.get('path')
        latestFilePath = pathLocal

    def getLatestPath(self, files, latestPath, latestDate):
        for file in files:
            file = files.get(file)
            if file.get('type') == "folder":
                fileDict = self.getLatestPath(file.get('children'), latestPath, latestDate)
                latestPath = fileDict.get('path')
                latestDate = fileDict.get('date')

            if file.get('type') == "machinecode":
                if file.get('date') > latestDate:
                    latestPath = file.get('path')
                    latestDate = file.get('date')

        return {
            "path" : latestPath,
            "date" : latestDate
        }

    def setOutput(self, value, activeTime, outputDevice):
        if value == 'HIGH':
            outputDevice.on()
        elif value == 'LOW':
            outputDevice.off()
        elif value == 'Toggle':
            outputDevice.toggle()

        if activeTime == 0:
            return
        else:
            time.sleep(activeTime/1000)

        outputDevice.toggle()

    def setup_for_installed_plugins(self):
        global sup_inst_plugins
        for plugin in sup_inst_plugins.get('supported').keys():
            if plugin not in self._plugin_manager.plugins:
                self._logger.debug(f"The plugin with identifier {plugin} is not installed!")
                continue
            plugin_info = self._plugin_manager.get_plugin_info(plugin)
            if not plugin_info:
                self._logger.debug(f"The plugin with identifier {plugin} is not enabled!")
                continue
            if not (plugin_info.version >= sup_inst_plugins.get('supported').get(plugin)):
                self._logger.debug(f"The plugin with identifier {plugin} does not have minimal required version!")
                continue
            self._logger.debug(f"{plugin} is supported. Setting up actions for {plugin}!")
            actions = []  # TODO: get actions of specified plugin
            sup_inst_plugins.get('installed')[plugin] = actions



    ##################################################################################################
    ########################################_Custom actions_##########################################
    ##################################################################################################
    def toggle_cancel_print(self):
        if self._printer.is_ready():
            self._printer.start_print()
        else:
            self._printer.cancel_print()
        return 0

    def start_latest(self):
        if (latestFilePath is None) or (not self._file_manager.file_exists("local",latestFilePath)):
            self._logger.debug(f"latestFilePath not set yet, start search")
            self.updateLatestFilePath()

        if latestFilePath is None:
            self._logger.error(f"No files found!")
            return -1

        if self.selectFile(latestFilePath) == -1:
            return -1

        self._printer.start_print()
        return 0

    def toggle_cancel_start_latest(self):
        if self._printer.is_ready():
            return self.start_latest()
        else:
            self._printer.cancel_print()
            return 0
    ##################################################################################################
    ########################################_OctoPrint Functions_#####################################
    ##################################################################################################
    def on_event(self, event, payload):
        if event == "FileAdded":
            global latestFilePath
            latestFilePath = payload.get('path')
            self._logger.debug(f"Added new file: {latestFilePath}")
        elif event == "ClientOpened":
            self._plugin_manager.send_plugin_message("physicalbutton", sup_inst_plugins.get('installed'))

    def on_after_startup(self):
        if self._settings.get(["buttons"]) == None or self._settings.get(["buttons"]) == []:
            self._logger.debug(f"No buttons to initialize!")
            return
        self._logger.debug(f"Setting up buttons ...")
        self.setupButtons()
        self._logger.info(f"Buttons have been set up!")

        self._logger.debug(f"Setup for third party plugins, if any are available")
        self.setup_for_installed_plugins()


    def on_shutdown(self):
        if self._settings.get(["buttons"]) == None or self._settings.get(["buttons"]) == []:
            self._logger.debug(f"No buttons to clean up ...")
            return
        self._logger.info(f"Cleaning up used GPIOs before shutting down ...")
        self.removeButtons()
        self.removeOutputs()
        self._logger.info(f"Done!")

    def on_settings_save(self, data):
        #Handle old configuration:
        if self._settings.get(["buttons"]) != None and self._settings.get(["buttons"]) != []:
            self.removeButtons()
            self.removeOutputs()
            self._logger.debug(f"Removed old button configuration")
        #Save new Settings
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        #Handle new configuration
        if self._settings.get(["buttons"]) != None and self._settings.get(["buttons"]) != []:
            self.setupButtons()
            self._logger.debug(f"Added new button configuration")

    def on_settings_cleanup(self):
        self.removeButtons()
        self.removeOutputs()
        octoprint.plugin.SettingsPlugin.on_settings_cleanup(self)

    def get_settings_defaults(self):
        return dict(
            buttons = [],
            installedSupportedPlugins = []
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
