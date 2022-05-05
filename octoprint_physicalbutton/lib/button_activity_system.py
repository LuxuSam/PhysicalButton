import subprocess


def run_system(printer, commands):
    # split commands lines and execute one by one, unless there is an error
    for command in commands.splitlines():
        printer._logger.info(f"Executing system command '{command}'")

        try:
            # send command to Pi
            ret = subprocess.check_output(command,
                                          stderr=subprocess.STDOUT, shell=True, executable='/bin/bash')
            # log output
            printer._logger.info(f"Command '{command}' returned: {ret.decode('utf-8')}")
            return 0
        except subprocess.CalledProcessError as e:
            # return exception and stop further processing
            printer._logger.error(f"Error [{e.returncode}] executing command '{command}': {e.output.decode('utf-8')}")
            return -1