from machine import Pin,SPI
import framebuf
import time

DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class Display(framebuf.FrameBuffer):
    WIDTH = 128
    HEIGHT = 64
    HALF_WIDTH = WIDTH/2
    HALF_HEIGHT = HEIGHT/2
    
    def __init__(self):
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,2000_000)
        self.spi = SPI(1,20000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(Display.HEIGHT * Display.WIDTH // 8)
        super().__init__(self.buffer, Display.WIDTH, Display.HEIGHT, framebuf.MONO_HMSB)
        self.init_display()
        self.white =   0xffff
        self.black =   0x0000

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        self.write_cmd(0xAE)
        self.write_cmd(0x00)
        self.write_cmd(0x10)
        self.write_cmd(0xB0)
        self.write_cmd(0xdc)
        self.write_cmd(0x00)
        self.write_cmd(0x81)
        self.write_cmd(0x6f)
        self.write_cmd(0x21)
        self.write_cmd(0xa0)
        self.write_cmd(0xc0)
        self.write_cmd(0xa4)
        self.write_cmd(0xa6)
        self.write_cmd(0xa8)
        self.write_cmd(0x3f)
        self.write_cmd(0xd3)
        self.write_cmd(0x60)
        self.write_cmd(0xd5)
        self.write_cmd(0x41)
        self.write_cmd(0xd9)
        self.write_cmd(0x22)
        self.write_cmd(0xdb)
        self.write_cmd(0x35)
        self.write_cmd(0xad)
        self.write_cmd(0x8a)
        self.write_cmd(0XAF)

    def show(self):
        self.write_cmd(0xb0)
        for page in range(0,64):
            self.column = 63 - page              
            self.write_cmd(0x00 + (self.column & 0x0f))
            self.write_cmd(0x10 + (self.column >> 4))
            for num in range(0,16):
                self.write_data(self.buffer[page*16+num])

    def center(self, text, height, color):
        self.text(text, int(Display.WIDTH/2)-4*len(text),height,color)
        self.show()

    def animation(self):
        for i in range(0, Display.WIDTH, 16):
            self.rect(i,48,14,14,self.white)
            self.show()   
        for i in range(48, 0, -16):
            self.rect(112,i,14,14,self.white)
            self.show()  
        for i in range(112, 0, -16):
            self.rect(i,0,14,14,self.white)
            self.show() 
        for i in range(0, Display.HEIGHT, 16):
            self.rect(0,i,14,14,self.white)
            self.show()
