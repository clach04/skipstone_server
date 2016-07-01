# skipstone_server

Fake WDTV simulator for [Pebble app Skipstone](https://github.com/Skipstone/Skipstone)
aim is to be a generic multimedia keyboard to control almost any
player or application that supports multimedia keys.

Should work with:

   * Windows
   * Linux
   * Mac OS X

Downloads (including Windows exes) available from https://github.com/clach04/skipstone_server/releases/

Works well enough with Skipstone for Pebble that WDTV option can be used to control:

   * Windows Media Center (aka MCE)
   * Windows Media Player
   * Winamp
   * VLC (more functionality present in Skipstone via direct VLC support)
   * LibreOffice Impress for navigating presentation slides (up/down goes backwards/forwards and select also does forwards)

Should work with any media player that supports media keys.

## Instructions

  1. If not already installed install Pebble app from appstore https://apps.getpebble.com/en_US/application/52f1095ba0cb6abe6d002f05.
  2. Install/run the server `wdtv_sim.exe` (or `wdtv_sim.py` if running from source), by default the server starts on the local machine listening on port 8777.
  2. Open Skipstone config on phone, add a new WDTV device, name it, e.g. `fake WDTV`, enter in ip address of machine, colon, 8777. For example, assume IP address for server machine is 10.10.10.10, enter in, `10.10.10.10:8777`.
  3. Save and then open Skipstone on watch, open WDTV from above (e.g. `fake WDTV`). See below for some information on controls and see https://github.com/Skipstone/Skipstone#wdtv for latest information.

### Controls


<img src="https://raw.githubusercontent.com/Skipstone/Skipstone/master/resources/images/wdtv.png" alt="Skipstone Pebble screen, showing three different options"> 

| Pebble Button                                        | WDTV Function                  | Keyboard Function on remote PC |
| ---------------------------------------------------- | ------------------------------ | ------------------------------ |
| Double click select                                  | Switch between options 1/2/3   | Switch between options 1/2/3   |
|                                                      |                                |                                |
| Single click up <sub><sup>(option 1)</sup></sub>     | Rewind                         | Ctrl+Left and Ctrl+Shift+b     |
| Long click up <sub><sup>(option 1)</sup></sub>       | Previous                       | Multimedia key: Previous track |
| Single click select <sub><sup>(option 1)</sup></sub> | Play/Pause                     | Multimedia key: Play/Pause     |
| Long click select <sub><sup>(option 1)</sup></sub>   | Stop                           | Multimedia key: Stop           |
| Single click down <sub><sup>(option 1)</sup></sub>   | Forward                        | Ctrl+Right and Ctrl+Shift+f    |
| Long click down <sub><sup>(option 1)</sup></sub>     | Next                           | Multimedia key: Next track     |
|                                                      |                                |                                |
| Single click up <sub><sup>(option 2)</sup></sub>     | Up                             | Up                             |
| Long click up <sub><sup>(option 2)</sup></sub>       | Left                           | Left                           |
| Single click select <sub><sup>(option 2)</sup></sub> | OK                             | Enter/Return                   |
| Long click select <sub><sup>(option 2)</sup></sub>   | Back                           | Multimedia key: Browser back   |
| Single click down <sub><sup>(option 2)</sup></sub>   | Down                           | Down                           |
| Long click down <sub><sup>(option 2)</sup></sub>     | Right                          | Right                          |
|                                                      |                                |                                |
| Single click up <sub><sup>(option 3)</sup></sub>     | Back                           | Multimedia key: Browser back   |
| Long click up <sub><sup>(option 3)</sup></sub>       | Mute                           | Multimedia key: Mute toggle    |
| Single click select <sub><sup>(option 3)</sup></sub> | Home                           | TBD                            |
| Long click select <sub><sup>(option 3)</sup></sub>   | Option                         | TBD                            |
| Single click down <sub><sup>(option 3)</sup></sub>   | Setup                          | TBD                            |
| Long click down <sub><sup>(option 3)</sup></sub>     | Power                          | TBD                            |

## Source information

Relies on https://github.com/asweigart/pyautogui/ TODO add requirements.txt for pip.

Known to work with Python 2.6.6 and 2.7.

Provides a wsgi app, uses wsgi reference server if ran stand alone but should run with any wsgi server (Rocket, CherryPy, etc.)

