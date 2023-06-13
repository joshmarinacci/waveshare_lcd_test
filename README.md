# Waveshare LCD Test

A set of tests and utility functions for working with the 
[Waveshare round 1.28 LCD + touch + RP2040 core + accelerometer](https://www.waveshare.com/rp2040-touch-lcd-1.28.htm).



see also the [notes](notes.md)



To run an example like `kalidedraw.py`, copy it to `code.py` on your device, and also copy `waveshare128.py`. You'll also
need to make sure any other libs are installed using `circup update`


* `tilt.py` draws a circle at the  'down' direction of the screen, using the accelerometer
* `touch.py` draws a circle wherever you touch the screen
* `bignum_clock.py` draws the time using large number sprites
* `earth.py` draws static image of Earth from space
* `eyedraw.py` Eye of Agamotto animation
* `kalidedraw.py`  drag finger on screen to draw with 4x kalidescope reflection
* `watch.py` Beginnings of a multi-screen smart watch. Swipe left and right to switch screens

