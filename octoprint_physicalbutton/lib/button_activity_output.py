import threading
import time


def generate_output(printer, output):
    global output_list

    if output.get('gpio') == 'none':
        return -2

    gpio = int(output.get('gpio'))
    value = output.get('value')
    active_time = int(output.get('time'))

    output_device = next(iter(filter(lambda o_d: o_d.pin.number == gpio, output_list)))

    if output.get('async') == 'True':
        t = threading.Thread(target=printer.set_output, args=(value, active_time, output_device,))
        t.start()
    else:
        printer.set_output(value, active_time, output_device)
    return 0


def set_output(printer, value, active_time, output_device):
    if value == 'HIGH':
        output_device.on()
    elif value == 'LOW':
        output_device.off()
    elif value == 'Toggle':
        output_device.toggle()

    if active_time == 0:
        return
    else:
        time.sleep(active_time / 1000)

    output_device.toggle()
