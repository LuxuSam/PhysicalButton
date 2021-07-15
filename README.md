# 🎛 Physical Button 🎛

The **PhysicalButton** plugin (hence the name) lets you add physical buttons to your Raspberry Pi.
The buttons are then able to send GCODE and actions to your printer.

---
## Setup
Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/LuxuSam/PhysicalButton/archive/master.zip

The Buttons have to be plugged in to a ground pin and the desired GPIO Pin that you want to use.
The GPIO must be chosen in BCM mode (see <https://pinout.xyz/>).
If you have other plugins installed that use GPIOs, make sure those plugins are also set to BCM mode.

---
## 🔧 Configuration 🔧
To add a new button you have to click on the ➕. This adds a new button to the end of your list.

From there you should enter a button name, the used GPIO and the mode (NO or NC) of the button.
In addition you have to specify for how long a button has to be held in order to trigger.

The last step is to add activities to your button which are executed in order of the activities list.
You can edit, move or remove activities in the right pane.

### More details for the button setup:
* **Button Name**
  * This is where you put the name of your button to differentiate them in the list of buttons.
* **GPIO**
  * This is the GPIO you connect your button to, the other cable has to be connected to a ground pin. Buttons are configured to use internal pulled-up resistors.
* **Mode**
  * Depending on your button setup or wiring you have to choose between the two modes.
  * Normally Open (NO)
    * Use this mode if your button is usually not pressed (open).
  * Normally Closed (NC)
    * Use this mode if your button is usually pressed (closed).
* **Hold Time**
  * This is where you set the hold time for your button, this means how long the button has to be held until the reaction is triggered.
* **Choose activities for your button**
  * Action:
    * You can choose between the standard actions of OctoPrint (cancel, connect, disconnect, home (x, y and z are homed), pause, resume and start).
  * GCODE:
    * You can input any GCODE.
  * These activities will be executed in order of your list. You can also rearrange them by inserting them at your desired position.

### Note:
You can only configure one button per GPIO.
If you want more activities to be activated upon button press (/release), add more activities to the button.

---
## Screenshots
![Action activity](/assets/img/plugins/physicalbutton/PhysicalButton_action.png)</br></br>
![GCODE activity](/assets/img/plugins/physicalbutton/PhysicalButton_gcode.png)</br></br>
![Delete Button](/assets/img/plugins/physicalbutton/PhysicalButton_delete.png)

---
## Get Help / Feature request
If you encounter problems using the plugin or if you have an idea for a new feature please use the [issue tracker](https://github.com/LuxuSam/PhysicalButton/issues) and if applicable add the corresponding label.

---
## ⚠️ Use at your own risk ⚠️
I am not accountable for any damages made to your printer/raspberry pi when using this plugin (e.g. wrong wiring
of buttons, GCODE commands that you send with the buttons to your printer, ...).

When setting the plugin up corresponding to my instructions, nothing should happen.

---
## ❤️ Support me ❤️
If you enjoy my plugin and want to support me and the development, you can do so by sending me a donation on</br>

[![paypal](https://www.paypalobjects.com/webstatic/de_DE/i/de-pp-logo-100px.png)](https://www.paypal.com/paypalme/luxusam3d)&emsp;&emsp;[![ko-fi](https://uploads-ssl.webflow.com/5c14e387dab576fe667689cf/5c91bddac6c3aa6b3718fd86_kofisvglofo.svg)](https://ko-fi.com/C0C14BZCR)
