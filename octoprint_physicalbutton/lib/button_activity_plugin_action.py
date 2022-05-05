
def send_plugin_action(self, plugin_action):
    identifier = plugin_action.get('plugin')
    action = plugin_action.get('action')
    if identifier not in self._plugin_manager.plugins:
        self._logger.error(f"The plugin with identifier {identifier} is not installed!")
        return -1
    if not self._plugin_manager.get_plugin_info(identifier):
        self._logger.error(f"The plugin with identifier {identifier} is not enabled!")
        return -1
    if identifier not in registered_plugins:
        self._logger.error(f"The plugin with identifier {identifier} has no registered actions!")
        return -1
    if action not in registered_plugins[identifier]:
        self._logger.error(f"The plugin with identifier {identifier} did not register that action!")
        return -1
    registered_plugins[identifier][action]()
