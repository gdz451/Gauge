# SPDX-FileCopyrightText: 2024 Your Name
#
# SPDX-License-Identifier: MIT

"""
`gauge`
================================================================================

Various common shapes for use with displayio - Gauge shape!

A 270-degree progress gauge for CircuitPython displays.

* Author(s): Your Name

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

try:
    from typing import Optional
except ImportError:
    pass

import math
import displayio
import bitmaptools

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/your_repo/Adafruit_CircuitPython_Display_Shapes.git"


class Gauge(displayio.TileGrid):
    """A 270-degree progress gauge.
    
    :param int x: The x-position of the center.
    :param int y: The y-position of the center.
    :param int radius: The radius of the gauge.
    :param int width: The width of the gauge arc (minimum 2).
    :param float progress: The progress percentage (0-100).
    :param int|None outline: The color of the gauge outline. Can be a hex value for a color or
                            ``None`` for no outline.
    :param int|None fill: The color to fill the progress. Can be a hex value for a color or
                         ``None`` for no fill.
    :param int|None background: The background color. Can be a hex value for a color or
                               ``None`` for transparent.
    """

    def __init__(
        self,
        x: int,
        y: int,
        radius: int,
        width: int,
        progress: float = 0,
        *,
        outline: Optional[int] = 0xFFFFFF,
        fill: Optional[int] = 0x00FF00,
        background: Optional[int] = 0x000000,
    ) -> None:
        self._x = x
        self._y = y
        self._radius = radius
        self._width = max(width, 2)  # Minimum width of 2
        self._progress = max(0, min(100, progress))  # Clamp between 0-100
        
        # Calculate bitmap dimensions
        tile_grid_width = 2 * self._radius + 1
        tile_grid_height = math.ceil(0.71 * self._radius) + self._radius + 1
        
        # Create bitmap and palette
        self._bitmap = displayio.Bitmap(tile_grid_width, tile_grid_height, 3)
        self._palette = displayio.Palette(3)
        self._palette[0] = background if background is not None else 0x000000
        self._palette[1] = outline if outline is not None else 0xFFFFFF
        self._palette[2] = fill if fill is not None else 0x00FF00
        
        # Calculate position offset
        x_offset = self._x - self._radius + 1
        y_offset = self._y - self._radius + 1

        super().__init__(
            self._bitmap, 
            pixel_shader=self._palette, 
            x=x_offset, 
            y=y_offset
        )

        self._draw_gauge()

    def _draw_gauge(self) -> None:
        """Draw the gauge outline using Bresenham's circle algorithm."""
        # Clear bitmap
        self._bitmap.fill(0)
        
        # Draw outer arc (octants 1-6, skipping 0 & 7 for 270-degree gauge)
        self._draw_arc(self._radius, 1)
        
        # Draw inner arc
        inner_radius = self._radius - self._width + 1
        self._draw_arc(inner_radius, 1)
        
        # Connect inner and outer arcs at endpoints
        outer_end_x = self._get_arc_endpoint_x(self._radius)
        outer_end_y = self._get_arc_endpoint_y(self._radius)
        inner_end_x = self._get_arc_endpoint_x(inner_radius)
        inner_end_y = self._get_arc_endpoint_y(inner_radius)
        
        # Draw connecting lines
        bitmaptools.draw_line(
            self._bitmap, 
            self._radius + outer_end_x, self._radius + outer_end_y,
            self._radius + inner_end_x, self._radius + inner_end_y, 
            1
        )
        bitmaptools.draw_line(
            self._bitmap, 
            self._radius - outer_end_x, self._radius + outer_end_y,
            self._radius - inner_end_x, self._radius + inner_end_y, 
            1
        )
        
        # Draw progress
        self._draw_progress()

    def _draw_arc(self, radius: int, color: int) -> None:
        """Draw an arc using Bresenham's circle algorithm."""
        x = 0
        y = radius
        d = 3 - 2 * radius

        while x <= y:
            # Draw 6 octants (excluding bottom octants 0 & 7)
            self._bitmap[-x + self._radius, -y + self._radius] = color  # Octant 3
            self._bitmap[x + self._radius, -y + self._radius] = color   # Octant 2
            self._bitmap[y + self._radius, x + self._radius] = color    # Octant 1
            self._bitmap[-y + self._radius, x + self._radius] = color   # Octant 4
            self._bitmap[-y + self._radius, -x + self._radius] = color  # Octant 5
            self._bitmap[y + self._radius, -x + self._radius] = color   # Octant 6

            if d <= 0:
                d = d + (4 * x) + 6
            else:
                d = d + 4 * (x - y) + 10
                y = y - 1
            x = x + 1

    def _get_arc_endpoint_x(self, radius: int) -> int:
        """Get the x endpoint of the arc."""
        x = 0
        y = radius
        d = 3 - 2 * radius

        while x <= y:
            if d <= 0:
                d = d + (4 * x) + 6
            else:
                d = d + 4 * (x - y) + 10
                y = y - 1
            x = x + 1
        return x - 1

    def _get_arc_endpoint_y(self, radius: int) -> int:
        """Get the y endpoint of the arc."""
        return self._get_arc_endpoint_x(radius)

    def _draw_progress(self) -> None:
        """Draw the progress fill."""
        if self._progress <= 0:
            return

        # Calculate progress end angle (315° - progress percentage of 270°)
        progress_angle = 315 - (self._progress * 270 / 100)
        
        # Calculate end line coordinates
        sin_val = math.sin(math.radians(progress_angle))
        cos_val = math.cos(math.radians(progress_angle))
        
        start_x = self._radius + int(round(sin_val * (self._radius - 1), 0))
        start_y = self._radius + int(round(cos_val * (self._radius - 1), 0))
        end_x = self._radius + int(round(sin_val * (self._radius - self._width + 2), 0))
        end_y = self._radius + int(round(cos_val * (self._radius - self._width + 2), 0))

        # Draw progress end line (unless at 100%)
        if self._progress != 100:
            bitmaptools.draw_line(self._bitmap, start_x, start_y, end_x, end_y, 2)

        # Find fill start point
        fill_angle = progress_angle + 1
        fill_x = self._radius + int(round(
            math.sin(math.radians(fill_angle)) * (self._radius - self._width // 2), 0
        ))
        fill_y = self._radius + int(round(
            math.cos(math.radians(fill_angle)) * (self._radius - self._width // 2), 0
        ))
        
        # Search for a blank pixel to start fill
        for i in range(1, 5):
            if self._bitmap[fill_x, fill_y] == 0:
                break
            fill_angle = progress_angle + i
            fill_x = self._radius + int(round(
                math.sin(math.radians(fill_angle)) * (self._radius - self._width // 2), 0
            ))
            fill_y = self._radius + int(round(
                math.cos(math.radians(fill_angle)) * (self._radius - self._width // 2), 0
            ))

        # Fill the progress area
        bitmaptools.paint_fill(self._bitmap, fill_x, fill_y, 2, 0)

    def _draw_regress(self) -> None:
        """Clear progress fill when progress decreases."""
        # Calculate progress end angle
        progress_angle = 315 - (self._progress * 270 / 100)
        
        # Calculate end line coordinates
        sin_val = math.sin(math.radians(progress_angle))
        cos_val = math.cos(math.radians(progress_angle))
        
        start_x = self._radius + int(round(sin_val * (self._radius - 1), 0))
        start_y = self._radius + int(round(cos_val * (self._radius - 1), 0))
        end_x = self._radius + int(round(sin_val * (self._radius - self._width + 2), 0))
        end_y = self._radius + int(round(cos_val * (self._radius - self._width + 2), 0))

        # Clear the end line (unless at 100% or 0%)
        if 0 < self._progress < 100:
            bitmaptools.draw_line(self._bitmap, start_x, start_y, end_x, end_y, 0)

        # Find fill start point for clearing
        fill_angle = progress_angle - 1
        fill_x = self._radius + int(round(
            math.sin(math.radians(fill_angle)) * (self._radius - self._width // 2), 0
        ))
        fill_y = self._radius + int(round(
            math.cos(math.radians(fill_angle)) * (self._radius - self._width // 2), 0
        ))
        
        # Search for a filled pixel to start clearing
        for i in range(1, 5):
            if self._bitmap[fill_x, fill_y] == 2:
                break
            fill_angle = progress_angle - i
            fill_x = self._radius + int(round(
                math.sin(math.radians(fill_angle)) * (self._radius - self._width // 2), 0
            ))
            fill_y = self._radius + int(round(
                math.cos(math.radians(fill_angle)) * (self._radius - self._width // 2), 0
            ))

        # Clear the progress area
        bitmaptools.paint_fill(self._bitmap, fill_x, fill_y, 0, 2)

    @property
    def x(self) -> int:
        """The x-position of the center of the gauge."""
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        self._x = x
        # Update TileGrid position
        super().__setattr__("x", x - self._radius + 1)

    @property
    def y(self) -> int:
        """The y-position of the center of the gauge."""
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        self._y = y
        # Update TileGrid position
        super().__setattr__("y", y - self._radius + 1)

    @property
    def radius(self) -> int:
        """The radius of the gauge."""
        return self._radius

    @property
    def width(self) -> int:
        """The width of the gauge arc."""
        return self._width

    @property
    def progress(self) -> float:
        """The progress percentage (0-100)."""
        return self._progress

    @progress.setter
    def progress(self, value: float) -> None:
        new_progress = max(0, min(100, value))  # Clamp between 0-100
        
        if new_progress >= self._progress:
            self._progress = new_progress
            self._draw_progress()
        else:
            self._progress = new_progress
            self._draw_regress()

    @property
    def outline(self) -> Optional[int]:
        """The outline color of the gauge."""
        return self._palette[1]

    @outline.setter
    def outline(self, color: Optional[int]) -> None:
        if color is not None:
            self._palette[1] = color

    @property
    def fill(self) -> Optional[int]:
        """The fill color of the progress."""
        return self._palette[2]

    @fill.setter
    def fill(self, color: Optional[int]) -> None:
        if color is not None:
            self._palette[2] = color

    @property
    def background(self) -> Optional[int]:
        """The background color of the gauge."""
        return self._palette[0]

    @background.setter
    def background(self, color: Optional[int]) -> None:
        if color is not None:
            self._palette[0] = color
