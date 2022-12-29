"""Object-oriented shapes extended from the widget class. These shapes have are
built-off from pyglet shapes, and are added to a batch for speedy rendering.
The vast majority of properties can be accessed and changed from creation.

Custom shapes can be easily created, mainly by subclassing the Shape class.
Optionally, you can subclass the Widget class, but you must do either one, but
not both, for futura to display them.
"""

import os
import sys
from cmath import tau

from pyglet.shapes import (Arc, BorderedRectangle, Circle, Ellipse, Line,
                           Polygon, Sector, Star, Triangle)

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
  
sys.path.append(parent)

from color import BLACK, WHITE, four_byte
from geometry import Pointlist

from widgets import Widget
from management import get_container


class Shape(Widget):
    """Primitive drawing Shape. This is subclassed by all shapes. You may or
    may not want to subclass this.
    """

    def __init__(self):
        """Initialize a shape. When using a shape, be sure to create vertex
        lists from pyglet.graphics.vertex_list(), then draw them with pyglet
        rendering. Refer to the pyglet.shapes module for more information.

        A shape should not need an update function. Instead, put all of the
        properties as function-defined ones. This saves time and GPU. Also,
        instead of having x and y properties seperately, use a Point or a
        Pointlist. These are much faster performance-wise and more neater.

        A shape should look like one from the pyglet.shapes module, but should
        be drawn with pyglet rendering. It should subclass a widget or a shape,
        but that is not necessary. If you do, however, keep in mind that the
        events of a widget will be dispatched, like draw and update. You can
        also add the shape's vertex list to a pyglet.graphics.Batch() for
        faster performance and draw the batch instead of drawing the vertex
        list.

        You can use pyglet rendering like this:

        with arcade.get_window().ctx.pyglet_rendering():
            # Do something

        Alternatively the arcade.get_window() part can be replaced with the
        window property of the widget. This can save time.

        See https://pyglet.readthedocs.io/en/latest/modules/graphics/index.html
        """

        Widget.__init__(self)

    def _update_position(self, x, y):
        """Update the position of the shape. This is called internally
        whenever position properties are modified.
        """

        self.shape.x = x
        self.shape.y = y

    def draw(self):
        """Draw the shape with pyglet rendering. You may need to override this
        when creating your custom shapes.

        This was deprecated in favor of pyglet batching.
        """

        # with self.window.ctx.pyglet_rendering():
        #     self.shape.draw()

    def _get_x(self):
        """X position of the shape.

        type: property, int
        """

        return self.shape.x

    def _set_x(self, x):
        self.shape.x = x

    def _get_y(self):
        """Y position of the shape.

        type: property, int
        """

        return self.shape.y

    def _set_y(self, y):
        self.shape.y = y

    def _get_alpha(self):
        """Alpha, opacity, or transparency of the shape. You may need to
        override this if creating your own custom shapes. An alpha of zero is
        completely transparent and invisible. An alpha of 255 is completely
        opaque.

        Values below zero or above 255 are caught and fixed.

        type: property, int
        """

        return self.shape.opacity

    def _set_alpha(self, alpha):
        if alpha > 255: alpha = 255
        if alpha < 0: alpha = 0

        self.shape.opacity = alpha

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    alpha = property(_get_alpha, _set_alpha)

    def delete(self):
        """Delete the shape and its events. The shape is not drawn. You may
        need to override this if creating your own custom shapes.
        """

        self.shape.delete()


_Circle = Circle
_Ellipse = Ellipse
_Sector = Sector
_Line = Line
_Triangle = Triangle
_Star = Star
_Polygon = Polygon
_Arc = Arc


