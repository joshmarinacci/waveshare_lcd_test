notes
The board lists

``` python
['__class__', '__name__', 'A0', 'A1', 'A2', 'A3', 'BAT_ADC', 'GP0', 'GP1', 'GP10',
 'GP11', 'GP12', 'GP13', 'GP14', 'GP15', 'GP16', 'GP17', 'GP18', 'GP19', 'GP2', 
 'GP20', 'GP21', 'GP22', 'GP23', 'GP24', 'GP25', 'GP26', 'GP26_A0', 'GP27', 
 'GP27_A1', 'GP28', 'GP28_A2', 'GP3', 'GP4', 'GP5', 'GP6', 'GP7', 'GP8', 'GP9', 
 'IMU_INT1', 'IMU_INT2', 'IMU_SCL', 'IMU_SDA',
  'LCD_BL', 'LCD_CLK', 'LCD_CS', 'LCD_DC', 'LCD_DIN', 'LCD_RST', 'board_id']
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





# touch sensor

The touch sensor is accessed over I2C and is documented in the PDF. It has three *modes*.  In *dynamic* mode the chip is always scanning and you can always get the current touch.  In *standby* mode the chip scans at a lower frequency and notifies the main CPU using an interrupt when a gesture occurs. It is not clear how a gesture is defined. Any touch? A specific length of time? An up or down swipe?  The third mode is a *sleep* mode where it does not scan at all to save power.

According to the docs the i2c communication can be anywhere from 10khz to 400khz rate.

There is a [second PDF](docs/CST816S_register_declaration.pdf) in Chinese which details the 
meaning of the different registers. Combined with the example code, hopefully this is 
enough to reverse engineer the protocol. Below are my notes on the different registers


# Registers

* 0x01 = Gesture ID
  * reading a byte from this register returns a number for the kind of gesture. So far it seems that these are the values
  * 0x00: seems to be when a finger is touching the screen?
  * 0x01: did a bottom to top swipe
  * 0x02: did a top to bottom swipe
  * 0x03: did a right to left swipe
  * 0x04: did a left to right swipe
  * 0x05: when a touch is done??
  * 0x0B: ???
  * 0x0C: ???
* 0x02 = Finger Num
  * this only ever seems to be zero for no fingers and 1 for a single active figure
* 0x03 = XPosH
  * this and the next three bytes represent the X and Y. I think they are in pairs for the low and high bytes of a 16bit integer
* 0x04 = XposL
* 0x05 = YposH
* 0x06 = YposL
* 0xB0 = BPC0H
* 0xB1 = BPC0L
* 0xB2 = BPC1H
* 0xB3 = BPC1L
* 0xA7 = ChipID
* 0xA8 = ProjID
* 0xA9 = FwVersion
* 0xEC = MotionMask
* 0xED = IrqPluseWidth
* 0xEE = NorScanPer
* 0xEF = MotionS1Angle
* 0xF0 = LpScanRaw1H
* 0xF1 = LpScanRaw1L
* 0xF2 = LpScanRaw2H
* 0xF3 = LpScanRaw2L
* 0xF4 = LpAutoWakeTime
* 0xF5 = LpScanTH
* 0xF6 = LpScanWin
* 0xF7 = LpScanFreq
* 0xF8 = LpScanIdac
* 0xF9 = AutoSleepTime
* 0xFA = IrqCtl
* 0xFB = AutoReset
* 0xFC = LongPressTime
* 0xFD = IOCtl
  * the PDF says that three bits are used for `SOFT_RST`, `IIC_OD` and `En1v8`. `SOFT_RST` probably means soft reset. So if we write a 1 to bit 2 of register 0xFD then it will do a soft reset?  
* 0xFE = DisAutoSleep
