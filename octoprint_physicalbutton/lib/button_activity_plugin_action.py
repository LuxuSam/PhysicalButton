from .. import button_globals as bg


def send_plugin_action(plugin_action):
    identifier = plugin_action.get('plugin')
    action = plugin_action.get('action')
    if identifier not in bg.plugin._plugin_manager.plugins:
        bg.plugin._logger.error(f"The plugin with identifier {identifier} is not installed!")
        return -1
    if not bg.plugin._plugin_manager.get_plugin_info(identifier):
        bg.plugin._logger.error(f"The plugin with identifier {identifier} is not enabled!")
        return -1
    if identifier not in bg.registered_plugins:
        bg.plugin._logger.error(f"The plugin with identifier {identifier} has no registered actions!")
        return -1
    if action not in bg.registered_plugins[identifier]:
        bg.plugin._logger.error(f"The plugin with identifier {identifier} did not register that action!")
        return -1
    bg.registered_plugins[identifier][action]()
