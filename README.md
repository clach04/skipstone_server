# skipstone_server

Fake WDTV simulator for https://github.com/Skipstone/Skipstone
aim is to be a generic multimedia keyboard to control almost any
player that supports multimedia keys.

Relies on https://github.com/asweigart/pyautogui/ TODO add requirements.txt for pip.

Provides a wsgi app, uses wsgi reference server if ran stand alone but should run with any wsgi server (Rocket, CherryPy, etc.)

Works well enough with Skipstone for Pebble that WDTV option can be used to control:

   * Windows Media Center (aka MCE)
   * Windows Media Player
   * VLC (more functionality present in Skipstone via direct VLC support)

Should work with any media player that supports media keys.
