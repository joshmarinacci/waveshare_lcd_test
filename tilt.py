import busio
import board
import time
import board
import os
import displayio
import gc9a01
from vectorio import Rectangle, Circle, Polygon


# A class to interface with a Microchip QMI8658 6-axis IMU
# https://www.microchip.com/wwwproducts/en/QMI8658
# Working code already exists in micropython, this is an 
# adaptation of that code for use with CircuitPython (see
# micro.py for the original code)
class QMI8658_Accelerometer(object):
    # Initialize the hardware
    # address: the I2C address of the device
    # returns: nothing
    def __init__(self,address=0X6B, scl=board.GP7, sda=board.GP6):
        self._address = address
        self._bus = busio.I2C(scl,sda)
        if self.who_am_i():
            self.rev = self.read_revision()
        else:
            raise Exception("QMI8658 not found")
        self.config_apply()
    
    # Read a byte from the specified register
    # register: the register to read from
    # returns: the byte read
    def _read_byte(self,register):
        return self._read_block(register,1)[0]

    # Read a block of bytes from the specified register
    # register: the register to begin the read from
    # length: the number of bytes to read
    # returns: a list of bytes read
    def _read_block(self, register, length=1):
        while not self._bus.try_lock():
            pass
        try:
            rx = bytearray(length)
            self._bus.writeto(self._address, bytes([register]))
            self._bus.readfrom_into(self._address, rx)
        finally:
            self._bus.unlock()    
        return rx
    
    # Read a 16-bit unsigned integer from the specified register
    # register: the register to begin the read from
    # returns: the 16-bit unsigned integer read
    def _read_u16(self,register):
        return (self._read_byte(register) << 8) + self._read_byte(register+1)

    # Write a byte to the specified register
    # register: the register to write to
    # value: the byte to write
    # returns: nothing    
    def _write_byte(self,register,value):
        while not self._bus.try_lock():
            pass
        try:
            self._bus.writeto(self._address, bytes([register, value]))
            #self._bus.writeto(self._address, bytes([value]))
        finally:
            self._bus.unlock()

    # Make sure this device is what it thinks it is
    # returns: True if the device is what it thinks it is, False otherwise  
    def who_am_i(self):
        bRet=False
        rec = self._read_byte(0x00)
        if (0x05) == rec:
            bRet = True   
        return bRet

    # Read the revision of the device
    # returns: the revision of the device
    def read_revision(self):
        return self._read_byte(0x01)

    # Apply the configuration to the device by writing to 
    # the appropriate registers.  See device datasheet for
    # details on the configuration.
    # returns: nothing    
    def config_apply(self):
        # REG CTRL1
        self._write_byte(0x02,0x60)
        # REG CTRL2 : QMI8658AccRange_8g  and QMI8658AccOdr_1000Hz
        self._write_byte(0x03,0x23)
        # REG CTRL3 : QMI8658GyrRange_512dps and QMI8658GyrOdr_1000Hz
        self._write_byte(0x04,0x53)
        # REG CTRL4 : No
        self._write_byte(0x05,0x00)
        # REG CTRL5 : Enable Gyroscope And Accelerometer Low-Pass Filter 
        self._write_byte(0x06,0x11)
        # REG CTRL6 : Disables Motion on Demand.
        self._write_byte(0x07,0x00)
        # REG CTRL7 : Enable Gyroscope And Accelerometer
        self._write_byte(0x08,0x03)

    # Read the raw accelerometer and gyroscope data from the device
    # returns: a list of 6 integers, the first 3 are the accelerometer
    #          data, the last 3 are the gyroscope data
    def read_raw_xyz(self):
        xyz=[0,0,0,0,0,0]
        raw_timestamp = self._read_block(0x30,3)
        raw_acc_xyz=self._read_block(0x35,6)
        raw_gyro_xyz=self._read_block(0x3b,6)
        raw_xyz=self._read_block(0x35,12)
        timestamp = (raw_timestamp[2]<<16)|(raw_timestamp[1]<<8)|(raw_timestamp[0])
        for i in range(6):
            # xyz[i]=(raw_acc_xyz[(i*2)+1]<<8)|(raw_acc_xyz[i*2])
            # xyz[i+3]=(raw_gyro_xyz[((i+3)*2)+1]<<8)|(raw_gyro_xyz[(i+3)*2])
            xyz[i] = (raw_xyz[(i*2)+1]<<8)|(raw_xyz[i*2])
            if xyz[i] >= 32767:
                xyz[i] = xyz[i]-65535
        return xyz

    # Read the accelerometer and gyroscope data from the device and return
    # in human-readable format.
    # returns: a list of 6 floats, the first 3 are the accelerometer
    #         data, the last 3 are the gyroscope data    
    def read_xyz(self):
        xyz=[0,0,0,0,0,0]
        raw_xyz=self.read_raw_xyz()  
        #QMI8658AccRange_8g
        acc_lsb_div=(1<<12)
        #QMI8658GyrRange_512dps
        gyro_lsb_div = 64
        for i in range(3):
            xyz[i]=raw_xyz[i]/acc_lsb_div#(acc_lsb_div/1000.0)
            xyz[i+3]=raw_xyz[i+3]*1.0/gyro_lsb_div
        return xyz


# setup accel
qmi = QMI8658_Accelerometer()


# setup display
displayio.release_displays()
spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_DIN)
# LCD_RST is 12 in the regular, but 13 for the touch version
display_bus = displayio.FourWire(spi, command=board.LCD_DC, chip_select=board.LCD_CS,reset=board.GP13)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=board.LCD_BL)

main = displayio.Group()


circ_palette = displayio.Palette(1)
circ_palette[0] = (255,0,255)
circ = Circle(pixel_shader=circ_palette, radius=10, x=120, y=120)
circ.x = 120
circ.y = 120
main.append(circ)

display.show(main)


xsamples = []
ysamples = []

while True:
    display.refresh()
    time.sleep(0.08)
    xyz = qmi.read_xyz()
    accel = {}
    gyro = {}
        
    accel['x'] = xyz[1]
    accel['y'] = xyz[0]
    accel['z'] = xyz[2]
    gyro['x'] = xyz[3]
    gyro['y'] = xyz[4]
    gyro['z'] = xyz[5]       
    # print('accel',accel)
    xsamples.append(accel['x'])
    ysamples.append(accel['y'])
    if len(xsamples) > 5:
        xsamples.pop(0)
    if len(ysamples) > 5:
        ysamples.pop(0)
    xavg = sum(xsamples)/len(xsamples)
    yavg = sum(ysamples)/len(ysamples)
    circ.x = 120 + int(xavg*100)
    circ.y = 120 + int(yavg*100*-1)



