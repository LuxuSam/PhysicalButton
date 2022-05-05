def register_button_actions(printer, plugin, action_callback):
    global registered_plugins

    identifier = plugin._identifier
    # has plugin already registered an action, if not initialize array and dictionary for plugin
    if identifier not in registered_plugins:
        registered_plugins[identifier] = {}

    for action in action_callback:
        if action not in registered_plugins[identifier]:
            registered_plugins[identifier][action] = action_callback[action]
            printer._logger.debug(f"{identifier} registered action: {action}.")
        else:
            printer._logger.error(f"{identifier} tried to register action {action}.")
            printer._logger.error(f"{action} is already registered for {identifier}!")