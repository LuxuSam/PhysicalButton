# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class PhysicalbuttonPlugin(octoprint.plugin.SettingsPlugin,
                           octoprint.plugin.AssetPlugin,
                           octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin
	#def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
	#	return dict(
	#		js=["js/physicalbutton.js"],
	#		css=["css/physicalbutton.css"],
	#		less=["less/physicalbutton.less"]
	#	)

	##~~ Softwareupdate hook
	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			physicalbutton=dict(
				displayName="Physicalbutton Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="LuxuSam",
				repo="PhysicalButton",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/LuxuSam/PhysicalButton/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "Physicalbutton Plugin"

__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PhysicalbuttonPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
