# 🎛 Physical Button 🎛

The **PhysicalButton** plugin (hence the name) lets you add physical buttons to your Raspberry Pi.
The buttons are then able to send GCODE and actions to your printer.

---
## Setup
Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/LuxuSam/PhysicalButton/archive/master.zip

The buttons have to be plugged in to a ground pin and the desired GPIO pin that you want to use.
The GPIO must be chosen in BCM mode (see <https://pinout.xyz/>).
If you have other plugins installed that use GPIOs, make sure those plugins are also set to BCM mode.

---
## 🔧 Configuration - Overview 🔧
To add a new button you have to click on the ➕. This adds a new button to the end of your list.

From there you should enter a button name, the used GPIO and the mode (NO or NC) of the button.
In addition you have to specify for how long a button has to be held in order to trigger.

The last step is to add activities to your button which are executed in order of the activities list.
You can edit, move or remove activities in the right pane.

### 🔧 Configuration - Detail 🔧
* **Button Name**
  * This is where you put the name of your button to differentiate it in the list of buttons.
* **GPIO**
  * This is the GPIO you connect your button to. The other cable has to be connected to a ground pin (Buttons are configured to use internal pulled-up resistors).
* **Mode**
  * Depending on your button setup or wiring you have to choose between the following two modes:
    * Normally Open (NO)
      * Use this mode if your button is usually not pressed (open).
    * Normally Closed (NC)
      * Use this mode if your button is usually pressed (closed).
* **Hold Time**
  * This is where you set the hold time for your button, meaning how long the button has to be held until the reaction is triggered.
* **Choose activities for your button**
  * Action:
    * You can choose between different actions:
      * connect:
        * Connect to the printer.
      * disconnect
        * Disconnect from the printer.
      * home
        * Homes all axes of the printer.
      * pause
        * Pause the current print.
      * resume
        * Resume the current print.
      * start
        * Start printing the currently selected file.
      * start latest
        * Start printing the latest uploaded file.
      * cancel
        * Cancel the current print.
      * toggle pause-resume
        * Toggle between pausing and resuming a print.
      * toggle start-cancel
        * Toggle between starting the currently selected file or cancelling a print.
      * toggle start latest-cancel
        * Toggle between starting the latest uploaded file and cancelling a print.
      * unselect file
        * Unselect the currently selected file.
  * File:
    * You can specify the path to a file which will be selected.
    * To start the execution of a file, add 'start action' behind the 'file activity'.
    * There are three ways to specify a file:
      * Absolute path to a file:  
        `/home/pi/Some/Folder/Test.gcode`
      * Relative path to a file inside the uploads folder:  
        `Some/Folder/Test.gcode`
      * Path to a file on the SD-card of the printer:  
        `@sd:Some/Folder/Test.gcode`
  * GCODE:
    * You can input any GCODE commands.
  * System:
    * You can input any system command for your Octoprint host.  
    Note that system commands will be run under the same user that owns your OctoPrint service (usually 'pi' for OctoPi) with the same rights and permissions, so you may need to use sudo facilities for certain tasks. Please refer to your OctoPrint host's documentation for details.
  * Output:
    * Generate output on the given GPIO pin for a given amount of time.
    * By setting the time to 0, the output will continue until you toggle it again.
    * The async option lets the output run while also continuing with the next activities.
    * The initial value sets the level of the GPIO pin for startup and settings save.
  * Plugin:
    * This activity will appear if other plugins provide actions for this plugin.
  * These activities will be executed in order of your list. You can also rearrange them by inserting them at your desired position.

### Note:
You can only configure one button per GPIO.
If you want more activities to be activated upon button press (/release), add more activities to the button.

## Custom actions from your plugin:
If you are a developer and want to include functionality of your plugin into PhysicalButton, you can proceed as follows:

 * To get the function to register actions:
```python
helpers = self._plugin_manager.get_helpers("physicalbutton", "register_button_actions")
if helpers and "register_button_actions" in helpers:
    self.register_button_actions = helpers["register_button_actions"]
```

* To register actions use `self.register_button_actions(self, some_action_callback_dict)` with:
  * `some_action_callback_dict` being a dictionary with structure `{some_action : some_callback, ...}`.
    * `some_action` being a string with the name that should be displayed.
    * `some_callback` being a function without parameters that is executed on a button press.

---
## Screenshots
![Output activity](/assets/img/plugins/physicalbutton/PhysicalButton_output.png)</br></br>
![Action activity](/assets/img/plugins/physicalbutton/PhysicalButton_action.png)</br></br>
![GCODE activity](/assets/img/plugins/physicalbutton/PhysicalButton_gcode.png)</br></br>
![System activity](/assets/img/plugins/physicalbutton/PhysicalButton_system.png)</br></br>
![File activity](/assets/img/plugins/physicalbutton/PhysicalButton_file.png)</br></br>
![Delete Button](/assets/img/plugins/physicalbutton/PhysicalButton_delete.png)


---
## Get Help / Feature request
If you encounter problems using the plugin or if you have an idea for a new feature please use the [issue tracker](https://github.com/LuxuSam/PhysicalButton/issues) and if applicable add the corresponding label.

---
## ⚠️ Use at your own risk ⚠️
I am not accountable for any damages made to your printer/raspberry pi when using this plugin (e.g. wrong wiring
of buttons, GCODE or system commands that you send with the buttons to your printer, ...).

When setting the plugin up corresponding to my instructions, nothing should happen.

---
## ❤️ Support me ❤️
If you enjoy my plugin and want to support me and the development, you can do so by sending me a donation on</br>

[![paypal](https://www.paypalobjects.com/webstatic/de_DE/i/de-pp-logo-100px.png)](https://www.paypal.com/paypalme/luxusam3d)&emsp;&emsp;[![ko-fi](https://uploads-ssl.webflow.com/5c14e387dab576fe667689cf/5c91bddac6c3aa6b3718fd86_kofisvglofo.svg)](https://ko-fi.com/C0C14BZCR)
