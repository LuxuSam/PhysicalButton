import octoprint.plugin


def select_file(printer, path):
    try:
        if not printer._printer.is_ready():
            printer._logger.error(f"Your machine is not ready to select a file!")
            return -1
        if '@sd:' in path:
            path = path.replace('@sd:', '').strip()
            printer._printer.select_file(path, True, printAfterSelect=False)
            printer._logger.debug(f"Selecting SD-file '{path}'")
        else:
            path = path.strip()
            printer._printer.select_file(path, False, printAfterSelect=False)
            printer._logger.debug(f"Selecting file '{path}'")
        return 0
    except (octoprint.printer.InvalidFileType, octoprint.printer.InvalidFileLocation) as e:
        printer._logger.error(e)
        return -1
