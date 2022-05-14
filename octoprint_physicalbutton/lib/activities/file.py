import octoprint.plugin

from ... import button_globals as bg

def select_file(path):
    try:
        if not bg.plugin._printer.is_ready():
            bg.plugin._logger.error(f"Your machine is not ready to select a file!")
            return -1
        if '@sd:' in path:
            path = path.replace('@sd:', '').strip()
            bg.plugin._printer.select_file(path, True, printAfterSelect=False)
            bg.plugin._logger.debug(f"Selecting SD-file '{path}'")
        else:
            path = path.strip()
            bg.plugin._printer.select_file(path, False, printAfterSelect=False)
            bg.plugin._logger.debug(f"Selecting file '{path}'")
        return 0
    except (octoprint.printer.InvalidFileType, octoprint.printer.InvalidFileLocation) as e:
        bg.plugin._logger.error(e)
        return -1
