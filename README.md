# 🎛 Physical Button 🎛

The PhysicalButton Plugin (hence the name) lets you add physical buttons to your Raspberry Pi.
The buttons are then able to send GCODE or actions to your printer.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/LuxuSam/PhysicalButton/archive/master.zip

The Buttons have to be plugged in to a ground pin and the desired GPIO Pin that you want to use.
The GPIO must be chosen in BCM mode (see https://pinout.xyz/).
If you have other plugins installed that use GPIOs, make sure those plugins are also set to BCM mode.


## 🔧 Configuration 🔧
 To add a new button you have to click on the ➕.

 From there you must enter a button name, the used GPIO and the mode (NO or NC) of the button.

 In addition you have to specify for how long a button has to be held in order to trigger.
 The last step is to either select Action or GCODE and then specify what should happen upon button activation.

 After an initial save you can still set the button name, debounce time and activity.
 You are not able to switch from action to GCODE or from GCODE to action anymore for that button.

### Note:
 When you set up multiple "buttons" for one GPIO, only the hold time of the first created button is used.
 The specified GCODE commands or actions for the other "buttons" will be executed in order of your button list.

### ⚠️ Use at your own risk ⚠️
  I am not accountable for any damages made to your printer/raspberry pi when using this plugin (e.g. wrong wiring
  of buttons, GCODE commands that you send with the buttons to your printer, ...).


  When setting the plugin up corresponding to my instructions, nothing should happen.

# Get Help / Feature request

If you encounter problems using the plugin or if you have an idea for a new feature please use the [issue tracker](https://github.com/LuxuSam/PhysicalButton/issues) and if applicable add the corresponding label.

# ❤️ Support me ❤️

If you enjoy my plugin and want to support me and the development, you can do so by sending me a donation on</br>
[![paypal](https://www.paypalobjects.com/webstatic/de_DE/i/de-pp-logo-150px.png)](https://www.paypal.com/paypalme/luxusam3d)&emsp;&emsp;&emsp;&emsp;[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C14BZCR)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate?business=luxusam3d%40gmail.com&currency_code=EUR)