class Rectangle(Shape):
    """A rectangular shape."""

    def __init__(self, x, y, width, height, border=1,
                 colors=(four_byte(WHITE), four_byte(BLACK))):

        """Create a rectangle.

        x - x position of rectangle
        y - y position of rectangle
        width - width of rectangle
        height - height of rectangle
        border - border width. The bigger this value is, the more three
                 dimensional effect there will be. If set to 0 there will be no
                 effect.
        colors - color of the rectangle in RGBA as a tuple of three ints. There
                 are two tuples in a list, the first one for the shape fill and
                 the second one for the outline color. The default for this is:
                 [(255, 255, 255, 255), (0, 0, 0, 255)]

        parameters: int, int, int, int, int, list [(RGB), (RGB)], Label
        """

        self.shape = BorderedRectangle(
                            x, y, width, height,
                            border, colors[0], colors[1],
                            batch=get_container().batch
                        )

        Shape.__init__(self) # Do this after defining self.shape

        self.width_ = width
        self.height_ = height
        self.border = border
        self.colors = colors

    def _get_width(self):
        """Width of the rectangle.

        type: property, int or float
        """

        return self.width_

    def _set_width(self, width):
        self.width_ = width

        self.shape.width = width

    def _get_height(self):
        """Height of the rectangle.

        type: property, int or float
        """

        return self.height_

    def _set_height(self, height):
        self.height_ = height

        self.shape.height = height

    width = property(_get_width, _set_width)
    height = property(_get_height, _set_height)


class Circle(Shape):
    """A circular shape."""

    def __init__(self, x, y, radius, segments=None, color=BLACK):
        """Create a circle.

        x - x position of the circle
        y - y position of the circle
        radius - radius of the circle (see radius)
        segments - number of segments of the circle. This is the number of
                   distinct triangles should the circle be formed from. If not
                   specified it is calculated with

                   max(14, int(radius ÷ 1.25))
        color - color of the circle in RGB as a tuple of three ints

        parameters: int, int, int, int, tuple (RGB)
        """

        if not segments:
            segments = max(14, int(radius / 1.25))

        self.shape = _Circle(x, y, radius, segments, color, batch=get_container().batch)

        Shape.__init__(self, x, y)

        self.radius = radius
        self.color = color

    def _get_radius(self):
        """Radius of the circle (the distance from the center to the edge). The
        radius is the same throughout the whole circle.

        type: property, int
        """

        return self.shape.radius

    def _set_radius(self, radius):
        self.shape.radius = radius

    def _get_segments(self):
        """Number of segments in the circle. This is the number of distinct
        triangles that the circle is made from. On default, it is calculated
        by:

        max(14, int(radius ÷ 1.25))

        Note this must be used because you cannot draw a perfect circle on a
        pixeled monitor.

        returns: int
        """

        return self.shape._segments

    radius = property(_get_radius, _set_radius)
    segments = property(_get_segments)


class Ellipse(Shape):
    """An elliptical shape."""

    def __init__(self, x, y, a, b, color=BLACK):
        """Create a ellipse. This can also be called Oval.

        x - x position of the ellipse
        y - y position of the ellipse
        a - semi-major axes of the ellipse. If this and height are equal, a
            circle will be drawn. To draw a circle, set the a and b equal and
            divide their desired width and height by two for the radius.
        b - semi-minor axes of the ellipse. See a for more information.
        color - color of the ellipse in RGB as a tuple of three ints

        parameters: int, int, int, int, tuple (RGB)

        """

        self.shape = _Ellipse(x, y, a, b, color, batch=get_container().batch)

        Shape.__init__(self, x, y)

        self.a = a
        self.b = b

    def _get_a(self):
        """Semi-major axes of the ellipse.

        type: property, int
        """

        return self.shape.a

    def _set_a(self, a):
        self.shape.a = a

    def _get_b(self):
        """Semi-major axes of the ellipse.

        type: property, int
        """

        return self.shape.b

    def _set_b(self, b):
        self.shape.b = b

    a = property(_get_a, _set_a)
    b = property(_get_b, _set_b)


Oval = Ellipse


