# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
#import RPi.GPIO as GPIO

class PhysicalbuttonPlugin(octoprint.plugin.StartupPlugin,
                           octoprint.plugin.SettingsPlugin,
                           octoprint.plugin.TemplatePlugin,
                           octoprint.plugin.AssetPlugin
                           ):
    def on_after_startup(self):
        self._logger.info("Saved buttons have been initialized")

    def on_settings_save(self, data):
        ##Handle old configuration (remove old interrupts)
        self._logger.info("Old Button configuration:")
        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            #GPIO.remove_event_detect(buttonGPIO)

        ##Save new settings
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        ##Handle new configuration
        self._logger.info("New Button configuration:")
        for button in self._settings.get(["buttons"]):
            buttonGPIO = int(button.get("gpio"))
            buttonMode = button.get("buttonMode")
            buttonTime = int(button.get("buttonTime"))
            if buttonMode == "Normally Open (NO)" :
                #GPIO.add_event_detect(buttonGPIO, GPIO.RISING, callback=self.reactToInput(buttonGPIO), bouncetime = buttonTime)
                self._logger.info("added (NO) button for gpio%s with buttontime : %s" %(buttonGPIO,buttonTime))
            if buttonMode == "Normally Closed (NC)" :
                #GPIO.add_event_detect(buttonGPIO, GPIO.RISING, callback=self.reactToInput(buttonGPIO), bouncetime = buttonTime)
                self._logger.info("added (NC) button for gpio%s with buttontime : %s" %(buttonGPIO,buttonTime))


        self.reactToInput(2)
        self._logger.info("Saved and initialized new button settings")

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

        #execute activity specified by triggered buttons
        for button in reactButtons:
            if button.get("show") == "action" :
                action = button.get("action")
                self._logger.info(action)
            else :
                gcode = button.get("gcode")
                self._logger.info(gcode)





__plugin_name__ = "Physical Button"
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PhysicalbuttonPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
