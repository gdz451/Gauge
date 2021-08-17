"""
Gauge

Class to create a 270 degree Progress Gauge

"""

import math
import displayio
import bitmaptools
import time

class Gauge(displayio.TileGrid):

    def __init__(self, xcenter, ycenter, radius, width, progress, lineColor, progressColor, backgroundColor):

        self.xcenter = xcenter
        self.ycenter = ycenter
        self.radius = radius
        self.width = width
        if width < 2:
            self.width = 2
        self._progress = progress
        tileGridWidth = 2 * self.radius + 1
        tileGridHeight = math.ceil(0.71 * self.radius) + self.radius + 1
        self._bitmap = displayio.Bitmap(tileGridWidth, tileGridHeight, 3)

        self._palette = displayio.Palette(3)
        self._palette[0] = backgroundColor
        self._palette[1] = lineColor
        self._palette[2] = progressColor
        x_offset = self.xcenter - self.radius + 1
        y_offset = self.ycenter - self.radius + 1

        super().__init__(
            self._bitmap, pixel_shader=self._palette, x=x_offset, y=y_offset
        )

        self._draw_gauge()


    def _draw_gauge(self):
        # empty the bitmap
        #self._bitmap.fill(0)


        x = 0
        y = self.radius
        d = 3 - 2 * self.radius

        # Bresenham's circle algorithm drawing octants 1 - 6, skipping 0 & 7
        # Outer arc
        while x <= y:
            self._bitmap[-x + self.radius, -y + self.radius] = 1
            self._bitmap[x + self.radius, -y + self.radius] = 1
            self._bitmap[y + self.radius, x + self.radius] = 1
            self._bitmap[-y + self.radius, x + self.radius] = 1
            self._bitmap[-y + self.radius, -x + self.radius] = 1
            self._bitmap[y + self.radius, -x + self.radius] = 1

            if d <= 0:
                d = d + (4 * x) + 6
            else:
                d = d + 4 * (x - y) + 10
                y = y - 1
            x = x + 1
        self.yend = self.xend = x - 1

        # Inner Arc
        x = 0
        y = self.radius - self.width + 1
        d = 3 - 2 * y

        while x <= y:
            self._bitmap[-x + self.radius, -y + self.radius] = 1
            self._bitmap[x + self.radius, -y + self.radius] = 1
            self._bitmap[y + self.radius, x + self.radius] = 1
            self._bitmap[-y + self.radius, x + self.radius] = 1
            self._bitmap[-y + self.radius, -x + self.radius] = 1
            self._bitmap[y + self.radius, -x + self.radius] = 1

            if d <= 0:
                d = d + (4 * x) + 6
            else:
                d = d + 4 * (x - y) + 10
                y = y - 1
            x = x + 1
        self.yend2 = x
        self.xend2 = x

        # Connect inner and outer arc at endpoints
        bitmaptools.draw_line(self._bitmap, self.radius + self.xend, self.radius + self.yend, self.radius + self.xend2, self.radius + self.yend2, 1)
        bitmaptools.draw_line(self._bitmap, self.radius - self.xend, self.radius + self.yend, self.radius - self.xend2, self.radius + self.yend2, 1)
        self._draw_progress()

    def _draw_progress(self):

        if self.progress <= 0:  # Just draw the gauge (which is done now) and leave
            return

        #   Color in progress

        #print("drawing progress: {}".format(self.progress))
        #   Find progress end line
        prog = 315 - (self.progress * 270 / 100)  # what percent of gauge in degrees to fill in
        xs = self.radius + int(round(math.sin(math.radians(prog)) * (self.radius - 1), 0))
        ys = self.radius + int(round(math.cos(math.radians(prog)) * (self.radius - 1), 0))
        xe = self.radius + int(round(math.sin(math.radians(prog)) * (self.radius - self.width + 2), 0))
        ye = self.radius + int(round(math.cos(math.radians(prog)) * (self.radius - self.width + 2), 0))

        # Draw end line for progress value
        if self.progress != 100:  # @ 100%, no need to draw end line
            bitmaptools.draw_line(self._bitmap, xs, ys, xe, ye, 2)
        # Find a point just before the progress line as a start point for the boundary fill

        xp = self.radius + int(round(math.sin(math.radians(prog + 1)) * (self.radius - int(self.width/2)), 0))
        yp = self.radius + int(round(math.cos(math.radians(prog + 1)) * (self.radius - int(self.width/2)), 0))
        i = 1
        while self._bitmap[xp, yp] != 0 and i < 4:  #Search a little for a blank pixel
            i += 1
            xp = self.radius + int(round(math.sin(math.radians(prog + i)) * (self.radius - int(self.width/2)), 0))
            yp = self.radius + int(round(math.cos(math.radians(prog + i)) * (self.radius - int(self.width/2)), 0))

        bitmaptools.paint_fill(self._bitmap, xp, yp, 2, 0)


    def _draw_regress(self):

        #   Color in reverse progress

        #   Find progress end line
        prog = 315 - (self.progress * 270 / 100)  # what percent of gauge in degrees to fill in
        xs = self.radius + int(round(math.sin(math.radians(prog)) * (self.radius - 1), 0))
        ys = self.radius + int(round(math.cos(math.radians(prog)) * (self.radius - 1), 0))
        xe = self.radius + int(round(math.sin(math.radians(prog)) * (self.radius - self.width + 2), 0))
        ye = self.radius + int(round(math.cos(math.radians(prog)) * (self.radius - self.width + 2), 0))

        # Draw end line for progress value
        if self.progress != 100 and self.progress != 0:  # @ 100%, no need to draw end line
            bitmaptools.draw_line(self._bitmap, xs, ys, xe, ye, 0)
        if self.progress == 24:
            print(xs, ys, xe, ye)

        # Find a point just after the progress line as a start point to blank out to new progress line

        xp = self.radius + int(round(math.sin(math.radians(prog - 1)) * (self.radius - int(self.width/2)), 0))
        yp = self.radius + int(round(math.cos(math.radians(prog - 1)) * (self.radius - int(self.width/2)), 0))
        i = 1
        while self._bitmap[xp, yp] != 2 and i < 4:  #Search a little for a blank pixel
            i += 1
            xp = self.radius + int(round(math.sin(math.radians(prog - i)) * (self.radius - int(self.width/2)), 0))
            yp = self.radius + int(round(math.cos(math.radians(prog - i)) * (self.radius - int(self.width/2)), 0))

        bitmaptools.paint_fill(self._bitmap, xp, yp, 0, 2)


    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, new_progress):
        if new_progress >= self._progress:
            self._progress = new_progress
            self._draw_progress()
        else:
            self._progress = new_progress
            self._draw_regress()


    @property
    def progressColor(self):
        return self.progressColor

    @progressColor.setter
    def progressColor(self, new_progressColor):
        self._palette[2] = new_progressColor