class Sector(Shape):
    """A sector or pie slice of a circle."""

    def __init__(self, x, y, radius, segments=None,
                 angle=tau, start=0, color=BLACK):

        """Create a sector. A sector is essentially a slice of a circle. The
        sector class was created from the arc class in pyglet.

        x - x position of the sector
        y - y position of the sector
        radius - radius of the sector (see _set_radius)
        segments - number of segments of the sector. This is the number of
                   distinct triangles should the sector be formed from. If not
                   specified it is calculated with

                   max(14, int(radius ÷ 1.25))
        angle - angle of the sector in radians. This defaults to tau, which
                is approximately equal to 6.282 or 2π
        start - start angle of the sector in radians

        parameters: int, int, int, int, int
        """

        self.shape = _Sector(x, y, radius, segments, angle, start, color, batch=get_container().batch)

        Shape.__init__(self)

        self.radius = radius
        self.segments = segments
        self.rotation = angle
        self.start = start
        self.color = color

    def _get_radius(self):
        """Radius of the sector. This is the distance from the center of the
        circle to its edge.

        type: property, int
        """

        return self.shape.radius

    def _set_radius(self, radius):
        self.shape.radius = radius

    def _get_start(self):
        """Start angle of the sector.

        type: property, int
        """

        return self.shape.start_angle

    def _set_start(self, start):
        self.shape.start = start

    def _get_segments(self):
        """Number of segments in the sector. This is the number of distinct
        triangles that the sector is made from. On default, it is calculated
        by:

        max(14, int(radius ÷ 1.25))

        Note this must be used because you cannot draw a perfect sector on a
        pixeled monitor.

        type: property, int
        """

        return self.shape._segments

    radius = property(_get_radius, _set_radius)
    start = property(_get_start, _set_start)
    segments = property(_get_segments)


class Line(Shape):
    """A line shape."""

    def __init__(self, point1, point2, width=1, color=BLACK):
        """Create a line. Unlike other shapes, a line has a start point and an
        endpoint.

        point1 - first start coordinate pair of line
        point2 - second end coordinate pair of line
        width - width, weight or thickness
        color - color of the line in RGB in a tuple of three ints

        parameters: Point, Point, int, tuple (RGB)
        """

        # Normally we don't format like this. But it makes it neater and more
        # consistent when we use three lines instead of one.

        self.shape = _Line(point1.x, point1.y,
                           point2.x, point2.y,
                           width, color, batch=get_container().batch)

        Shape.__init__(self)

        self._point1 = point1
        self._point2 = point2
        self.width = width
        self.color = color

    def _get_point1(self):
        """First Point of the line.

        type: property, Point
        """

        # We can't return thea new Point, as it would have a different id

        return self._point1

    def _set_point1(self, point1):
        self._point1 = point1

        self.shape.x1 = point1.x
        self.shape.y1 = point1.y

    def _get_point2(self):
        """Second Point of the line.

        type: property, Point
        """

        # We can't return thea new Point, as it would have a different id

        return self._point2

    def _set_point2(self, point2):
        self._point2 = point2

        self.shape.x2 = point2.x
        self.shape.y2 = point2.y

    def _get_width(self):
        """Width of the line. This has an alias called thickness and another
        called weight.

        type: property, int
        """

        return self.shape._width

    def _set_width(self, width):
        self.shape._width = width

    point1 = property(_get_point1, _set_point1)
    point2 = property(_get_point2, _set_point2)
    width = property(_get_width, _set_width)

    # Alias
    thickness = width
    weight = width


