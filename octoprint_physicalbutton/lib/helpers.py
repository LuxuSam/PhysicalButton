from .. import button_globals as bg


def register_button_actions(plugin_instance, action_callback):
    identifier = plugin_instance._identifier
    # has plugin already registered an action, if not initialize array and dictionary for plugin
    if identifier not in bg.registered_plugins:
        bg.registered_plugins[identifier] = {}

    for action in action_callback:
        if action not in bg.registered_plugins[identifier]:
            bg.registered_plugins[identifier][action] = action_callback[action]
            bg.plugin._logger.debug(f"{identifier} registered action: {action}.")
        else:
            bg.plugin._logger.error(f"{identifier} tried to register action {action}.")
            bg.plugin._logger.error(f"{action} is already registered for {identifier}!")
