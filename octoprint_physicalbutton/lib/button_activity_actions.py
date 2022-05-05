from .. import button_globals as bg


def send_action(action):
    if action == "connect":
        bg.plugin._printer.connect()
        return 0
    elif action == "disconnect":
        bg.plugin._printer.disconnect()
        return 0
    elif action == "home":
        bg.plugin._printer.home(["x", "y", "z"])
        return 0
    elif action == "pause":
        bg.plugin._printer.pause_print()
        return 0
    elif action == "resume":
        bg.plugin._printer.resume_print()
        return 0
    elif action == 'toggle pause-resume':
        bg.plugin._printer.toggle_pause_print()
        return 0
    elif action == "start":
        bg.plugin._printer.start_print()
        return 0
    elif action == "cancel":
        bg.plugin._printer.cancel_print()
        return 0
    elif action == 'unselect file':
        bg.plugin._printer.unselect_file()
        return 0
    elif action == "start latest":
        return start_latest()
    elif action == 'toggle start-cancel':
        return toggle_cancel_print()
    elif action == 'toggle start latest-cancel':
        return toggle_cancel_start_latest()

    bg.plugin._logger.debug(f"No action selected or action (yet) unknown")
    return 0


def toggle_cancel_print():
    if bg.plugin._printer.is_ready():
        bg.plugin._printer.start_print()
    else:
        bg.plugin._printer.cancel_print()
    return 0


def start_latest():
    if (bg.latest_file_path is None) or (not bg.plugin._file_manager.file_exists("local", bg.latest_file_path)):
        bg.plugin._logger.debug(f"latest_file_path not set yet, start search")
        bg.plugin.update_latest_file_path()

    if bg.latest_file_path is None:
        bg.plugin._logger.error(f"No files found!")
        return -1

    if bg.plugin.selectFile(bg.latest_file_path) == -1:
        return -1

    bg.plugin._printer.start_print()
    return 0


def toggle_cancel_start_latest():
    if bg.plugin._printer.is_ready():
        return bg.plugin.start_latest()
    else:
        bg.plugin._printer.cancel_print()
        return 0


def update_latest_file_path():
    files = bg.plugin._file_manager.list_files(recursive=True)
    local_file_dict = get_latest_path(files.get('local'), None, -1)
    path_local = local_file_dict.get('path')

    bg.latest_file_path = path_local


def get_latest_path(files, latest_path, latest_date):
    for file in files:
        file = files.get(file)
        if file.get('type') == "folder":
            file_dict = get_latest_path(file.get('children'), latest_path, latest_date)
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
