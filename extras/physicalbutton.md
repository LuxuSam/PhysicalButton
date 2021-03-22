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

# Screenshots
<p align="middle">
  <img src="/assets/img/NewGcodeButton.png" width="49%"/>
  <img src="/assets/img/NewActionButton.png" width="49%"/>
  <img src="/assets/img/ListButtons.png" width="49%"/>
</p>
