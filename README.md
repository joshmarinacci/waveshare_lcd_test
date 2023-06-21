# Waveshare LCD Test

A set of tests and utility functions for working with the 
[Waveshare round 1.28 LCD + touch + RP2040 core + accelerometer](https://www.waveshare.com/rp2040-touch-lcd-1.28.htm).



see also the [notes](notes.md)



# setup

### Install CircuitPython

First you need a recent version of CircuitPython on the device. You can get the latest version
from [here](https://circuitpython.org/board/waveshare_rp2040_lcd_1_28/). Note that this is for
the non-touch version of this board. There is no build for the touch version so you'll have to use
this one and then add in the utils library from this repo.

To install CircuitPython (hereafter referred to as *CP*), you must reset the device to firmware
mode by holding down the *boot* button while plugging it into USB on your computer. You will see
a drive called `RPI-RP2` appear on your computer. Note: this won't work if you have a battery plugged into the board. Disconnect the battery before trying this. Once you see the `RPI_RP2` drive
drag the downloaded *.UF2* file to the drive. This will install CP and reboot. When you see the 
the CIRCUITPY drive it will be done. 

Look at the *boot_out.txt* file on the CIRCUITPY drive to see if it
is a recent version of CP. At the time of writing this readme, I am running CP 8.1 stable,
and CP 8.2 beta should also work.

### Install the lib and a simple test.

Copy `waveshare128.py` and `code.py` to the CP drive.  It will reboot automatically. If you look
at the console through whatever IDE you are using, or the command line 
(`screen /dev/tty.usbmodemSOMETHING` on MacOS), you will likely see an error about a missing
module like `gc9a01`.  This code requires some libraries. You can either download the full libraries
and extract the ones you need by following [this guide](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries) or use the [circup command line tool](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/install-circup) to install them.
I prefer `circup`, like this:


```shell
# list the currently installed modules
circup freeze
# install 
circup install gc9a01
```

Now you should see the boot text on the device's display, and then a white circle. You can drag the circle around
with your finger on the touch screen. On the console you'll see constant output about the state of touches
on the touch screen.



# Examples

* `tilt.py` draws a circle at the  'down' direction of the screen, using the accelerometer
* `touch.py` draws a circle wherever you touch the screen
* `bignum_clock.py` draws the time using large number sprites
* `earth.py` draws static image of Earth from space
* `eyedraw.py` Eye of Agamotto animation
* `kalidedraw.py`  drag finger on screen to draw with 4x kalidescope reflection
* `watch.py` Beginnings of a multi-screen smart watch. Swipe left and right to switch screens

# running the examples

Copy one of the example programs to `/CIRCUIPY/code.py`. Leave the libs as they are. 
Example: to run the Kalidascope drawing example, copy `kalidedraw.py` to `code.py` on your device.



# customizing images

Some of the examples use images. You can replace them with your own, but make sure
to use the same size and format them as indexed BMP files. [Read more about CP BMP formats](https://learn.adafruit.com/creating-your-first-tilemap-game-with-circuitpython/indexed-bmp-graphics)

Convert a PNG on disk to BMP

```shell
convert digits.png -colors 64 -type palette -compress None BMP3:digits.bmp
```

Then copy `digits.bmp` to the device drive