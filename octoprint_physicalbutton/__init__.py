# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class PhysicalbuttonPlugin(octoprint.plugin.StartupPlugin,
                           octoprint.plugin.SettingsPlugin,
                           octoprint.plugin.TemplatePlugin):
    def on_after_startup(self):
        self._logger.info("Physical Button plugin started")


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
            dict(type="settings", custom_bindings=False)
        ]

    def get_template_vars(self):
        return dict(buttonname=self._settings.get(["buttonname"]))

    


__plugin_name__ = "Physical Button"
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PhysicalbuttonPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
