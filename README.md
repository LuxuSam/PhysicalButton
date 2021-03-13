# Physical Button

The PhysicalButton Plugin lets you add physical buttons to your Raspberry Pi.
The buttons are then able to send GCODE or actions to your printer.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/LuxuSam/PhysicalButton/archive/master.zip

The Buttons have to be plugged in to a ground pin and the desired GPIO Pin that you want to use.


## Configuration
 To add a new button you have to click on the +.
 From there you must enter a button name, the used GPIO and the mode (NO or NC) of the button.
 In addition you have to specify a debounce time (or time after which the button activates)
 The last step is to either select Action or GCODE and then specify what should happen upon button activation

 After an initial save you can still set the button name, GPIO mode, debounce time and activity.
 You are not able to switch from action to GCODE or from GCODE to action anymore for that button
