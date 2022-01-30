# Test for epd7in5b_HD

from epaper7in5b_HD import EPD, WIDTH, HEIGHT
from machine import Pin, SPI
from micropython import const
import framebuf

# Tested on E-PAPER-ESP32-DRIVER-BOARD with already soldered cable connector.
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(13),
          miso=Pin(23), mosi=Pin(14))
e_ink = EPD(spi, cs=Pin(15), dc=Pin(27), rst=Pin(26), busy=Pin(25))

spi.init()
e_ink.init()
#e_ink.clear()

BLACK = const(0)
WHITE = const(1)
STEP = const(174)

buf = bytearray(WIDTH * HEIGHT // 8)
fb = framebuf.FrameBuffer(buf, WIDTH, HEIGHT, framebuf.MONO_HLSB)

fb.fill(WHITE)
for i in range(0, WIDTH, STEP):
    fb.fill_rect(i, 0, 10, HEIGHT, BLACK)
    fb.fill_rect(0, i, WIDTH, 10, BLACK)
    for t in range(0, 3):
        fb.text('T E S T', i + 63, 80 + t*STEP, BLACK)
    
e_ink.display_frame(buf, None) # Loading a black frame without displaying on the screen.

fb.fill(WHITE)
for i in range(0, WIDTH, STEP):
    for t in range(0, 3):
        fb.fill_rect(i + 25, 25 + t*STEP, 134, 134, BLACK)
        fb.text('T E S T', i + 63, 80 + t*STEP, WHITE)
        fb.text('T E S T', i + 63, 97 + t*STEP, WHITE)
        fb.rect(i + 45, 45 + t*STEP, 94, 94, WHITE)
    
e_ink.display_frame(None, buf) # After loading the red frame, the screen refreshes.

del buf
e_ink.sleep()