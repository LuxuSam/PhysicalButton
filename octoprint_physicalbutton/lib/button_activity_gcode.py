
def send_gcode(printer, gcode_txt):
    if not printer._printer.is_operational():
        printer._logger.error(f"Your machine is not operational!")
        return -1
    # split gcode lines in single commands without comment and add to list
    command_list = []
    for temp in gcode_txt.splitlines():
        command_list.append(temp.split(";")[0].strip())
    # send commandList to printer
    printer._printer.commands(command_list, force=False)
    return 0
