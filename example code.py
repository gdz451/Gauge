"""
Gauge.py

Turning the arc function into a guage that starts at angle 315 degrees
and sweeps 270 degrees


"""

import math
import time
import board
import displayio
import terminalio
from gauge import Gauge
from adafruit_display_text import bitmap_label

display = board.DISPLAY

# Make the display context
main_group = displayio.Group()

# Make a background color fill
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
main_group.append(bg_sprite)
display.show(main_group)
#
# ----------------------------------------------------

gauge1 = Gauge(
    xcenter=30,
    ycenter=30,
    radius=27,
    width=3,
    progress=10,
    lineColor=0xFFFFFF,
    progressColor=0x00FF00,
    backgroundColor=0x000000,
)
main_group.append(gauge1)

gauge2 = Gauge(
    xcenter=90,
    ycenter=30,
    radius=27,
    width=8,
    progress=30,
    lineColor=0xFFFFFF,
    progressColor=0x00FF00,
    backgroundColor=0x000000,
)
main_group.append(gauge2)
gauge3 = Gauge(
    xcenter=150,
    ycenter=30,
    radius=27,
    width=10,
    progress=60,
    lineColor=0xFFFFFF,
    progressColor=0xFF0000,
    backgroundColor=0x000000,
)
main_group.append(gauge3)

gauge4 = Gauge(
    xcenter=210,
    ycenter=30,
    radius=28,
    width=12,
    progress=0,
    lineColor=0xFFFFFF,
    progressColor=0xFF0000,
    backgroundColor=0x000000,
)
main_group.append(gauge4)


gauge5 = Gauge(
    xcenter=120,
    ycenter=120,
    radius=50,
    width=20,
    progress=0,
    lineColor=0xFFFFFF,
    progressColor=0x00FF00,
    backgroundColor=0x000000,
)
main_group.append(gauge5)



while True:

    for i in range(0, 101, 4):
        if i >= 80:
            gauge4.progressColor = 0xFF0000
            gauge5.progressColor = 0xFF0000
        else:
            gauge4.progressColor = 0x00FF00
            gauge5.progressColor = 0x00FF00

        gauge4.progress= i
        gauge5.progress = i
        time.sleep(0.1)


    for i in range(100, 0, -4):
        if i >= 80:
            gauge4.progressColor = 0xFF0000
            gauge5.progressColor = 0xFF0000
        else:
            gauge4.progressColor = 0x00FF00
            gauge5.progressColor = 0x00FF00

        gauge4.progress= i
        gauge5.progress = i
        time.sleep(0.1)

