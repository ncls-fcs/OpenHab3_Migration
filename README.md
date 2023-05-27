# OpenHab3_Migration
A little script that converts the KNX-Things in OpenHAB2 config files to the JSON format used by OpenHAB in its UI-based configuration.
Use it to easily move multiple Things from OH2 to OH3´s UI without having to click through the UI for every Thing.

This implementation parses the OH2 config file, filters out KNX-devices and saves them as an internal object. The process of generating valid OpenHAB3 JSON is done in another step.

This internal representation enables the posibility to convert your old KNX-Thing configuration to everything you want. There is also a function to convert them into a HomeBridge compatible format that you can paste into HomeBridge´s configuration.


The script is only hacked together in a very basic way and might not work for your configuration file. It also currently only supports Lights (OpenHab Switches) and Rollershutters (as I dont have anything else implemented through KNX). If you want support for other OpenHAB Things, simply open an issue and I will work on it.
As I said the implementation is very rudimentary and far from perfect but it worked for me and more importantly it doesnt rely on any external libraries.
