notes
The board lists

``` python
['__class__', '__name__', 'A0', 'A1', 'A2', 'A3', 'BAT_ADC', 'GP0', 'GP1', 'GP10', 'GP11', 'GP12', 'GP13', 'GP14', 'GP15', 'GP16', 'GP17', 'GP18', 'GP19', 'GP2', 'GP20', 'GP21', 'GP22', 'GP23', 'GP24', 'GP25', 'GP26', 'GP26_A0', 'GP27', 'GP27_A1', 'GP28', 'GP28_A2', 'GP3', 'GP4', 'GP5', 'GP6', 'GP7', 'GP8', 'GP9', 'IMU_INT1', 'IMU_INT2', 'IMU_SCL', 'IMU_SDA', 'LCD_BL', 'LCD_CLK', 'LCD_CS', 'LCD_DC', 'LCD_DIN', 'LCD_RST', 'board_id']
```


IMU must be the sensor

The board is supposedly only 4MB of flash, but on my mac it's reporting 16MB. :shrug:

draw something to the screen

need a displayio object to connect to, so we need a driver

the display is SPI, the board has exposed pins labeled:

'LCD_BL', 'LCD_CLK', 'LCD_CS', 'LCD_DC', 'LCD_DIN', 'LCD_RST',

from the script to dump names, 
LCD_DC = 8
LCD_CS = 9
LCD_CLK = 10
LCD_DIN = 11
LCD_RST = 12
LCD_BL = 25

IMU_SDA = 6
IMU_SCL = 7

IMU_INT1 = 23
IMU_INT2 = 24

BAT_ADC = 29


according to this page
https://www.waveshare.com/wiki/RP2040-LCD-1.28

However that is the non-touch version.  For the touch version the downloaded sample code seems to have different pins:

LCD_DC = 14
LCD_CS = 9
LCD_CLK = 10
LCD_DIN = 11
LCD_RST = 8
LCD_BL = 15

this schematic says:

http://cdn.static.spotpear.com/uploads/picture/learn/raspberry-pi/rpi-pico/rp2040-lcd-1.28-touch/RP2040-Touch-LCD-1.28.pdf

LCD_DC = 8
LCD_CS = 9
LCD_CLK = 10
LCD_MOSI = 11
LCD_MISO = 12
LCD_RST = 13
LCD_BL = 25