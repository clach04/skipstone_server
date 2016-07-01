# skipstone_server

Fake WDTV simulator written in Python for https://github.com/Skipstone/Skipstone
aim is to be a generic multimedia keyboard to control almost any
player or application that supports multimedia keys.

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

### Controls

| Pebble Button                                        | WDTV Function                  | Keyboard Function on remote PC |
| ---------------------------------------------------- | ------------------------------ | ------------------------------ |
| Double click select                                  | Switch between options 1/2/3/4 | Switch between options 1/2/3/4 |
|                                                      |                                |                                |
| Single click up <sub><sup>(option 1)</sup></sub>     | Rewind                         |                                |
| Long click up <sub><sup>(option 1)</sup></sub>       | Previous                       |                                |
| Single click select <sub><sup>(option 1)</sup></sub> | Play/Pause                     |                                |
| Long click select <sub><sup>(option 1)</sup></sub>   | Stop                           |                                |
| Single click down <sub><sup>(option 1)</sup></sub>   | Forward                        |                                |
| Long click down <sub><sup>(option 1)</sup></sub>     | Next                           |                                |
|                                                      |                                |                                |
| Single click up <sub><sup>(option 2)</sup></sub>     | Up                             |                                |
| Long click up <sub><sup>(option 2)</sup></sub>       | Left                           |                                |
| Single click select <sub><sup>(option 2)</sup></sub> | OK                             |                                |
| Long click select <sub><sup>(option 2)</sup></sub>   | Back                           |                                |
| Single click down <sub><sup>(option 2)</sup></sub>   | Down                           |                                |
| Long click down <sub><sup>(option 2)</sup></sub>     | Right                          |                                |
|                                                      |                                |                                |
| Single click up <sub><sup>(option 3)</sup></sub>     | Back                           |                                |
| Long click up <sub><sup>(option 3)</sup></sub>       | Mute                           |                                |
| Single click select <sub><sup>(option 3)</sup></sub> | Home                           |                                |
| Long click select <sub><sup>(option 3)</sup></sub>   | Option                         |                                |
| Single click down <sub><sup>(option 3)</sup></sub>   | Setup                          |                                |
| Long click down <sub><sup>(option 3)</sup></sub>     | Power                          |                                |
