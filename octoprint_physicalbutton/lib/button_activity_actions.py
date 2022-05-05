def send_action(printer, action):
    if action == "connect":
        printer._printer.connect()
        return 0
    elif action == "disconnect":
        printer._printer.disconnect()
        return 0
    elif action == "home":
        printer._printer.home(["x", "y", "z"])
        return 0
    elif action == "pause":
        printer._printer.pause_print()
        return 0
    elif action == "resume":
        printer._printer.resume_print()
        return 0
    elif action == 'toggle pause-resume':
        printer._printer.toggle_pause_print()
        return 0
    elif action == "start":
        printer._printer.start_print()
        return 0
    elif action == "start latest":
        return printer.start_latest()
    elif action == "cancel":
        printer._printer.cancel_print()
        return 0
    elif action == 'toggle start-cancel':
        return printer.toggle_cancel_print()
    elif action == 'toggle start latest-cancel':
        return printer.toggle_cancel_start_latest()
    elif action == 'unselect file':
        return printer._printer.unselect_file()

    printer._logger.debug(f"No action selected or action (yet) unknown")
    return 0


def toggle_cancel_print(printer):
    if printer._printer.is_ready():
        printer._printer.start_print()
    else:
        printer._printer.cancel_print()
    return 0


def start_latest(printer):
    if (latest_file_path is None) or (not printer._file_manager.file_exists("local", latest_file_path)):
        printer._logger.debug(f"latestFilePath not set yet, start search")
        printer.update_latest_file_path()

    if latest_file_path is None:
        printer._logger.error(f"No files found!")
        return -1

    if printer.selectFile(latest_file_path) == -1:
        return -1

    printer._printer.start_print()
    return 0


def toggle_cancel_start_latest(printer):
    if printer._printer.is_ready():
        return printer.start_latest()
    else:
        printer._printer.cancel_print()
        return 0


def update_latest_file_path(printer):
    global latest_file_path

    files = printer._file_manager.list_files(recursive=True)
    local_file_dict = printer.get_latest_path(files.get('local'), None, -1)
    path_local = local_file_dict.get('path')
    latest_file_path = path_local


def get_latest_path(printer, files, latest_path, latest_date):
    for file in files:
        file = files.get(file)
        if file.get('type') == "folder":
            file_dict = printer.get_latest_path(file.get('children'), latest_path, latest_date)
            latest_path = file_dict.get('path')
            latest_date = file_dict.get('date')

        if file.get('type') == "machinecode":
            if file.get('date') > latest_date:
                latest_path = file.get('path')
                latest_date = file.get('date')

    return {
        "path": latest_path,
        "date": latest_date
    }