class Triangle(Shape):
    """A triangular shape."""

    def __init__(self, points, color=BLACK):
        """Create a triangle.

        points - pointlist of the triangle
        color - color of of the triangle in RGB as a tuple of three ints

        parameters: Pointlist, tuple (RGB)
        """

        self.shape = _Triangle(*points, color, batch=get_container().batch)

        Shape.__init__(self)

        self._points = Pointlist(points)
        self.color = color

    def _get_points(self):
        """Points of the triangle. This is listed as point1, point2, and
        point3, which each have their x and y coordinates.

        Asserts that the pointlist is valid.

        returns: Pointlist
        """

        return self._points

    def _set_points(self, points):
        assert len(points) > 3, (
            "The points of the Pointlist specified must be labeled as point1,"
            "point2, and point3."
        )

        self._points = points

        self.shape.x1 = points[0].x
        self.shape.y1 = points[0].x
        self.shape.x2 = points[1].x
        self.shape.y2 = points[1].x
        self.shape.x3 = points[2].x
        self.shape.y3 = points[2].x

    points = property(_get_points, _set_points)


class Star(Shape):

    def __init__(
                 self, x, y, outer, inner, spikes=5,
                 rotation=0, color=four_byte(BLACK), opengl_error=True
                ):
        """Create a star. You can make a n-sided polygon from this, by setting
        the outer radius to nothing.

        x - x position of star
        y - y position of star
        outer - outer diameter of spike
        inner - inner diameter of spike
        spikes - number of spikes. Defaults to 5 (a plain star).
        rotation - rotation of the star in degrees. A rotation of 0 degrees
                   will result in one spike lining up with the x axis in
                   positive direction.
        color - color of the star in RGBA as a tuple of four ints. Defaults to
                (255, 255, 255, 255)
        opengl_error - checks whether or not the outer diameter is greater
                       than the inner diameter. This is not supposed to be like
                       this, but results in interesting patterns. Defaults to
                       True.

        parameters: int, int, int, int, int, int, tuple (RGB), bool
        """

        if opengl_error:
            assert outer > inner, (
                "The outer diameter of the star must be greater than its inner "
                "diameter. You can turn this off by setting the opengl_error "
                "parameter to False. Switching this off is programmatically "
                "incorrect, but results in interesting patterns."
            )

        self.shape = _Star(x, y, outer, inner, spikes, rotation, color, batch=get_container().batch)

        Shape.__init__(self)

        self.x = x
        self.y = y
        self.outer = outer
        self.inner = inner
        self.spikes = spikes
        self.rotation = rotation
        self.color = color

    def _get_outer(self):
        """Outer diameter of each spike in the star.

        type: property, int
        """

        return self.shape.outer_radius

    def _set_outer(self, diameter):
        self.shape.outer_radius = diameter

    def _get_inner(self):
        """Inner diameter of each spike in the star.

        type: property, int
        """

        return self.shape.inner_radius

    def _set_inner(self, diameter):
        self.shape.inner_radius = diameter

    def _get_spikes(self):
        """Number of spikes in the star. This typically should be set to five.

        type: property, int
        """

        return self.shape.num_spikes

    def _set_spikes(self, spikes):
        self.shape.num_spikes = spikes

    outer = property(_get_outer, _set_outer)
    inner = property(_get_inner, _set_inner)
    spikes = property(_get_spikes, _set_spikes)


class Polygon(Shape):

    def __init__(self, *coordinates, color=BLACK):
        self.shape = _Polygon(*coordinates, color, batch=get_container().batch)

        Shape.__init__(self)

        self.coordinates = list(coordinates)
        self.color = color

    def update(self):
        self.shape.coordinates = self.coordinates
        self.shape.color = self.color


class Arc(Shape):

    def __init__(self, x, y, radius, segments=None,
                 angle=tau, start=0, closed=False, color=BLACK):

        self.shape = _Arc(x, y, radius, segments, angle, start, closed, color, batch=get_container().batch)

        Shape.__init__(self)

        self.x = x
        self.y = y
        self.radius = radius
        self.segments = segments
        self.rotation = angle
        self.start = start
        self.closed = closed
        self.color = color

    def update(self):
        self.shape.x = self.x
        self.shape.y = self.y
        self.shape.radius = self.radius
        self.shape.segments = self.segments
        self.shape.angle = self.rotation
        self.shape.start = self.start
        self.shape.closed = self.closed
