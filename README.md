# skipstone_server

Fake WDTV simulator written in Python for https://github.com/Skipstone/Skipstone
aim is to be a generic multimedia keyboard to control almost any
player that supports multimedia keys.

Relies on https://github.com/asweigart/pyautogui/ TODO add requirements.txt for pip.

Provides a wsgi app, uses wsgi reference server if ran stand alone but should run with any wsgi server (Rocket, CherryPy, etc.)

Works well enough with Skipstone for Pebble that WDTV option can be used to control:

   * Windows Media Center (aka MCE)
   * Windows Media Player
   * VLC (more functionality present in Skipstone via direct VLC support)
   * LibreOffice Impress for navigating presentation slides (up/down goes backwards/forwards and select also does forwards)

Should work with any media player that supports media keys.

## Instructions

  1. Install/run, by default the server starts on the local machine listening on port 8777.
  2. Open Skipstone config on phone, add a new WDTV device, name it, e.g. `fake WDTV`, enter in ip address of machinr, colon, 8777. For example, assume IP address for server machine is 10.10.10.10, enter in, `10.10.10.10:8777`.
  3. Save and then open Skipstone on watch, open WDTV from above (e.g. `fake WDTV`) then control and see https://github.com/Skipstone/Skipstone#wdtv for controls
