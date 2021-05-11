---
layout: plugin

id: physicalbutton
title: Physical Button
description: Add physical buttons to your octoprint
authors:
- LuxuSam
license: AGPLv3

# TODO
date: today's date in format YYYY-MM-DD, e.g. 2015-04-21

homepage: https://github.com/LuxuSam/PhysicalButton
source: https://github.com/LuxuSam/PhysicalButton
archive: https://github.com/LuxuSam/PhysicalButton/archive/master.zip

# TODO
# Set this to true if your plugin uses the dependency_links setup parameter to include
# library versions not yet published on PyPi. SHOULD ONLY BE USED IF THERE IS NO OTHER OPTION!
#follow_dependency_links: false

# TODO
tags:
- physical
- button
- buttons
- gpio
- pins
- external
- send
- action
- actions
- gcode


# TODO
screenshots:
- url: url of a screenshot, /assets/img/...
  alt: alt-text of a screenshot
  caption: caption of a screenshot
- url: url of another screenshot, /assets/img/...
  alt: alt-text of another screenshot
  caption: caption of another screenshot
- ...

# TODO
featuredimage: url of a featured image for your plugin, /assets/img/...

# TODO
# You only need the following if your plugin requires specific OctoPrint versions or
# specific operating systems to function - you can safely remove the whole
# "compatibility" block if this is not the case.

compatibility:

  # List of compatible versions
  #
  # A single version number will be interpretated as a minimum version requirement,
  # e.g. "1.3.1" will show the plugin as compatible to OctoPrint versions 1.3.1 and up.
  # More sophisticated version requirements can be modelled too by using PEP440
  # compatible version specifiers.
  #
  # You can also remove the whole "octoprint" block. Removing it will default to all
  # OctoPrint versions being supported.

  #octoprint:
  #- 1.2.0

  # List of compatible operating systems
  #
  # Valid values:
  #
  # - windows
  # - linux
  # - macos
  # - freebsd
  #
  # There are also two OS groups defined that get expanded on usage:
  #
  # - posix: linux, macos and freebsd
  # - nix: linux and freebsd
  #
  # You can also remove the whole "os" block. Removing it will default to all
  # operating systems being supported.

  os:
  - linux
  - windows
  - macos
  - freebsd

  # Compatible Python version
  #
  # Plugins should aim for compatibility for Python 2 and 3 for now, in which case the value should be ">=2.7,<4".
  #
  # Plugins that only wish to support Python 3 should set it to ">=3,<4".
  #
  # If your plugin only supports Python 2 (worst case, not recommended for newly developed plugins since Python 2
  # is EOL), leave at ">=2.7,<3" - be aware that your plugin will not be allowed to register on the
  # plugin repository if it only support Python 2.

  python: ">=2.7,<4"

---

# 🎛 Physical Button 🎛

The PhysicalButton Plugin (hence the name) lets you add physical buttons to your Raspberry Pi.
The buttons are then able to send GCODE or actions to your printer.

- - - -
## Screenshots
<p align="middle">
  <img src="/assets/img/NewGcodeButton.png" width="49%"/>
  <img src="/assets/img/NewActionButton.png" width="49%"/>
  <img src="/assets/img/ListButtons.png" width="49%"/>
  <img src="/assets/img/ButtonList2.png" width="49%"/>
</p>

- - - -
## Settings
* **Button Name**
  * This is where you put the name of your button to differentiate them in the list of buttons
* **GPIO**
  * This is the gpio you connect your button to, the other cable has to be connected to a ground pin (Buttons are configured to use internal pulled-up resistors)
* **Mode**
  * Depending on your button setup you have to choose between the two modes  
  * Normally Open (NO)
    * Use this mode if your button is normally not pressed (open)
  * Normally Closed (NC)
    * Use this mode if your button is normally pressed (closed)
* **Debounce Time / Time until active**
  * This is where you set the debounce time for your button if you want the button to react immedieatly on press
  * or when you the button to activate after having pressed the button for the inputed amount of time
* **Choose an activity for your button**
  * Action:
    * You can choose between the standard actions of octoprint (cancel, connect, disconnect, home ( x,y,z are homed), pause, resume and start)
  * Gcode:
    * You can input any GCODE

- - - -
### ⚠️ Use at your own risk ⚠️
  I am not accountable for any damages made to your printer/raspberry pi when using this plugin (e.g. wrong wiring
  of buttons, GCODE commands that you send with the buttons to your printer, ...).

- - - -
## Get Help / Feature request

If you encounter problems using the plugin or if you have an idea for a new feature please use the [issue tracker](https://github.com/LuxuSam/PhysicalButton/issues)

- - - -
# ❤️ Support me❤️

If you enjoy my plugin and want to support me and the development, you can do so by sending me a donation on

[![paypal](https://www.paypalobjects.com/webstatic/de_DE/i/de-pp-logo-150px.png)](https://www.paypal.com/paypalme/luxusam3d)&emsp;&emsp;&emsp;&emsp;[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C14BZCR)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate?business=luxusam3d%40gmail.com&currency_code=EUR)
