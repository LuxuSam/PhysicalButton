# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

from . import button_globals as bg
from .lib.button_gpio_setup import setup_buttons, remove_buttons, remove_outputs
from .lib.button_helpers import register_button_actions

# Set this to true if not programming on raspberry pi
debug = True
if debug:
    import gpiozero
    from gpiozero.pins.mock import MockFactory

    gpiozero.Device.pin_factory = MockFactory()


class PhysicalbuttonPlugin(octoprint.plugin.AssetPlugin,
                           octoprint.plugin.EventHandlerPlugin,
                           octoprint.plugin.SettingsPlugin,
                           octoprint.plugin.ShutdownPlugin,
                           octoprint.plugin.StartupPlugin,
                           octoprint.plugin.TemplatePlugin
                           ):

    def on_event(self, event, payload):
        if event == "FileAdded":
            bg.latest_file_path = payload.get('path')
            self._logger.debug(f"Added new file: {bg.latest_file_path}")
        elif event == "ClientOpened" or event == "SettingsUpdated":
            registered_plugin_actions = {identifier: list(bg.registered_plugins[identifier].keys())
                                         for identifier in bg.registered_plugins}
            self._plugin_manager.send_plugin_message("physicalbutton", registered_plugin_actions)

    def on_after_startup(self):
        bg.plugin = self
        if self._settings.get(["buttons"]) is None or self._settings.get(["buttons"]) == []:
            self._logger.debug(f"No buttons to initialize!")
            return
        self._logger.debug(f"Setting up buttons ...")
        setup_buttons()
        self._logger.info(f"Buttons have been set up!")

    def on_shutdown(self):
        if self._settings.get(["buttons"]) is None or self._settings.get(["buttons"]) == []:
            self._logger.debug(f"No buttons to clean up ...")
            return
        self._logger.info(f"Cleaning up used GPIOs before shutting down ...")
        remove_buttons()
        remove_outputs()
        self._logger.info(f"Done!")

    def on_settings_save(self, data):
        # Handle old configuration:
        if self._settings.get(["buttons"]) is not None and self._settings.get(["buttons"]) != []:
            remove_buttons()
            remove_outputs()
            self._logger.debug(f"Removed old button configuration")
        # Save new Settings
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        # Handle new configuration
        if self._settings.get(["buttons"]) is not None and self._settings.get(["buttons"]) != []:
            setup_buttons()
            self._logger.debug(f"Added new button configuration")

    def on_settings_cleanup(self):
        remove_buttons()
        remove_outputs()
        octoprint.plugin.SettingsPlugin.on_settings_cleanup(self)

    def get_settings_defaults(self):
        return dict(
            buttons=[]
        )

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=True)
        ]

    def get_assets(self):
        return dict(
            js=["js/physicalbutton.js"],
            css=["css/physicalbutton.css"],
            less=["less/physicalbutton.less"]
        )

    # ~~ Softwareupdate hook
    def get_update_information(self):
        return {
            "physicalbutton": {
                "displayName": "Physical Button",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "user": "LuxuSam",
                "repo": "PhysicalButton",
                "current": self._plugin_version,
                "pip": "https://github.com/LuxuSam/PhysicalButton/archive/{target_version}.zip",
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
__plugin_pythoncompat__ = ">=3,<4"  # python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PhysicalbuttonPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

    global __plugin_helpers__
    __plugin_helpers__ = dict(
        register_button_actions=register_button_actions
    )
