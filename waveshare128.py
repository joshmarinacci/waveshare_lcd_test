import board
import displayio
import analogio
import busio
import gc9a01

def setup_display(speed=100_000_000):
    print("display setup")
    # setup the display
    displayio.release_displays()
    spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_DIN)
    # LCD_RST is 12 in the regular, but 13 for the touch version
    display_bus = displayio.FourWire(spi, command=board.LCD_DC, chip_select=board.LCD_CS,reset=board.GP13, baudrate=speed)
    display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=board.LCD_BL, rotation=0, auto_refresh=False)
    return display


class Touch_CST816T(object):
    x = 0
    y = 0
    #Initialize the touch chip  初始化触摸芯片
    def __init__(self, address=0x15, mode=0, i2c_num=1, i2c_sda=6, i2c_scl=7, int_pin=21, rst_pin=22, LCD=None):
        self._address = address
        self._bus = busio.I2C(board.GP7, board.GP6)
        # self._bus = I2C(id=i2c_num,scl=Pin(i2c_scl),sda=Pin(i2c_sda),freq=400_000) #Initialize I2C 初始化I2C
        # self._address = address #Set slave address  设置从机地址
        # self.int=Pin(int_pin,Pin.IN, Pin.PULL_UP)
        # self.tim = Timer()
        # self.rst=Pin(rst_pin,Pin.OUT)
        # self.Reset()
        if self.who_am_i():
            self.rev = self.read_revision()
            print("CST816T Revision = {}".format(self.rev))
            self.Stop_Sleep()
        else:
            raise Exception("CST816T not found")
        self.config_apply()

        # bRet=self.WhoAmI()
        # if bRet :
        #     print("Success:Detected CST816T.")
        #     Rev= self.Read_Revision()
        #     print("CST816T Revision = {}".format(Rev))
        #     self.Stop_Sleep()
        # else    :
        #     print("Error: Not Detected CST816T.")
        #     return None
        self.Mode = mode
        self.Gestures="None"
        self.Flag = self.Flgh =self.l = 0
        self.X_point = self.Y_point = 0
        self.Set_Mode(0)
        # self.int.irq(handler=self.Int_Callback,trigger=Pin.IRQ_FALLING)

    def config_apply(self):
        print("configuring self")


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


    # def _read_block(self, reg, length=1):
    #     rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
    #     return rec

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

    # def _write_byte(self,cmd,val):
    #     self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))

    # def WhoAmI(self):
    #     if (0xB5) != self._read_byte(0xA7):
    #         return False
    #     return True
    def who_am_i(self):
        bRet=False
        rec = self._read_byte(0xA7)
        if (0xB5) == rec:
            bRet = True
        return bRet

    def read_revision(self):
        return self._read_byte(0xA9)

    #Stop sleeping  停止睡眠
    def Stop_Sleep(self):
        self._write_byte(0xFE,0x01)

    #Reset  复位
    def Reset(self):
        self.rst(0)
        time.sleep_ms(1)
        self.rst(1)
        time.sleep_ms(50)

    #Set mode  设置模式
    def Set_Mode(self,mode,callback_time=10,rest_time=5):
        # mode = 0 gestures mode
        # mode = 1 point mode
        # mode = 2 mixed mode
        if (mode == 1):
            self._write_byte(0xFA,0X41)

        elif (mode == 2) :
            self._write_byte(0xFA,0X71)

        else:
            self._write_byte(0xFA,0X11)
            self._write_byte(0xEC,0X01)

    #Get the coordinates of the touch  获取触摸的坐标
    def get_point(self):
        xy_point = self._read_block(0x03,4)

        x_point= ((xy_point[0]&0x0f)<<8)+xy_point[1]
        y_point= ((xy_point[2]&0x0f)<<8)+xy_point[3]

        self.X_point=x_point
        self.Y_point=y_point

    def Int_Callback(self,pin):
        if self.Mode == 0 :
            self.Gestures = self._read_byte(0x01)

        elif self.Mode == 1:
            self.Flag = 1
            self.get_point()

    def Timer_callback(self,t):
        self.l += 1
        if self.l > 100:
            self.l = 50

    def update(self):
        self.gestureId = self._read_byte(0x01)
        self.fingerNum = self._read_byte(0x02)
        xy_point = self._read_block(0x03,4)
        self.x = ((xy_point[0]&0x0f)<<8)+xy_point[1]
        self.y = ((xy_point[2]&0x0f)<<8)+xy_point[3]


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


class Battery(object):
    # Initialize the battery
    # returns: nothing
    def __init__(self, pin=board.BAT_ADC):
        self._pin = analogio.AnalogIn(pin)
        self._max_voltage = 4.14
        self._min_voltage = 3.4
        self._max_diff = self._max_voltage - self._min_voltage
        self._diff = 0.0
        self._voltage = 0.0
        self._percent = 0.0
        self._charging = False
        self._discharging = False
        self._full = False
        self._empty = False
        self._update()

    # Update the battery status
    # returns: nothing
    def _update(self):
        # Read the battery voltage
        self._voltage = self._pin.value * 3.3 / 65535 * 2
        self._diff = self._max_voltage - self._voltage
        # Convert the voltage to a percentage
        if self._voltage > self._max_voltage:
            self._percent = 100.0
        elif self._voltage < self._min_voltage:
            self._percent = 0.0
        else:
            self._percent = (self._diff / self._max_diff) * 100.0 
        # Determine the charging status
        if self._voltage > 4.14:
            self._charging = True
            self._discharging = False
            self._full = True
            self._empty = False
        elif self._voltage < 3.4:
            self._charging = False
            self._discharging = False
            self._full = False
            self._empty = True
        else:
            self._charging = False
            self._discharging = True
            self._full = False
            self._empty = False

    # Get the battery voltage
    # returns: the battery voltage
    @property
    def voltage(self):
        self._update()
        return self._voltage

    # Get the battery percentage
    # returns: the battery percentage
    @property
    def percent(self):
        self._update()
        return self._percent

    # Get the charging status
    # returns: True if the battery is charging, False otherwise
    @property
    def charging(self):
        self._update()
        return self._charging

    # Get the discharging status
    # returns: True if the battery is discharging, False otherwise
    @property
    def discharging(self):
        self._update()
        return self._discharging


