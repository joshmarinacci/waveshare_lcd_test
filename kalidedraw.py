import time
import board, busio
import displayio
import gc9a01
import gifio
import vectorio
import bitmaptools
import gc
import adafruit_imageload

SPEED = 100_000_000
TARGET_FPS = 100

# setup the display
displayio.release_displays()
spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_DIN)
# LCD_RST is 12 in the regular, but 13 for the touch version
display_bus = displayio.FourWire(spi, command=board.LCD_DC, chip_select=board.LCD_CS,reset=board.GP13, baudrate=SPEED)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=board.LCD_BL, rotation=0, auto_refresh=False)



# make the main group
main = displayio.Group()
display.root_group = main


class Touch_CST816T(object):
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



# setup accel
touch = Touch_CST816T()

pal = displayio.Pallet()
pal[0] = 0x000000
pal[1] = 0xFFFFFF
bitmap = displayio.Bitmap(240,240,2)
bitmap.fill(0)
tilemap = displayio.TileGrid(bitmap,pixel_shader=pal)

main.append(tilemap)


while True:
    time.sleep(0.01)
    state = touch._read_byte(0x01)
    num = touch._read_byte(0x02)
    xy_point = touch._read_block(0x03,4)
    x_point= ((xy_point[0]&0x0f)<<8)+xy_point[1]
    y_point= ((xy_point[2]&0x0f)<<8)+xy_point[3]
    print('num',num,x_point,y_point)
    bitmap[x_point,y_point] = 1
    display.refresh()



