# Driver for epd7in5b_HD 880x528

from micropython import const
from time import sleep_ms

WIDTH  = const(880)
HEIGHT = const(528)

class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT)
        self.dc.init(self.dc.OUT)
        self.rst.init(self.rst.OUT)
        self.busy.init(self.busy.IN)
        self.width = WIDTH
        self.height = HEIGHT

    def _command(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)
        
    def _wait_busy(self):
        while(self.busy.value() == 1):
            sleep_ms(200)
        
    def init(self):
        self.reset()
        self._command(0x12)
        self._wait_busy()
        self._command(0x46, b'\xF7')
        self._wait_busy()
        self._command(0x47, b'\xF7')
        self._wait_busy()
        self._command(0x0C, b'\xAE\xC7\xC3\xC0\x40')
        self._command(0x01, b'\xAF\x02\01')
        self._command(0x11, b'\x01')
        self._command(0x44, b'\x00\x00\x6F\x03')
        self._command(0x45, b'\xAF\x02\x00\x00')
        self._command(0x3C, b'\x01')
        self._command(0x18, b'\x80')
        self._command(0x22, b'\xB1')
        self._command(0x20)
        self._wait_busy()
        self._command(0x4E, b'\x00\x00')
        self._command(0x4F, b'\xAF\x02')
        
    def reset(self):
        self.rst(1)
        sleep_ms(200)
        self.rst(0)
        sleep_ms(4)
        self.rst(1)
        sleep_ms(200)

    def display_frame(self, frame_buffer_black, frame_buffer_red):
        self._command(0x4F, b'\xAF\x02')
        if (frame_buffer_black != None):
            self._command(0x24)
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([frame_buffer_black[i]]))
        if (frame_buffer_red != None):
            self._command(0x26)
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([~frame_buffer_red[i]]))
            self._command(0x22, b'\xC7')
            self._command(0x20)
            sleep_ms(200)
            self._wait_busy()

    def clear(self):
        self._command(0x4F, b'\xAF\x02')
        self._command(0x24)
        for i in range(0, self.width * self.height // 8):
            self._data(bytearray([0xff]))
        self._command(0x26)
        for i in range(0, self.width * self.height // 8):
            self._data(bytearray([0x00]))
        self._command(0x22, b'\xC7')
        self._command(0x20)
        sleep_ms(200)
        self._wait_busy()

    
    def sleep(self):
        self._command(0x10, b'\x01')
        sleep_ms(200)