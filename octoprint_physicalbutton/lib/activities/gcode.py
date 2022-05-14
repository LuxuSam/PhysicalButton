from ... import button_globals as bg

def send_gcode(gcode_txt):
    if not bg.plugin._printer.is_operational():
        bg.plugin._logger.error(f"Your machine is not operational!")
        return -1
    # split gcode lines in single commands without comment and add to list
    command_list = []
    for temp in gcode_txt.splitlines():
        command_list.append(temp.split(";")[0].strip())
    # send commandList to printer
    bg.plugin._printer.commands(command_list, force=False)
    return 0
