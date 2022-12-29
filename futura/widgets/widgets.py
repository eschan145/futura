"""GUI interface and widgets. Documentation is found throughout the file,
though in some areas it may be obsolete or incomplete.

More than meets the eye in this example. To see all features, look at the source
code of each widget. This includes several different types of interactive
widgets and displays an example at the end. It also includes API for creating
your own widgets, which is quite easy to do. Everything is object-oriented,
which aids in accessing properties and setting them. Nearly all properties can
be accessed and set from creation. These built-in widgets have plenty of
documentation and functions.

Several widgets are provided to use. These include
:py:class:`~futura.widgets.Image`, :py:class:`~futura.widgets.Label`,
:py:class:`~futura.widgets.Button`, :py:class:`~futura.widgets.Slider`,
:py:class:`~futura.widgets.Toggle`, :py:class`~futura.widgets.Entry`,
and various shapes. Like most projects based off pyglet, in this GUI toolkit,
all widgets subclass a base widget class, which dispatches events to them.

This uses the well-known and high-end `pyglet <https://pyglet.org/>`_ and
`arcade <https://arcade.academy/>`_ libraries, which are still active and
working today.

Arcade does have a separate GUI toolkit implemented, but it has fewer features
compared to this. It does have some special enhancements and functionality that
is not provided here, such as the ability to place widgets with layouts and
groups. This is being developed here.

Contributions are welcome. Visit my GitHub repository at
https://github.com/eschan145/futura. Feel free to file a pull request or an
issue.

Code and graphics by Ethan Chan

**GitHub**: `eschan145`
**Discord**: `EthanC145#8543`

Contact me at esamuelchan@gmail.com
"""

from html import entities
from html.parser import HTMLParser
from re import compile
from typing import Tuple
from webbrowser import open_new
from inspect import currentframe
from typing import Optional
import pyglet
from arcade import (ShapeElementList, create_rectangle_outline,
                    draw_rectangle_outline, get_window, load_texture)
from pyglet.event import EventDispatcher
from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.text import HTMLLabel, decode_attributed
from pyglet.text.caret import Caret as _Caret
from pyglet.text.layout import IncrementalTextLayout

from futura.color import (BLACK, COOL_BLACK, DARK_GRAY, DARK_SLATE_GRAY, RED,
                          four_byte)
from futura.file import (blank1, entry_focus, entry_hover, entry_normal, knob,
                         slider_horizontal, toggle_false, toggle_false_hover,
                         toggle_true, toggle_true_hover, widgets)
from futura.geometry import Point, are_rects_intersecting, get_distance
from futura.key import (ALT, CONTROL, ENTER, KEY_LEFT, KEY_RIGHT,
                        MOTION_BACKSPACE, MOTION_BEGINNING_OF_FILE,
                        MOTION_BEGINNING_OF_LINE, MOTION_COPY, MOTION_DELETE,
                        MOTION_DOWN, MOTION_END_OF_FILE, MOTION_END_OF_LINE,
                        MOTION_LEFT, MOTION_NEXT_WORD, MOTION_PREVIOUS_WORD,
                        MOTION_RIGHT, MOTION_UP, MOUSE_BUTTON_LEFT, SHIFT,
                        SPACE, A, B, C, I, Keys, V, X)
from futura.management import (clipboard_append, clipboard_get, get_container,
                               resize_bordered_image, resize_bordered_images)

pyglet.options["debug_gl"] = False

MAX = 2 ** 32

# Sides

LEFT = "left"
CENTER = "center"
RIGHT = "right"

TOP = "top"
BOTTOM = "bottom"

# Callbacks
SINGLE = 1
DOUBLE = 2
MULTIPLE = 3

SIMPLE = "simple"

KEYBOARD = "keyboard"
MOUSE = "mouse"
PROGRAM = "program"

DISABLE_ALPHA = 160 # Alpha of disabled widget
FOCUS_SIZE = 1.05 # [DEPRECATED]

ENTRY_BLINK_INTERVAL = 0.5

TOGGLE_VELOCITY = 2
TOGGLE_FADE = 17

SLIDER_VELOCITY = 10
KNOB_HOVER_SCALE = 1

SCROLLER_PADDING = 20

HORIZONTAL = "horizontal"
VERTICAL = "vertical"

DEFAULT_FONT_FAMILY = "Montserrat"
DEFAULT_FONT_SIZE = 12

DEFAULT_FONT = ["Montserrat", 12]

DEFAULT_LABEL_COLORS = [BLACK, (COOL_BLACK, DARK_SLATE_GRAY, DARK_GRAY)]

DEFAULT_IMAGE_ATTRIBUTES = \
    [
        "width",
        "height"
    ]

def _exclude(exclusions):
    import types

    # Add everything as long as it's not a module and not prefixed with _
    functions = [name for name, function in globals().items()
                 if not (name.startswith('_') or isinstance(function, types.ModuleType))]

    # Remove the exclusions from the functions
    for exclusion in exclusions:
        if exclusion in functions:
            functions.remove(exclusion)

    del types  # Deleting types from scope, introduced from the import

    return functions


# The "_" prefix is important to not add these to the __all__
# _exclusions = ["function1", "function2"]
# __all__ = _exclude(_exclusions)


class WidgetsError(Exception):
    """Widgets error. When creating custom widgets, this can be invoked. Only
    use this if you need to, like if it is going to cause something to hang or
    crash, or it raises an unhelpful error. Making this unnecessary will be
    annoying in some scenarios. If the user absolutely wants to do something
    and this error keeps on being raised, this is aggravating and he will have
    to edit the source code.
    """


class Font:
    """An object-oriented Font."""

    def __init__(self,
                 family=DEFAULT_FONT_FAMILY,
                 size=DEFAULT_FONT_SIZE
                ):

        """Initialize an object-oriented Font. This is an experimental feature
        and has no effect.

        :Parameters:
            ``family`` : ``str``
                Family or name of the font (style).
            ``size`` : ``int`` or ``float``
                Size of the font. This is *not in pixels*.
        """

        self.family = family
        self.size = size

        self.list = [self.family, self.size]

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, index, item):
        self.list[index] = item


default_font = Font()


class Rect:
    """Rect class for bounding box and collision calculations. Supports border
    properties, and is subclassed by the widget class. Positioning and related
    properties are defined here.
    """

    _x = 0
    _y = 0

    _width = 0
    _height = 0

    _point = Point(0, 0)
    
    _created = False
    _need_update_position = False

    children = []

    def _update_position(self, x, y):
        """Update the position of the widget. This is called whenever position
        properties are changed, and should be made internally in the widget.
        It should set the component properties of the widget to the given
        coordinates.
        """

    def _update_size(self, width, height):
        """Update the size of the widget. This is called whenever size
        properties are changed, and should be made internally in the widget.
        """

    def _get_x(self):
        """Center x position of the rect.

        :type: ``int``
        """

        return self._x

    def _set_x(self, x):
        self._x = x

        # Don't let this fire _update_position on initialization. Usually it
        # a widget is created in the _create function. So _update_position
        # would raise an AttributeError.

        # if currentframe().f_back.f_code.co_name != "__init__":
        
        if self._created:
            self._update_position(x, self.y)
        
        else:
            self._need_update_position = True

    def _get_y(self):
        """Center y position of the rect.

        :type: ``int``
        """

        return self._y

    def _set_y(self, y):
        self._y = y

        # if currentframe().f_back.f_code.co_name != "__init__":
        
        if self._created:
            self._update_position(self.x, y)
        
        else:
            self._need_update_position = True

    def _get_point(self):
        """Center x and y position of the widget, as a Point.

        :type: :py:class:`~futura.Point`
        """

        return self._point

    def _set_point(self, point):
        self._point = point

        self.x = point.x
        self.y = point.y

    def _get_left(self):
        """Left x position of the widget.

        :type: ``int``
        """

        return self.x - self.width / 2

    def _set_left(self, left):
        self.x = left + self.width / 2 # Opposite, if you think about it

    def _get_right(self):
        """Right x position of the widget.

        :type: ``int``
        """

        return self.x + self.width / 2

    def _set_right(self, right):
        self.x = right - self.width / 2

    def _get_top(self):
        """Top y position of the widget.

        :type: ``int``
        """

        return self.y + self.height / 2

    def _set_top(self, top):
        self.y = top - self.height / 2

    def _get_bottom(self):
        """Bottom y position of the widget.

        :type: ``int``
        """

        return self.y - self.height / 2

    def _set_bottom(self, bottom):
        self.y = bottom + self.height / 2

    def _get_width(self ):
        """Width of the widget.

        This property is read-only.

        :type: ``int``
        """

        if self.children:
            if hasattr(self.children[0], "width"):
                return self.children[0].width
            elif hasattr(self.children[0], "content_width"):
                return self.children[0].content_width

        return self._width

    def _set_width(self, width):
        if currentframe().f_back.f_code.co_name != "__init__":
            self._update_size(width, self.height)

            self._width = width

    def _get_height(self):
        """Height of the widget.

        This property is read-only.

        :type: ``int``
        """

        if self.children:
            if hasattr(self.children[0], "height"):
                return self.children[0].height
            elif hasattr(self.children[0], "content_height"):
                return self.children[0].content_height

        return self._height

    def _set_height(self, height):
        if currentframe().f_back.f_code.co_name != "__init__":
            self._update_size(self.width, height)

            self._height = height

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    point = property(_get_point, _set_point)
    left = property(_get_left, _set_left)
    right = property(_get_right, _set_right)
    top = property(_get_top, _set_top)
    bottom = property(_get_bottom, _set_bottom)
    width = property(_get_width, _set_width)
    height = property(_get_height, _set_height)

    def _check_collision(self, point):
        """Check if an ``x`` and ``y`` position exists within the widget's
        hitbox. This is an alternative to
        :py:meth:`~futura.widgets.Rect.check_collision`, and should only
        be used if you are not using any children (ex.
        :py:class`~futura.widgets.Label` widget), or they do not have ``left``,
        ``right``, ``top``, and ``bottom`` properties.

        TODO: replace ``x`` and ``y`` parameters with :py:class:`~futura.Point`
              (COMPLETED)

        :Parameters:
            ``point`` : :py:class:`~futura.Point`
                :py:class:`~futura.Point` to check for collision with.

        :rtype: ``bool``
        :returns: Whether the point exists inside the rect.
        """

        return (0 < point.x - self.x < self.width and
                0 < point.y - self.y < self.height)

    def check_collision(self, point):
        """Check if an ``x`` and ``y`` position exists within the widget's
        hitbox. This should be used if you are using children, or if they do
        have ``left``, ``right``, ``top``, and ``bottom`` properties, or with
        an underscore as a prefix.

        TODO: replace ``x`` and ``y`` parameters with :py:class:`~futura.Point` (COMPLETED)

        :Parameters:
            ``point`` : :py:class:`~futura.Point`
                :py:class:`~futura.Point` to check for collision with.

        :rtype: ``bool``
        :returns: Whether or not the point exists inside the rect.
        """

        return point.x > self.left and point.x < self.right and \
               point.y > self.bottom and point.y < self.top

    def is_colliding(self, rect):
        """Check if the :py:class`~futura.widgets.Rect` is colliding with
        a given one. It uses the :py:func:`~futura.are_rects_intersecting`
        function in the :py:mod:`~futura.geometry` module.

        :Parameters:
            ``rect`` : :py:class:`~futura.widgets.Rect`
                Rect to check for collision with.

        :rtype: ``bool``
        :returns: Whether or not the rect is colliding with the given one.
        """

        return are_rects_intersecting(self, rect)

    def draw_bbox(self, width=1, padding=0):
        """Draw the bounding box of the widget. The drawing is cached in a
        :py:class:`~arcade.ShapeElementList` so it won't take up more time.
        This can also be called
        :py:meth:`~futura.widgets.Rect.draw_hitbox` or
        :py:meth:`~futura.widgets.Rect.draw_hit_box`.

        :Parameters:
            ``width`` : ``int``
                Width or thickness of the bounding box outline. Defaults to
                ``1``.
            ``padding`` : ``int``
                Padding around the widget. Defaults to ``0``.
        """

        if self.shapes is None:
            shape = create_rectangle_outline(self.x, self.y,
                                             self.width + padding,
                                             self.height + padding,
                                             RED, width
                                            )

            self.shapes = ShapeElementList()
            self.shapes.append(shape)

            self.shapes.center_x = self.x
            self.shapes.center_y = self.y

    draw_hitbox = draw_bbox # Alias
    draw_hit_box = draw_bbox

    def snap_to_point(self, point, distance, move=True):
        """Snap the widget's position to a :py:class:`~futura.Point`. This is
        useful in dragging widgets around, so snapping can make them snap to
        position if they are aligned to a certain widget, etc.

        :Parameters:
            ``point`` : :py:class:`~futura.Point`
                Point for the widget to snap to. Typically should be a mouse
                position.
            ``distance`` : ``int``
                Distance of the snapping. This gives the user less freedom but
                makes it easier for larger snaps.
            ``move`` : ``True``
                Move the widget towards the snapping point. If this is
                ``False``, then coordinates will be returned. Defaults to
                ``True``. You may want to add an effect to this.

        :rtype: ``bool``
        :returns: Whether or not the widget was snapped to position
        """

        if get_distance(self, point) <= distance:
            if move:
                self.x = point.x
                self.y = point.y

                return True

            return point


class Widget(Rect, EventDispatcher):
    """Create a user interface GUI widget. This is a high-level class and is
    not suitable for very complex widgets. It comes with built-in states,
    which can be accessed just by getting its properties. Dispatching events
    makes subclassing a widget and creating your own very easy.

    Widgets must have several things.

    1. Specified main widget in widget parameter

       This part must be set. Some different elements are supported by futura,
       including :py:class:`~pyglet.text.layouts.TextLayout`s and
       :py:class:`~arcade.Sprites`. Basically, anything with ``_width`` and
       ``_height`` or ``content_width`` and ``_content_height`` properties.

       It is the widget that takes the hitbox points for collision detection.

    2. Children (sometimes)

       Widgets should have children if they have elements from other widgets.
       Very primitive elements are not necessary for this. A widget with
       children is recognized as a group of widgets, and therefore can have
       focus traversal. Single widgets, without any children, are not
       recognized by focus traversal.

    3. Drawing and update functions

       Widgets must have a draw function defined. It may be blank. In the
       future this may be made optional. They should also have an update
       function.

    If you have an error, double-check your code is using the right datatype
    or the value is valid.

    Plenty of things are built-in here. For example, you can access the current
    window just by using the window property. Or the key state handler
    with the :py:attr:`~futura.widgets.Widget.key` property. You can draw the
    hitbox of a widget for debugging, and performance is not lost because the
    drawing is cached. When removing a widget, use its
    :py:meth:`~futura.widgets.Widget.delete` function.

    There are dozens and dozens of properties for the widget. You can add a
    :py:class`~arcade.Shape` to its :py:class:`~arcade.ShapeElementList`, in
    the :py:attr:`~futura.widgets.Widget.shapes` property. Key state handlers
    are already built-in, along with mouse state handlers.

    You can access the widget's state by properties. Several built-in states
    are supported: ``normal``, ``hover``, ``press``, ``disable``, and
    ``focus``. A disabled widget cannot have focus. It is highly not
    recommended to change any of these properties, as these may lead to drawing
    glitches. One exception is when defining them in the beginning.

    TODO: of course, there are many enhancements and other things that need to
          be worked on for the built-in widgets. If you would like to work on
          these post your enhancements in the discussions.

        1. Adding ``left``, ``right``, ``top``, and ``bottom`` properties to
           widgets. This has been implemented in arcade
           :py:class`~arcade.Sprite` and should be for this too. It can be
           useful for enhanced positioning.

           - Create a ``_set_coords()`` function that is called whenever border
             position properties are modified
           - Add setting properties for each widget. This is not recommended
             because it's a hassle to code and will take up more space.
           - Make functions like ``set_border_coords``

           (COMPLETED)

        2. Move documentation from ``setters`` to ``getters`` for properties.
           I think this is a big stretch; it will cost me literally thousands
           of deletions on my repository. (or not)

           Actually not really. I was able to do this without too many
           deletions.
    """
    
    _attributes = {}
    application = None
    
    def __init__(self, widget=None, x=0, y=0):
        """Here's an example of a widget. This ``_colorchooser`` dispatches
        events, so a widget that subclasses it can use them.

        ```
        >>> class _Colorchooser(Widget):

                def __init__(self):
                    self.image = Image("colorchooser.png")

                    Widget.__init__(self)

                def on_press(self, x, y, buttons, modifiers):
                    color = self.get_color_from_pos(x, y)
                    self.dispatch_event("on_color_pick", color)

                def get_color_from_pos(self, x, y):
                    # Get a color from x, y
                    pass

        >>> _Colorchooser.register_event_type("on_color_pick")
        ```

        On lines 1-5 we create and initialize the widget. An event is
        dispatched by the widget called on_press when the widget is pressed.
        This _colorchooser widget then dispatches an event, called
        ``on_color_pick``, with its parameters listed beside it. At the end of
        defining the widget you have to register it, so we do that in the last
        line. This just confirms to pyglet that we're creating an event.

        Now, the actual colorchooser would look like this::

        >>> class Colorchooser(_Colorchooser):

                def __init__(self):
                    _Colorchooser.__init__(self)

                def on_color_pick(self, color):
                    print("Color picked: ", color)

        -----------------------------------------------------------------------

        :Parameters:
            ``x`` : ``int``
                Initial ``x`` position of the widget. This can be modified
                later on. This parameter is only used to call
                :py:meth:`~futura.widgets.Rect._update_position` right away.
        widget - widgets and components to be added. If you are creating
                 components, add them before initializing the widget. These
                 help calculate the hitbox or bounding box.
        image - image to be displayed. Use this only for defining an image
                widget, though one is already pre-defined.
        scale - scale of the widget. This has been deprecated, as setting this
                to a value different that one will mess up the widget's bbox
        frame - not yet implemented. This is supposed to have a frame widget,
                which stores multiple widgets. It's similar to tkinter's Frame.

        parameters:
            widgets: tuple
            image - str (filepath) or arcade.Texture
        """

        # We don't need to initialize Rect because it does not have an __init__
        # function. It's just a wrapper for hitbox and coordinate math.

        # Super messy, but it works

        # for var in vars(self):
        #     # if hasattr(var, "width") or \
        #     #     hasattr(var, "content_width"):
        #     #     if hasattr(var, "height") or \
        #     #     hasattr(var, "content_height"):
        #     #         if hasattr(var, "content_width") or \
        #     #             hasattr(var, "content_height"):
        #     #             self.width = var.content_width
        #     #             self.height = var.content_height

        #     #         else:
        #     #             self.width = var.width
        #     #             self.height = var.height

        #     attribute = getattr(self, var)

        #     # TODO: support more instances

        #     if isinstance(attribute, Widget) or isinstance(var, Sprite):
        #         self.width = attribute.width
        #         self.height = attribute.height

        #     elif isinstance(attribute, TextLayout):
        #         pass

        #         # Doesn't work with widgets with images and buttons

        #         # self.width = attribute.content_width
        #         # self.height = attribute.content_height

        self.hover = False
        self.press = False
        self.disable = False
        
        self.drag = False

        self._left = None
        self._right = None
        self._top = None
        self._bottom = None

        self._children = []
        self.parent = None

        self.frames = 0

        self.last_press = Point(0, 0)

        self.keys = Keys()
        self.shapes = None

        self.window = get_window()

        self.window.push_handlers(
            self.on_key_press,
            self.on_key_release,
            self.on_mouse_motion,
            self.on_mouse_press,
            self.on_mouse_release,
            self.on_mouse_scroll,
            self.on_mouse_drag,
            self.on_text_motion_select,
            self.on_deactivate,
            self.on_update
        )
        
        self._update_position(x, y)

    def __getitem__(self, attribute):
        if attribute in self._attributes:
            return self._attributes[attribute]

    def __setitem__(self, attribute, value):
        self._attributes[attribute] = value

    @property
    def focus(self):
        """Focus of the widget. Setting the focus for a widget removes focus
        for all other widgets. If the focus is false, the previous widget will
        attempt to receive focus.

        Raises a :py:exc:`~ValueError` if there are one or fewer widgets in the
        widget list and ``focus`` is set to False. Technically, this should do
        nothing if raised.

        See :py:meth:`~futura.widgets.Widget.on_focus` for details.

        .. hint::

            You can set the focus state of the widget with this property. Any
            other widgets will lose focus; only one widget can have focus at
            the time.

            Additionally, *focus can only be added to a widget with children*.
            This command will do nothing if the widget has no children at all.
        """

        return self.application.focus

    @focus.setter
    def focus(self, focus):
        if focus:
            self.application.focus = self

            self.dispatch_event("on_focus", PROGRAM)

            # Remove all other widgets' focus

            for widget in self.application.added_widgets:
                if widget.children and not widget == self:
                    widget.focus = False

        else:
            if len(self.application.added_widgets) <= 1:
                raise ValueError("You must have at least two widgets added "
                                 "when setting focus of a widget to False. "
                                 "The previous widget should be set focus."
                                )

            index = self.application.added_widgets.index(self)

            self.application.focus = self.application.added_widgets[index - 1]

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

        if children and len(children) > 1:
            for child in children:
                child.application = self.application
                child.parent = self
                
                self.application._widgets.append(child)

    def delete(self):
        """Delete this widget and remove it from the event stack. The widget
        is not drawn and will not be accepting any events. You may want to
        override this if creating your own custom widget.

        You may not want to use this for shapes.

        If overriding this, you should remove all bindings of the widget and
        all events.
        """

        self.bindings = []
        self.disable = True
        self.focus = False

        self.window.remove_handlers(
            self.on_key_press,
            self.on_key_release,
            self.on_mouse_motion,
            self.on_mouse_press,
            self.on_mouse_release,
            self.on_mouse_scroll,
            self.on_mouse_drag,
            self.on_text_motion_select,
            self.on_deactivate,
            self.on_update
        )

    def draw(self):
        pass

    def on_key_press(self, keys, modifiers):
        """The user pressed a key(s) on the keyboard.
        
        :Parameters:
            ``keys`` : ``int``
                Key pressed by the user. In pyglet, this can be called
                ``symbol``.
            ``modifiers`` : ``int``
                Modifiers held down during the key press.
        """

        if self.disable or not self.focus:
            return

        self.dispatch_event("on_key", keys, modifiers)

        if self.focus:
            if self.children:
                self.dispatch_event("on_focus", KEYBOARD)

            # for widget in self.application.widgets:
            #     if not widget == self:
            #         widget.focus = False

    def on_key_release(self, keys, modifiers):
        """The user released a key(s) on the keyboard.

        ``keys`` - key released by the user. In pyglet, this can be called
                   ``symbol``.
        ``modifiers`` - modifiers held down during the key press

        parameters: int (32-bit), int (32-bit)
        """

        if self.disable or not self.focus:
            return

        self.press = False

        self.dispatch_event("on_lift", keys, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """The user moved the mouse.

        ``x`` - x position of mouse
        ``y`` - y position of mouse
        ``dx`` - x vector in last position from mouse
        ``dy`` - y vector in last position from mouse

        parameters: int, int, int, int
        """

        if self.disable:
            return

        if self.check_collision(Point(x, y)):
            self.hover = True

            self.dispatch_event("on_hover", x, y, dx, dy)
        else:
            self.hover = False

    def on_mouse_press(self, x, y, buttons, modifiers):
        """The user pressed a mouse button.

        ``x`` - x position of press
        ``y`` - y position of press
        ``buttons`` - buttons defined in keyboard pressed
        ``modifiers`` - modifiers held down during the press

        parameters: int, int, int (32-bit), int (32-bit)
        """

        if self.disable:
            return

        self.last_press = Point(x, y)

        if self.check_collision(Point(x, y)):
            self.press = True

            if self.children:
                self.focus = True

            self.dispatch_event("on_press", x, y, buttons, modifiers)
            self.dispatch_event("on_focus", MOUSE)

    def on_mouse_release(self, x, y, buttons, modifiers):
        """The user released a mouse button.

        :Parameters:
            ``x`` : ``int``
            x position of press.
            ``y`` : ``int``
            y position of press.
            ``buttons`` : ``int``
            buttons defined in keyboard released.
            ``modifiers`` : ``int``
            modifiers held down during the release.
        """

        if self.disable:
            return

        self.press = False

        self.drag = False

        self.dispatch_event("on_release", x, y, buttons, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """The user dragged the mouse.

        ``x`` - x position of mouse during drag
        ``y`` - y position of mouse during drag
        ``dx`` - movement of mouse in vector from last position
        ``dy`` - movement of mouse in vector from last position
        ``buttons`` - buttons defined in keyboard during drag
        ``modifiers`` - modifiers held down during the drag

        parameters: int, int, int, int, int (32-bit), int (32-bit)
        """

        if self.disable:
            return

        if not self.check_collision(Point(x, y)):
            if not self.check_collision(self.last_press):
                return

        self.drag = True

        if self.check_collision(Point(x, y)):
            self.dispatch_event("on_drag", x, y, dx, dy, buttons, modifiers)

    def on_mouse_scroll(self, x, y, sx, sy):
        """The user scrolled the mouse.

        ``x`` - x position of mouse during drag
        ``y`` - y position of mouse during drag
        ``scroll`` - scroll vector (positive being the mouse wheel up, negative the
                     mouse wheel down)

        parameters: int, int, Point
        """

        if self.disable:
            return

        if self.check_collision(Point(x, y)):
            if self.disable:
                return

            self.dispatch_event("on_scroll", x, y, Point(sx, sy))

    def on_text_motion_select(self, motion):
        """Some text in a pyglet.IncrementalTextLayout was selected. This is
        only used for entry widgets. See the entry widget on_text_select docs
        for more info.
        """

        self.dispatch_event("on_text_select", motion)

    def on_deactivate(self):
        """The window was deactivated. This means that the user switched the
        current window focus to an external application.
        """

        # for widget in self.widgets:
        #     widget.focus = widget.hover = False

    def on_update(self, delta):
        """Update the widget. Only do collision checking and property updating
        here. Drawing goes in the draw function.

        ``delta`` - time elapsed since last this function was last called
        """

        self.frames += 1

        # if self.widget:
        #     try:
        #         self.width = self.widget.width
        #         # self.height = self.widget.height

        #     except AttributeError:
        #         # For pyglet.text.Labels

        #         self.width = self.widget.content_width
        #         self.height = self.widget.content_height

        #     if self.disable:
        #         self.widget.alpha = DISABLE_ALPHA

        if self.application and not self.application.enable:
            self.disable = True

        if self.application:
            # Problem now fixed. Previously updated before added and
            # initialized, with some variables requiring application and widget
            # initialization.
            self.dispatch_event("update")

    def on_key(self, keys, modifiers):
        """The user pressed a key(s) on the keyboard. Note that this event is
        different from :py:meth:`~futura.widgets.Widget.on_text`, because
        :py:meth:`~futura.widgets.Widget.on_text` returns text typed as a
        string, though you can convert a key to a string by using some of the
        keyboard functions.

        When pressing :kbd:Tab\, the focus of the container switches to the
        next widget created. When a widget has focus, you can give it
        properties like if a button has focus, you can press :kbd:Space\ to
        invoke its command. If you press :kbd:Shift-Tab\, the focus is moved
        back by one notch. Focus of a widget can be gotten with the
        :py:attr:`~futura.widgets.Widget.focus` property, and the
        :py:meth:`~futura.widgets.Widget.on_focus` event.

        You can use a bit-wise "and" to detect multiple modifiers::

        >>> if modifiers & SHIFT and \
                modifiers & CONTROL and \
                keys == A:
                # Do something

        ``keys`` - key pressed by the user. In pyglet, this can be called
                   symbol.
        ``modifiers`` - modifiers held down during the key press

        parameters: int (32-bit), int (32-bit)
        """

    def on_lift(self, keys, modifiers):
        """The user released a key(s) on the keyboard.

        See :py:meth:`~futura.widgets.Widget.on_key` for details.

        ``keys`` - key released by the user. In pyglet, this can be called
                   symbol.
        ``modifiers`` - modifiers held down during the key press

        parameters: int (32-bit), int (32-bit)
        """

    def on_hover(self, x, y, dx, dy):
        """The widget was hovered over by the mouse. Typically, for widgets,
        something should react to this, for example their background shadow
        becomes more intense, or their color changes. For most widgets their
        image changes or their color does.

        You can see which specific widget if it had subwidgets had the hover
        event to get the coordinates. Hover states can be accessed with the
        :py:attr:`~futura.widgets.Widget.hover` property.

        For the modifiers, use a bitwise operation to detect multiple
        modifiers.

        :Parameters:
            ``x`` : ``int``
                ``x`` position of the mouse press.
            ``y`` : ``int``
                ``y`` position of the mouse press.
            ``buttons`` : ``int``
                Buttons that were pressed along with the mouse.
            ``modifiers`` : ``int``
                Modifiers being held down along with the mouse.

        :event:
        """

    def on_press(self, x, y, buttons, modifiers):
        """The user pressed the widget with the mouse. When this happens, the
        widget gets the focus traversal. This event can be used with
        :py:class:`~futura.widgets.Button`s,
        :py:class:`~futura.widgets.Label`s, and other widgets for cool special
        effects. This event is not called if the mouse is being dragged. This
        sets the :py:attr:`~futura.widgets.Widget.press` property to ``True``.

        For the modifiers, use a bitwise operation to detect multiple
        modifiers.

        :Parameters:
            ``x`` : ``int``
                ``x`` position of the mouse press.
            ``y`` : ``int``
                ``y`` position of the mouse press.
            ``buttons`` : ``int``
                Buttons that were pressed along with the mouse.
            ``modifiers`` : ``int``
                Modifiers being held down along with the mouse.

        :event:
        """

    def on_release(self, x, y, buttons, modifiers):
        """The user released the widget with the mouse. If the widget has an
        ``on_drag`` event, that event is canceled. For widgets, their state
        should be set to a hover state. This sets the drag and press properties
        to ``False``.

        For the modifiers, use a bitwise operation to detect multiple
        modifiers.

        :Parameters:
            ``x`` : ``int``
                ``x`` position of the mouse release.
            ``y`` : ``int``
                ``y`` position of the mouse release.
            ``buttons`` : ``int``
                Buttons that were pressed along with the mouse.
            ``modifiers`` : ``int``
                Modifiers being held down along with the mouse.

        :event
        """

    def on_drag(self, x, y, dx, dy, buttons, modifiers):
        """The user dragged the mouse, of which started over the widget. This
        is most used on text inputs and entries, where the user can select
        text, but can be on :py:class:`~futura.widgets.Slider`s and
        :py:class:`~futura.widgets.Toggle`s, and other widgets.

        There is no built-in way to get the starting position of the mouse,
        but that can be implemented. You could make a variable that gets the
        coordinates of each mouse press, then in the
        :py:meth:`~futura.widgets.Widget.on_drag` event, gets the last press
        coordinates.

        This sets the ``drag`` property to ``True``.

        This event is only dispatched if the mouse started on the widget. It is
        not canceled if the mouse moves outside of the widget, for as long as
        it starts in it, it works. You can get the starting point with the
        :py:attr:`~futura.widgets.Widget.last_press` property.

        ``x`` - x position of mouse during drag
        ``y`` - y position of mouse during drag
        ``dx`` - movement of mouse in vector from last position
        ``dy`` - movement of mouse in vector from last position
        ``buttons`` - buttons defined in keyboard during drag
        ``modifiers`` - modifiers held down during the drag

        parameters: int, int, int, int, int (32-bit), int (32-bit)
        """

    def on_scroll(self, x, y, scroll):
        """The user scrolled the mouse on the widget. This should be
        implemented in all widgets that change values, like spinboxes. Widgets
        that only have two values (like :py:class:`~futura.widgets.Toggle`s)
        should not use this event, as it is impractical.

        ``x`` - x position of mouse during drag
        ``y`` - y position of mouse during drag
        ``scroll`` - scroll vector (positive being the mouse wheel up, negative
                     the mouse wheel down)

        parameters: int, int, Point
        """

    def on_focus(self, approach):
        """The widget receives focus from the container. Two widgets cannot
        have focus simultaneously. A focused widget will immediately call all
        other widgets to lose focus. When a widget has focus, you should
        implement events that give it more features. For example, in a spinbox
        widget, if it has focus, the user can press the :kbd:Up\ or :kbd:Down\
        keys to increase or decrease the value. The
        :py:attr:`~futura.widgets.Widget.focus` property can be accessed.

        This may or may not be used for shapes. It vastly depends if how the
        widget gains focus. If it is pressed, then you may use this for certain
        shapes, but if it is focused with :kbd:Tab\, then you may use this for
        all shapes.

        ``approach`` - how the widget gains focus. This has two options:
                       :py:const:`~futura.KEYBOARD - the user pressed the
                                                    :kbd:Tab\ and/or
                                  :kbd:Shift-Tab\ key combinations to set focus
                       MOUSE - the user pressed the widget to get focus
                       PROGRAM - the focus property was set by the programmer
                                 (not yet implemented).

                       Usually this is the mouse option. Focus traversal via
                       keyboard is unknown to most people.

        See https://en.wikipedia.org/wiki/Focus_(computing)
        """


Widget.register_event_type("update")

Widget.register_event_type("on_key")
Widget.register_event_type("on_lift")
Widget.register_event_type("on_hover")
Widget.register_event_type("on_press")
Widget.register_event_type("on_release")
Widget.register_event_type("on_drag")
Widget.register_event_type("on_scroll")
Widget.register_event_type("on_focus")

Widget.register_event_type("on_text_select")


class Image(Widget):

    def __init__(self, filepath, x, y, anchor=(CENTER, CENTER)):
        """Create an Image widget. This is a simple widget used as the main
        component in many other widgets. It's also used to display any sort of
        image in a user interface tree, such as an icon or display.

        Setting an attribute of this widget will automatically set the
        corresponding attribute to its pyglet image, although **the image is
        not subclassed**. Please call a method defined by the image to use it.

        :Parameters:
            ``filepath``: file-like object or ``None``
                Filepath of the image. **Do not use a PIL image, a pyglet
                image, or an instance of arcade :py:class`~arcade.Texture`.**
            ``x`` : ``int``
                ``x`` position of the image
            ``y`` : ``int``
                ``y`` position of the image
            ``scale`` : ``int`` or ``float``
                Scaling factor of the image. Useful in shrinking/expanding. The
                width and height of the image are multiplied by the factor.
            ``bbox`` : ``str``
                Bounding box of the image. This must be either ``"simple"`` or
                ``"detailed"``. This parameter is not yet used.
        
        .. hint::
        
            As a last resort, you can use the
            :py:attr:`~futura.widgets.Image.sprite` property to get the actual
            pyglet sprite. But all properties are supported by futura.
            
            If a newer pyglet update adds a new property, please file a
            GitHub issue and describe the problem.
        """

        self.x = x
        self.y = y

        self.filepath = filepath
        self.anchor = anchor
        
    def _create(self):
        self.sprite = Sprite(load(self.filepath),
                             self.x, self.y,
                             batch=self.application.batch
                            )

        Widget.__init__(self, self.x, self.y)

        # HACK: We're using anchor instead of changing the anchor for the
        # pyglet sprite itself. Kind of nasty, but it improves consistency.
        # Anyways setting the sprite anchor does not work for now...
        
        # self.image.anchor_x = self.sprite.width
        # self.image.anchor_y = self.sprite.height
        
    def _update_position(self, x, y):
        """Update the position of the widget. This is called internally
        whenever position properties are modified.
        """

        self.sprite.x = x

        if self.anchor[0] == CENTER:
            self.sprite.x = x - self.width / 2
        elif self.anchor[0] == RIGHT:
            self.sprite.x = x + self.width
        
        self.sprite.y = y
        
        if self.anchor[1] == CENTER:
            self.sprite.y = y + self.height / 2
        elif self.anchor[1] == TOP:
            self.sprite.y = y + self.height

    @property
    def image(self):
        """Image displayed on the pyglet image. It's useful for different
        displays, costumes, or changing images.
        
        :type: :py:class:`~pyglet.image.AbstractImage`
        """
        
        return self.sprite.image
    
    @image.setter
    def image(self, image):
        self.sprite.image = image
    
    @property
    def width(self):
        """Width of the pyglet image. It directly uses the Sprite's
        :py:attr:`~pyglet.sprite.Sprite.width` property.
        
        This property is read-only.

        :type: ``int``
        """

        return self.sprite.width

    @property
    def height(self):
        """Height of the pyglet image. It directly uses the
        Sprite's :py:attr:`~pyglet.sprite.Sprite.height` property.
        
        This property is read-only.

        :type: ``int``
        """

        return self.sprite.height

    @property
    def scale(self):
        """Scale factor of the pyglet image. The Sprite's
        :py:attr:`~pyglet.sprite.Sprite.scale` property is used.
        
        :type: ``float``
        """
        
        return self.sprite.scale

    @scale.setter
    def scale(self, scale):
        self.sprite.scale = scale

    @property
    def alpha(self):
        """Blend opacity and transparency.
        
        This property sets the alpha component of the color of the sprite's
        vertices. With the default blend mode, this allows the sprite to be
        drawn with fractional opacity, blending with the background.
        
        :type: ``int``
        """
        
        return self.sprite.opacity

    @alpha.setter
    def alpha(self, alpha):
        self.sprite.opacity = alpha

    def draw(self):
        """Draw the image. The :py:class:`~futura.widgets.Image` class is one
        of the only widgets that use the
        :py:meth:`~futura.widgets.Widget.draw` method.

        The method :py:class:`~pyglet.image.AbstractImage.blit` is used to
        display a pyglet-type image.
        """
        
        # with self.application.ctx.pyglet_rendering():
        #     self.image.blit(self.x, self.y)


class Label(Widget):
    """Label widget to draw and display HTML text.

    FIXME: text changing styles after deleting and then replacing text
           (WORKAROUND)
    """

    UPDATE_RATE = 2

    def __init__(self, text, x, y,
                 colors=[BLACK, (COOL_BLACK, DARK_SLATE_GRAY, DARK_GRAY)],
                 font=DEFAULT_FONT, title=False,
                 justify=LEFT, width=None, multiline=False,
                 command=None, parameters=[],
                 outline=None, location=None
                ):

        """Create a Label widget to display efficient and advanced HTML text.
        Note that this uses pyglet's HTML decoder, so formats are limited. See
        the full list of formats at::

        https://pyglet.readthedocs.io/en/latest/programming_guide/text.html

        Text is antialiased to remove artifacts.

        :Parameters:
            ``text`` : ``str``
                HTML formatted text to be displayed on the label
            ``x`` : ``int``
                ``x`` position of the label
            ``y`` : ``int``
                ``y`` position of the label
            ``colors`` : ``list(tuple, (tuple, tuple, tuple)``
                Colors of the text. This is specified in a format
                ``[normal, (hover, press, disable)]``, which are its states and
                the appropriate colors displayed. Defaults to
                ``[(0, 0, 0), ((0, 46, 99), (47, 79, 79), (169, 169, 169))]``.
            ``font`` : `:py:class:`~futura.text.Font` or ``tuple``
                Font of the label. This can be an object-oriented font or just
                a tuple containing the font description in ``(family, size)``.
                Defaults to :py:const:`~futura.DEFAULT_FONT`.
            ``justify`` : ``str``
                Horizontal justification of the label. Its available options
                are ``"center"``, ``"left"``, or ``"right"``. Defaults to
                ``"right"``.
            ``width``` : ``int``
                Width of the label. This needs only to be used if the label is
                multiline. Defaults to ``None``, which is replaced by the
                window width. Setting it to a larger number can prevent this.
            ``multiline`` : ``bool``
                Text is drawn multiline. If this is set to true then the width
                must be set to a value greater than zero, as this will be the
                length of each line for wrap.
            ``command`` : ``callable``
                Command called and invoked when the label is pressed. Defaults
                to ``None``.
            ``parameters`` : ``list``
                Parameters of the command. **Do not use named parameters.**
                Defaults to an empty list.
            ``outline`` : ``tuple``
                Outline of the label as a rectangle. This is specified as
                ``(color, padding, width)``. Defaults to ``None``.

        Because this is object-oriented, nearly all of the values can be
        changed later by changing its properties.

        The update rate of the label defaults to once every sixty frames. This
        can be modified by setting the
        :py:attr:`~futura.widgets.Label.UPDATE_RATE`` property. The lower it is
        set, the higher the update rate is. If the update rate is too low (once
        every frame), then you will notice a massive performance drop. You can
        force the label to set text using
        :py:meth`~futura.widgets.Label.force_text`.

        See https://pyglet.readthedocs.io/en/latest/programming_guide/text.html
        for details regarding text specification and drawing.
        """

        # For new arcade installations, change the label property in
        # Text to a HTMLLabel for HTML scripting. (Don't need to do this
        # anymore)
        #
        # self._label = pyglet.text.HTMLLabel(
        #     text=text,
        #     x=start_x,
        #     y=start_y,
        #     width=width,
        #     multiline=multiline
        # )
        #
        # The Label widget is the only widget with a LEFT x anchor.
        #

        if not text:
            text = ""

        if not width:
            width = get_window().width

        if not justify in (LEFT, CENTER, RIGHT):
            raise WidgetsError(f"Invalid label justification \"{justify}\". "
                                "Must be \"left\", \"center\", or \"right\"."
                              )

        if multiline and not width:
            raise WidgetsError(f"When the parameter \"multiline\" is set to "
                                "True, the parameter \"width\" must be set to a "
                                "value greater than 0. See the documentation "
                                "for more details. This may be a side effect "
                                "of the window's width being set to zero."
                              )

        self.colors = colors
        self.font = font
        self.title = title
        self.justify = justify
        self.multiline = multiline
        self.command = command
        self.parameters = parameters
        self.outline = outline
        self.width = width
        self.multiline = multiline

        self.bindings = []

        self._attributes = \
            {
                "_x" : x,
                "_y" : y,
                "_text" : text,
                "_location" : location,
                "width" : width
            }

        self.length = 0

    def _create(self):
        self.label = HTMLLabel(self["_text"], self["_location"],
                               self["_x"], self["_y"],
                               anchor_x=LEFT, anchor_y=CENTER,
                               width=self["width"], multiline=self.multiline,
                               batch=self.application.batch,
                              )

        Widget.__init__(self, self.label)

        self.force_text(self.text)

    def _update_position(self, x, y):
        """Update the position of the widget. This is called internally
        whenever position properties are modified.
        """

        self.label.x = x
        self.label.y = y

    @property
    def text(self):
        """Text of the label. It is not recommended to call this repeatedly
        with a high update rate, as this can cause the fps to drop.

        FIXME: text changing styles after deleting and then replacing text
               (COMPLETED)

        See :py:class:`~pyglet.text.layout.TextLayout` documentation for
        details.

        :type: str
        """

        return self.document.text

    @text.setter
    def text(self, text):
        UPDATE_RATE = self.UPDATE_RATE

        if not self.UPDATE_RATE:
            UPDATE_RATE = 1 # ZeroDivisionError

        if self.frames % UPDATE_RATE:
            return

        text = str(text)

        if self.label.text == text:
            return

        if not text:
            text = ""

        self.label.begin_update()

        # self.document.delete_text(0, self.length)
        # self.document.insert_text(0, text)

        # Nasty, but it works as a workaround
        self.label.text = text

        self.label.end_update()

    @property
    def document(self):
        """Pyglet document of the label. Setting this is far less efficient
        than modifying the current document, as relayout and recalculating
        glyphs is very costly.

        :type: :py:meth:`~pyglet.text.document.FormattedDocument`
        """

        return self.label.document

    @document.setter
    def document(self, document):
        self.label.document = document

    @property
    def content_width(self):
        """Content width of the label.

        This property is read-only.

        :type: ``int``
        """

        return self.label.content_width

    @property
    def content_height(self):
        """Content height of the label.

        This property is read-only.

        :type: ``int``
        """

        return self.label.content_height

    def bind(self, *keys):
        """Bind some keys to the label. Invoking these keys activates the
        label. If the :kbd:`Enter`\ key was binded to the label, pressing
        :kbd:`Enter`\ will invoke its command and switch its display to a
        pressed state.

        Currently, binding modifiers with keys is not supported, though it is
        quite easy to implement by yourself.

            >>> label.bind(ENTER, PLUS)
            [65293, 43]

        :Parameters:
            ``keys`` : ``[[int, int]]``
                Keys to be binded to the label's associated command.

        :rtype: ``list``
        :returns: Current key bindings after the modification
        """

        self.bindings = [*keys]
        return self.bindings

    def unbind(self, *keys):
        """Unbind keys from the label. This reverts the
        :py:meth:`~futura.widgets.Label.bind` command partially.

            >>> label.bind(ENTER, PLUS, KEY_UP, KEY_DOWN)
            [65293, 43, 65362, 65364]
            >>> label.unbind(PLUS, KEY_UP)
            [65293, 65364]

        :Parameters:
            ``keys`` : ``List[[int, int]]``
                Keys to be unbinded to the button's associated command.

        :rtype: ``list``
        :returns: Current key bindings after the modification
        """

        for key in keys:
            self.bindings.remove(key)
        return self.bindings

    def invoke(self):
        """Invoke the label. This switches its text to a pressed state and
        calls its associated command with the specified parameters. If the
        label is disabled this has no effect.
        """

        if self.disable or not self.command:
            return

        self.press = True

        if self.parameters:
            self.command(self.parameters)
        else:
            self.command()

    def force_text(self, text):
        """Force the label to set the text. This should only be used with
        caution, because if used excessively, will cause a performance drop.
        The update rate is completely ignored.

        :Parameters:
            ``text`` : str
                HTML formatted text of the label. If this is excessively long,
                a performance drop will be visible.

        :see: :py:`~pyglet.text.layout.TextLayout`
        """

        if self.text == text:
            return

        if not text:
            text = ""

        text = str(text)

        self.label.text = text

    def draw_bbox(self, width=1, padding=0):
        """Draw the hitbox of the label. See Widget.bbox for more details.
        This overrides the Widget.bbox because of its left anchor_x.
        """

        draw_rectangle_outline(
            self.x + self.width / 2,
            self.y, self.width + padding,
            self.height + padding, RED, width
        )

    draw_hitbox = draw_bbox
    draw_hit_box = draw_bbox

    def draw(self):
        if self.outline:
            draw_rectangle_outline(
                self.x + self.width / 2, self.y,
                self.width + self.outline[1],
                self.height + self.outline[1],
                self.outline[0], self.outline[2]
            )

        if self.text:
            if not self._left == self.x - self.width / 2 or \
                not self._right == self.x + self.width / 2 or \
                not self._top == self.y + self.height / 2 or \
                not self._bottom == self.y - self.height / 2:
                self._left = self.x - self.width / 2
                self._right = self.x + self.width / 2
                self._top = self.y + self.height / 2
                self._bottom = self.y - self.height / 2

    def on_key(self, keys, modifiers):
        if isinstance(self.bindings, list):
            if keys in self.bindings:
                self.invoke()

        else:
            if self.bindings == keys:
                self.invoke()

    def on_press(self, x, y, buttons, modifiers):
        if self.disable or not self.command:
            return

        if buttons == MOUSE_BUTTON_LEFT:
            self.invoke()

    def update(self):
        """Update the label. This upgrades its properties and registers its
        states and events.

        The following section has been tested dozens of times. The performance
        was incredibly slow, with about 1 fps for 100 Labels. Usually, for a
        single Label the processing time is about one-hundredth of a second.

        With the :py:meth:`~pyglet.text.layout.TextLayout.begin_update` and
        :py:meth:`~pyglet.text.layout.TextLayout.end_update` methods for the
        label, the processing time is much faster. And with batches, things are
        more efficient and speed is even greater.

        Futura can display around 2,500 labels before the fps drops below sixty
        frames per second. Typically you should not need a high fps for a
        solely-UI focused application, but for a game that might be a problem.
        Optimizations for labels are in progress.

        Additionally, with a large number of labels (2,000+), the startup time
        may be very slow (a few seconds or more).

        .. note::

            Multiline labels do not switch color, as it doesn't make sense for
            a paragraph to change color on state change.
        """

        self.length = len(self.text)

        # if "<u" in self.text or "<\\u>" in self.text:
        #     # ValueError: Can only assign sequence of same size
        #     return
        #
        # This was solved in the latest pyglet release

        if not self.multiline:
            # States
            if self.hover:
                self.document.set_style(0, self.length,
                                        {"color" : (four_byte(self.colors[1][1]))})
            if self.press:
                self.document.set_style(0, self.length,
                                        {"color" : four_byte(self.colors[1][1])})
            if self.disable:
                self.document.set_style(0, self.length,
                                        {"color" : four_byte(self.colors[1][2])})

            if self.focus:
                self.document.set_style(0, self.length,
                                        {"color" : four_byte(self.colors[1][0])})

            if not self.hover and \
                not self.press and \
                not self.disable and \
                not self.focus:
                # Wipe the document. Seems nasty, but the getter and setter for
                # properties works with this instance.

                self.text = self.text


class Button(Widget):
    """Button widget to invoke and call commands. Pressing on a button invokes
    its command, which is a function, method, or callable.
    """

    def __init__(
                 self, text, x, y, command=None, parameters=[],
                 link=None, colors=["yellow", DEFAULT_LABEL_COLORS],
                 font=default_font, callback=SINGLE
                ):

        """Create a button widget. A button has two components: an
        :py:class:`~futura.widgets.Image` and a
        :py:class:`~futura.widgets.Label`. You can customize the button's
        images and display by changing its
        :py:attr:`~futura.widgets.Button.normal_image`,
        :py:attr:`~futura.widgets.Button.hover_image`,
        :py:attr:`~futura.widgets.Button.press_image`, and
        :py:attr:`~futura.widgets.Button.disable_image` properties, but it is
        recommended to use theming instead.

        The :py:meth:`~futura.widgets.Button.on_push` event is triggered when
        the button is invoked.

        :Parameters:
            ``text`` : ``str``
                HTML text to be displayed on the button.
            ``x`` : ``int``
                ``x`` position of the button.
            ``y`` : ``int``
                ``y`` position of the button.
            ``command`` : ``callable``
                Command called and invoked when the label is pressed. Defaults
                to ``None``.
            ``parameters`` : ``list``
                Parameters of the command. **Do not use named parameters.**
                Defaults to an empty list.
            ``link`` : ``str``
                Website link to go to when invoked. The ``webbrowser`` module
                is used. Defaults to ``None``.
            ``colors`` : ``list(str, [tuple, (tuple, tuple, tuple)])`
                Colors of the text of the button. Defaults to
                ``("yellow", ...)``.
            ``font`` : `:py:class:`~futura.text.Font` or ``tuple``
                Font of the label. This can be an object-oriented font or just
                a tuple containing the font description in ``(family, size)``.
                Defaults to :py:const:`~futura.DEFAULT_FONT`.
            ``callback`` : ``int``
                How the button is invoked::

                :py:const:`~futura.SINGLE` - the button is invoked once when
                pressed

                :py:const:`~futura.DOUBLE` - the button can be invoked
                multiple times if it has focus

                :py:const:`~futura.MULTIPLE` - the button can be invoked
                continuously

                Defaults to :py:const:`~futura.SINGLE`.
        """

        # A two-component widget:
        #     - Image
        #     - Label

        if not callback in (SINGLE, DOUBLE, MULTIPLE):
            raise WidgetsError("Invalid callback for button. Must be 1, 2, or "
                               "3. Refer to the class documentation for more "
                               "information."
                              )

        self.command = command
        self.parameters = parameters
        self.link = link

        self.callback = callback

        self.keys = []
        self.bindings = []

        self._attributes = \
            {
                "_text" : text,
                "_x" : x,
                "_y" : y,
                "_font" : font,
                "_colors" : colors
            }

        # Find a way to better fit to 80 chars

        self.normal_image = widgets[f"{colors[0]}_button_normal"]
        self.hover_image = widgets[f"{colors[0]}_button_hover"]
        self.press_image = widgets[f"{colors[0]}_button_press"]
        self.disable_image = widgets[f"{colors[0]}_button_disable"]

    def _create(self):
        self.image = Image(widgets[f"yellow_button_normal"],
                           self["_x"],
                           self["_y"]
                          )
        self.label = Label(self["_text"],
                           self["_x"],
                           self["_y"],
                           font=self["_font"]
                          )

        Widget.__init__(self, self["_x"], self["_y"])

        self.children = [self.image, self.label]

        self.image._create()
        self.label._create()

        # self.label.label.anchor_x = CENTER

        self.application.push_handlers(self.on_key_press)

    def _update_position(self, x, y):
        """Update the position of the widget. This is called internally
        whenever position properties are modified.
        """

        self.label.x = x
        self.image.x = x

        self.label.y = y
        self.image.y = y
        
    @property
    def text(self):
        """Text of the button. This is the direct text that is displayed on the
        label, not a modified version of it.

        :see: :py:attr:`~futura.widgets.Label.text`

        :type: ``str``
        """

        return self.label.text

    @text.setter
    def text(self, text):
        self.label.text = text

    def _get_font(self):
        """Font of the text displayed on the button.

        :see: :py:attr:`~futura.widgets.Label.font`

        :type: ``tuple`` or :py:class:`~futura.text.Font`
        """

        return self.label.font

    def _set_font(self, font):
        self.label.font = font

    def _get_colors(self):
        """Colors of the text of the button. Remember that this is a
        multi-dimensional list. This is also the color of the button.

        :see: :py:attr:`~futura.widgets.Label.color`

        :type: ``list``
        """

        return [self._color, self.label.colors]

    def _set_colors(self, colors):
        self._color = colors

        self.label.colors = colors[1]

    text = property(_get_text, _set_text)
    font = property(_get_font, _set_font)
    colors = property(_get_colors, _set_colors)

    def bind(self, *keys):
        """Bind some keys to the button. Invoking these keys activates the
        button. If the :kbd:`Enter`\ key was binded to the button, pressing
        :kbd:`Enter`\ will invoke its command and switch its display to a
        pressed state.

        Currently, binding modifiers with keys is not supported, though this is
        quite easy to implement by yourself.

            >>> button.bind(ENTER, PLUS)
            [65293, 43]

        :Parameters:
            ``keys`` : ``[[int, int]]``
                Keys to be binded to the button's associated command.

        :rtype: ``list``
        :returns: Current key bindings after the modification
        """

        self.bindings = [*keys]
        return self.bindings

    def unbind(self, *keys):
        """Unbind keys from the label. This reverts the
        :py:meth:`~futura.widgets.Button.bind` command partially.

            >>> button.bind(ENTER, PLUS, KEY_UP, KEY_DOWN)
            [65293, 43, 65362, 65364]
            >>> button.unbind(PLUS, KEY_UP)
            [65293, 65364]

        :Parameters:
            ``keys`` : ``List[[int, int]]``
                Keys to be unbinded to the button's associated command.

        :rtype: ``list``
        :returns: Current key bindings after the modification
        """

        for key in keys:
            self.bindings.remove(key)
        return self.bindings

    def invoke(self):
        """Invoke the button. This switches its image to a pressed state and
        calls its associated command with the specified parameters. If the
        button is disabled this has no effect.

        Dispatches the :py:class:`~futura.widgets.Button.on_push` event.
        """

        if self.disable or not self.command:
            return

        self.press = True

        self.dispatch_event("on_push")

        if self.parameters:
            self.command(self.parameters)
        else:
            self.command()

        if self.link:
            open_new(self.link)

    def on_press(self, x, y, buttons, modifiers):
        if buttons == MOUSE_BUTTON_LEFT:
            self.invoke()

    def on_key(self, keys, modifiers):
        if keys == SPACE:
            self.invoke()

    def on_key_press(self, keys, modifiers):
        if isinstance(self.bindings, list):
            if keys in self.bindings:
                self.invoke()

        else:
            if self.bindings == keys:
                self.invoke()

    def update(self):
        # if self.hover:
        #     self.image.image = self.hover_image
        # if self.press:
        #     self.image.image = self.press_image
        # if self.disable:
        #     self.image.image = self.disable_image

        # if not self.hover and \
        #     not self.press and \
        #     not self.disable:
        #     self.image.image = self.normal_image

        double = False

        for key in self.keys:
            for binding in self.bindings:
                if key == binding:
                    double = True
                    break
                # else:
                #     continue
            break

        multiple = double # Haha

        if self.callback == DOUBLE and self.focus and double:
            self.invoke()

        if self.callback == MULTIPLE:
            if self.press or multiple:
                self.invoke()

        # .update is not called for the Label, as it is unnecessary for the
        # Label to switch colors on user events.

Button.register_event_type("on_push")


class Slider(Widget):
    """Slider widget to display slidable values. A slider has a knob that can
    be scrolled by the user on keyboard, mouse, and scroll events. This knob
    determines the slider's value.

    FIXME: even knob moves when setting x property
    TODO: add keyboard functionality

    https://github.com/eschan145/futura/issues/20
    """

    _value = 0

    def __init__(self, x, y, colors=DEFAULT_LABEL_COLORS, font=DEFAULT_FONT,
                 default=0, size=100, length=200, padding=50, round=None,
                 group=None
                ):

        """Create a slider widget.

        :Parameters:
            ``x`` : ``int``
                ``x`` position of the slider.
            ``y`` : ``int``
                ``y`` position of the slider.
            ``colors`` : ``list(tuple, (tuple, tuple, tuple)``
                Colors of the text. This is specified in a format
                ``[normal, (hover, press, disable)]``, which are its states and
                the appropriate colors displayed. Defaults to
                ``[(0, 0, 0), ((0, 46, 99), (47, 79, 79), (169, 169, 169))]``.
            ``font`` : `:py:class:`~futura.text.Font` or ``tuple``
                Font of the label. This can be an object-oriented font or just
                a tuple containing the font description in ``(family, size)``.
                Defaults to :py:const:`~futura.DEFAULT_FONT`.
            ``default`` : ``int`` or ``float``
                Default value of the slider, where the knob starts at. Defaults
                to ``0``.
            ``size`` : ``int``
                The number of values that can be on the slider. The knob will
                automatically snap to these values and their designated x
                positions.
            ``length`` : ``int``
                Direct width/length in pixels of the slider.
            ``padding`` : ``int``
                Spacing between the label and the slider.
            ``round`` : ``int``
                Number of digits to round the slider's value to.
        """

        self.bar = Image(slider_horizontal, x, y)
        self.knob = Image(knob, x, y)
        self.label = Label(default, x, y, font=font)

        Widget.__init__(self, self.bar)

        self.children = [self.bar, self.knob, self.label]

        self.colors = colors
        self.font = font
        self.size = size
        self.length = length
        self.padding = padding
        self.round = round

        self.value = default

        # Must be after the above attributes
        self.x = x
        self.y = y

        self.value = 0
        self.destination = 0

    def _update_position(self, x, y):
        """Update the position of the widget. This is called internally
        whenever position properties are modified.
        """

        self.bar.x = x
        self.knob.left = x - self.length / 2
        self.label.x = self.bar.left - self.padding

        self.bar.y = y
        self.knob.y = y
        self.label.y = y

    def _get_value(self):
        """Value or ``x`` of the slider. Setting this updates and snaps it to
        the position relative to the given value.

        :type: ``float``
        """

        return self._value

    def _set_value(self, value):
        if self._value >= self.size:
            self._value = self.size
            return

        elif self._value <= 0:
            self._value = 0
            return

        max_knob_x = self.right # + self.knob.width / 2

        self._value = round(value, self.round)

        x = (max_knob_x - self.left) * value / self.size \
            + self.left + self.knob.width / 2
        self.knob.x = max(self.left, min(x - self.knob.width / 2, max_knob_x))

    def _get_text(self):
        """Text of the label. It is not recommended to call this repeatedly
        with a high update rate, as this can cause the fps to drop.

        See :py:class:`~pyglet.text.layout.TextLayout` documentation for
        details.

        :type: ``str``
        """

        return self.label.text

    def _set_text(self, text):
        self.label.text = text

    def _get_font(self):
        """Font of the text displayed on the slider.

        :see: :py:attr:`~futura.widgets.Label.font`

        :type: ``tuple`` or ``Font``
        """

        return self.label.font

    def _set_font(self, font):
        self.label.font = font

    def _get_colors(self):
        """Colors of the text of the slider. Remember that this is a
        multi-dimensional list.

        :see: :py:attr:`~futura.widgets.Label.colors`

        :type: ``list``
        """

        return self.label.colors

    def _set_colors(self, colors):
        self.label.colors = colors

    value = property(_get_value, _set_value)
    text = property(_get_text, _set_text)
    font = property(_get_font, _set_font)
    colors = property(_get_colors, _set_colors)

    def update_knob(self, x):
        """Update the knob and give it a velocity when moving. When calling
        this, the knob's position will automatically update so it is congruent
        with its size.

        Dispatches the :py:meth:`~futura.widgets.Slider.on_slide_start` event.

        .. hint::

            This method does not move the knob. It just sets a velocity.

        :Parameters:
            ``x`` : ``int``
                ``x`` value of the knob to set destination
        """

        self.destination = max(self.left, min(x, self.right))
        self._value = round(abs(((self.knob.x - self.left) * self.size)
                                / (self.left - self.right)), self.round)

        self.text = round(self.value, self.round)

        self.dispatch_event("on_slide_start", self._value)

    def reposition_knob(self):
        """Update the value of the slider. This is used when you want to move
        the knob without it snapping to a certain position and want to update
        its value. :py:meth:`~futura.widgets.Slider.update_knob` sets a
        velocity so the knob can glide.

        Dispatches the :py:meth:`~futura.widgets.on_slide_motion` event.
        """

        try:
            self._value = round(abs(((self.knob.x - self.left) * self.size) \
                          / (self.left - (self.right - self.knob.width))),
                          self.round)

            self.dispatch_event("on_slide_motion")

        except ZeroDivisionError: # Knob hasn't even moved
            return

        self.text = round(self.value, self.round)

    def draw(self):
        # Force setting width

        self.bar._width = self.length

    def on_key(self, keys, modifiers):
        if not self.focus:
            return

        if keys == KEY_RIGHT:
            self.value -= 1
            # self.reposition_knob()
        elif keys == KEY_LEFT:
            self.value += 1
            # self.reposition_knob()

    def on_press(self, x, y, buttons, modifiers):
        self.update_knob(x)

    def on_drag(self, x, y, dx, dy, buttons, modifiers):
        self.update_knob(x)

    def on_scroll(self, x, y, mouse):
        self.value += mouse.y

    def update(self):
        if self.destination:
            if self.knob.x <= self.destination and \
               self.knob.right <= self.right:
                # Knob too left, moving to the right
                self.knob.x += SLIDER_VELOCITY
                self.reposition_knob()

            else:
                self.dispatch_event("on_slide_finish", RIGHT)

            if self.knob.right > self.destination and \
               self.knob.left >= self.left:
                # Knob too right, moving to the left
                self.knob.x -= SLIDER_VELOCITY
                self.reposition_knob()

            else:
                self.dispatch_event("on_slide_finish", LEFT)

        # Knob hover effect
        if self.knob.hover:
            self.knob.scale = KNOB_HOVER_SCALE
        else:
            self.knob.scale = 0.9

    def on_slide_start(self, value):
        """The knob of the slider has started motion. This means that the
        velocity is set, and the knob just needs to finish its journey.

        :Parameters:
            ``value `` : ``int`` or ``float``
                Value the knob has ended at.

        :type: event
        """

    def on_slider_motion(self):
        """The knob of the slider is in motion. It is in its journey to reach
        the other slide of the bar.

        :type: event
        """

    def on_slide_finish(self, value):
        """The knob of the slider has finished its journey, therefore changing
        the value.

        :Parameters:
            ``value`` : ``int`` or ``float``
                New value that the knob has moved to.
        """

Slider.register_event_type("on_slide_start")
Slider.register_event_type("on_slide_motion")
Slider.register_event_type("on_slide_finish")


class Toggle(Widget):
    """Toggle widget to switch between true and false values. This uses
    a special effect of fading during the switch.

    FIXME: even knob moves when setting ``x`` property
    """

    true_image = load_texture(toggle_true)
    false_image = load_texture(toggle_false)
    hover_true_image = load_texture(toggle_true_hover)
    hover_false_image = load_texture(toggle_false_hover)

    on_left = True
    on_right = False
    value = None
    switch = False

    def __init__(
                 self, text, x, y,
                 colors=DEFAULT_LABEL_COLORS, font=DEFAULT_FONT,
                 default=True, padding=160,
                 callback=SINGLE
                ):

        """Create a toggle widget. A toggle is a widget that when pressed,
        switches between ``True`` and ``False`` values.

        TODO: fix knob image (scaling)

        :Parameters:
            ``text`` : ``str``
                HTML text to be displayed alongside the toggle.
            ``x`` : ``int``
                ``x`` position of the toggle.
            ``y`` : ``int``
                ``y`` position of the toggle.
            ``colors`` : ``list(str, [tuple, (tuple, tuple, tuple)])`
                Colors of the text of the toggle. Defaults to
                ``("yellow", ...)``.
            ``font`` : `:py:class:`~futura.text.Font` or ``tuple``
                Font of the label. This can be an object-oriented font or just
                a tuple containing the font description in ``(family, size)``.
                Defaults to :py:const:`~futura.DEFAULT_FONT`.
            ``default`` : ``int``
                Default value of the toggle.
            ``padding`` : ``int``
                Spacing between the label and the toggle.
            ``callback`` : ``int``
                how the toggle is invoked:

                :py:const:`~futura.SINGLE` - toggle is invoked once when
                pressed

                :py:const:`~futura.MULTIPLE` - toggle can be invoked
                continuously

                Defaults to :py:const:`~futura.SINGLE`.
        """

        # A three-component widget:
        #     - Image
        #     - Image
        #     - Label

        if default:
            image = toggle_true
        else:
            image = toggle_false

        if not callback in (SINGLE, DOUBLE, MULTIPLE):
            raise WidgetsError("Invalid callback for toggle. Must be 1, 2, or "
                               "3. Refer to the class documentation for more "
                               "information."
                              )

        self.bar = Image(image, x, y)
        self.knob = Image(knob, x, y)

        self.label = Label(knob, x, y, font=font)

        Widget.__init__(self, self.bar)

        self.children = [self.bar, self.knob, self.label]

        self.text = text
        self.colors = colors
        self.font = font
        self.padding = padding
        self.callback = callback

        self.x = x
        self.y = y

        self.knob.left = self.bar.left

    def _update_position(self, x, y):
        """Update the position of the widget. This is called internally
        whenever position properties are modified.
        """

        self.bar.x = x
        self.bar.y = self.knob.y = self.label.y = y

        self.label.x = self.bar.left - self.padding

    def _get_text(self):
        """Text of the toggle. This is the direct text that is displayed on the
        label, not a modified version of it.

        :see: :py:attr:`~futura.widgets.Label.text`

        :type: ``str``
        """

        return self.label.text

    def _set_text(self, text):
        self.label.text = text

    def _get_font(self):
        """Font of the text displayed on the toggle.

        :see: :py:attr:`~futura.widgets.Label.font`

        :type: ``tuple`` or :py:class:`~futura.text.Font``
        """

        return self.label.font

    def _set_font(self, font):
        self.label.font = font

    def _get_colors(self):
        """Colors of the text of the toggle. Remember that this is a
        multi-dimensional list.

        :see: :py:attr:`~futura.widgets.Label.color`

        :type: ``list``
        """

        return self.label.colors

    def _set_colors(self, colors):
        self.label.colors = colors

    text = property(_get_text, _set_text)
    font = property(_get_font, _set_font)
    colors = property(_get_colors, _set_colors)

    def on_press(self, x, y, buttons, modifiers):
        if not modifiers & CONTROL:
            self.switch = True

    def on_key(self, keys, modifiers):
        if keys == SPACE or keys == ENTER:
            self.switch = True

    def update(self):
        if self.on_left:
            self.value = True
        else:
            self.value = False

        if self.callback == MULTIPLE:
            if self.keys[SPACE]:
                self.switch = True

        if self.switch and not self.disable:
            if self.on_left:
                # Knob on the left, moving towards the right
                if self.knob.right < self.bar.right - 3:
                    self.knob.x += TOGGLE_VELOCITY
                else:
                    self.on_right = True
                    self.on_left = False

                    self.switch = False

                    self.dispatch_event("on_toggle", False)

                if self.knob.x < self.x:
                    try: self.bar.alpha -= TOGGLE_FADE
                    except ValueError: pass
                elif self.knob.x > self.x: # More than halfway
                    try: self.bar.alpha += TOGGLE_FADE
                    except ValueError: pass

                    self.bar.image = self.false_image
                    if self.hover: self.bar.image = self.hover_false_image

            elif self.on_right:
                # Knob on the right, moving towards the left
                if self.knob.left > self.bar.left + 2:
                    self.knob.x -= TOGGLE_VELOCITY
                else:
                    self.on_left = True
                    self.on_right = False

                    self.switch = False

                    self.dispatch_event("on_toggle", True)

                if self.knob.x > self.x:
                    try: self.bar.alpha -= TOGGLE_FADE
                    except ValueError: pass
                elif self.knob.x < self.x:
                    try: self.bar.alpha += TOGGLE_FADE
                    except ValueError: pass

                    self.bar.image = self.hover_true_image
                    if self.hover: self.bar.image = self.hover_true_image

        else:
            if self.hover:
                if self.value: self.bar.image = self.hover_true_image
                else: self.bar.image = self.hover_false_image
            else:
                if self.value: self.bar.image = self.true_image
                else: self.bar.image = self.false_image

        if self.disable:
            if self.value: self.bar.image = self.true_image
            else: self.bar.image = self.false_image

        if self.knob.hover:
            self.knob.scale = KNOB_HOVER_SCALE
        else:
            self.knob.scale = 0.9

    def on_toggle(self, value):
        """The toggle has been completed. This means that the knob has moved
        from one side of the bar to the other.

        value - boolean of the toggle's value

        parameters: bool
        """

Toggle.register_event_type("on_toggle")


class Caret(_Caret):
    """Caret used for pyglet.text.IncrementalTextLayout."""

    PERIOD = 0.5

    def __init__(self, layout):
        """Initialize a caret designed for interactive editing and scrolling of
        large documents and/or text.
        """

        _Caret.__init__(self, layout)

    def on_text_motion(self, motion, select=False):
        """The caret was moved or a selection was made with the keyboard.

        motion - motion the user invoked. These are found in the keyboard.
                 MOTION_LEFT                MOTION_RIGHT
                 MOTION_UP                  MOTION_DOWN
                 MOTION_NEXT_WORD           MOTION_PREVIOUS_WORD
                 MOTION_BEGINNING_OF_LINE   MOTION_END_OF_LINE
                 MOTION_NEXT_PAGE           MOTION_PREVIOUS_PAGE
                 MOTION_BEGINNING_OF_FILE   MOTION_END_OF_FILE
                 MOTION_BACKSPACE           MOTION_DELETE
                 MOTION_COPY                MOTION_PASTE
        select - a selection was made simultaneously

        parameters: int (32-bit), bool
        returns: event
        """

        if motion == MOTION_BACKSPACE:
            if self.mark is not None:
                self._delete_selection()
            elif self._position > 0:
                self._position -= 1
                self._layout.document.delete_text(self._position, self._position + 1)
                self._update()
        elif motion == MOTION_DELETE:
            if self.mark is not None:
                self._delete_selection()
            elif self._position < len(self._layout.document.text):
                self._layout.document.delete_text(self._position, self._position + 1)
        elif self._mark is not None and not select and \
            motion is not MOTION_COPY:
            self._mark = None
            self._layout.set_selection(0, 0)

        if motion == MOTION_LEFT:
            self.position = max(0, self.position - 1)
        elif motion == MOTION_RIGHT:
            self.position = min(len(self._layout.document.text), self.position + 1)
        elif motion == MOTION_UP:
            self.line = max(0, self.line - 1)
        elif motion == MOTION_DOWN:
            line = self.line
            if line < self._layout.get_line_count() - 1:
                self.line = line + 1
        elif motion == MOTION_BEGINNING_OF_LINE:
            self.position = self._layout.get_position_from_line(self.line)
        elif motion == MOTION_END_OF_LINE:
            line = self.line
            if line < self._layout.get_line_count() - 1:
                self._position = self._layout.get_position_from_line(line + 1) - 1
                self._update(line)
            else:
                self.position = len(self._layout.document.text)
        elif motion == MOTION_BEGINNING_OF_FILE:
            self.position = 0
        elif motion == MOTION_END_OF_FILE:
            self.position = len(self._layout.document.text)
        elif motion == MOTION_NEXT_WORD:
            pos = self._position + 1
            m = self._next_word_re.search(self._layout.document.text, pos)
            if not m:
                self.position = len(self._layout.document.text)
            else:
                self.position = m.start()
        elif motion == MOTION_PREVIOUS_WORD:
            pos = self._position
            m = self._previous_word_re.search(self._layout.document.text, 0, pos)
            if not m:
                self.position = 0
            else:
                self.position = m.start()

        self._next_attributes.clear()
        self._nudge()

    def _update(self, line=None, update_ideal_x=True):
        """Update the caret. This is used internally for the entry widget.

        line - current line of the caret
        update_ideal_x - x position of line is updated

        parameters: int, bool
        """

        if line is None:
            line = self._layout.get_line_from_position(self._position)
            self._ideal_line = None
        else:
            self._ideal_line = line
        x, y = self._layout.get_point_from_position(self._position, line)
        if update_ideal_x:
            self._ideal_x = x

        # x -= self._layout.view_x
        # y -= self._layout.view_y
        # add 1px offset to make caret visible on line start
        x += self._layout.x + 1

        y += self._layout.y + self._layout.height / 2 + 2

        font = self._layout.document.get_font(max(0, self._position - 1))
        self._list.position[:] = [x, y + font.descent, x, y + font.ascent]

        if self._mark is not None:
            self._layout.set_selection(min(self._position, self._mark), max(self._position, self._mark))

        self._layout.ensure_line_visible(line)
        self._layout.ensure_x_visible(x)


class Entry(Widget):
    """Entry widget to display user-editable text. This makes use of the
    :py:class:`~pyglet.text.layout.IncrementalTextLayout` and a modified
    version of its built-in caret.

    Rich text formatting is currently in progress.

    FIXME: caret not showing on line start (pyglet error)
           use of a lot of GPU when selected text is formatted (may be pyglet)
           make caret transparent or invisible instead of changing color (COMPLETED)
           caret glitching out on blinks at line end (pyglet error)
           entry taking up much CPU

    TODO

    1. Add rich text formatting (use pyglet.text.document.HTMLDocument)
    2. Add show feature for passwords
    3. Add copy, paste, select all, and more text features (COMPLETED)
    4. Add undo and redo features
    5. Enable updates for the layout for smoother performance. This raises
       AssertionError, one that has been seen before.
    6. Finish up scrolling of history. This is incomplete, and if text is
       added before the history's index, then the index is not changed.

    https://github.com/eschan145/futura/issues/1#issue-1393607169
    """

    # Simple validations
    VALIDATION_LOWERCASE = compile("^[a-z0-9_\-]+$")
    VALIDATION_UPPERCASE = compile("^[A-Z]*$")
    VALIDATION_LETTERS = compile("[A-Z]")
    VALIDATION_DIGITS = compile("[1-9]")

    # From https://www.computerhope.com/jargon/r/regex.htm
    VALIDATION_EMAIL = compile("/[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,4}")


    # Most advanced validation, with non-signed zero believers
    VALIDATION_ADVANCED_DIGITS = compile("^((?!-0?(\.0+)?(e|$))-?(0|[1-9]\d*)?"
                                         "(\.\d+)?(?<=\d)(e-?(0|[1-9]\d*))?|0x"
                                         "[0-9a-f]+)$"
                                        )
    VALIDATION_REGULAR = None
    
    #: Here below are several constants used by the entry widget. To set a
    #: constant, modify it by class attribute::
    #: 
    #:     Entry.[CONSTANT] = VALUE
    #: 
    #: This will change the constant. You do not have to do this multiple
    #: times, and it will *only* affect new entries, not existing ones.

    #: Blink period of the caret, in milliseconds. Once set this can not be
    #: changed, except by modifying the pyglet caret's
    #: :py:attr:`~pyglet.text.caret.Caret.PERIOD` property directly.
    #:
    #: A default blinking period for a regular caret (this may vary from system
    #: to system), is twice every second. The blink period for the caret in
    #: futura is 500 ms.
    PERIOD = 500
    
    #: Whether caret blinking should be enabled on default. A disabled caret
    #: leaves the effect of a bug in the display. The user may also find this
    #: ambiguous.
    ENABLE_BLINK = True
    
    _history_index = 0

    _validate = VALIDATION_LETTERS
    _document = None
    _placeholder = None

    _history_index = 0
    _history_enabled = None
    _blinking = True

    normal_image = load_texture(entry_normal)
    hover_image = load_texture(entry_hover)
    focus_image = load_texture(entry_focus)

    def __init__(self, application, x, y, width=200, height=80, text="",
                 font=default_font, color=BLACK,
                 history=True):

        """Create an entry widget. Typically a widget will push events
        automatically, but because there are custom-named events, they have
        to be defined here.

        An entry is a widget where text input can be returned. Typing into
        an entry appends some text, which can be used for usernames,
        passwords, and more. Text can be removed by many keys.

        The :py:meth:`~futura.widgets.Entry.on_text_edit` event is triggered
        when text in the entry is modified. The
        :py:meth:`~futura.widgets.Entry.on_text_interact` event is triggered
        when text is interacted with, like selecting, moving the caret, or
        other events that are associated with the caret and not text
        modification.

        :Parameters:
            ``x`` : ``int``
                ``x`` position of the entry.
            ``y`` : ``int``
                ``y`` position of the entry.
            ``text`` : ``str``
                Default unformatted text of the entry.
            ``font`` : :py:class:`~futura.text.Font` or ``tuple``
                Font of the label. This can be an object-oriented font or just
                a tuple containing the font description in ``(family, size)``.
                Defaults to :py:const:`~futura.DEFAULT_FONT`
            ``colors`` : ``list(tuple, (tuple, tuple, tuple)``
                Colors of the text in RGB. This is specified in a format
                ``[normal, (hover, press, disable)]``, which are its states and
                the appropriate colors displayed. Defaults to
                ``[(0, 0, 0), ((0, 46, 99), (47, 79, 79), (169, 169, 169))]``.

            ``history`` : ``bool``
                The user can press :kbd:`Alt-Left`\ or :kbd:`Alt-Right`\ to go
                back and forth between history. History can be marked when the
                user presses the entry and the position of the caret is
                changed.

        properties:
            document - document of the pyglet.text.layout.IncrementalTextLayout
            layout - internal pyglet.text.layout.IncrementalTextLayout for
                     efficient rendering
            caret - caret of the entry
            image - image displayed to give the entry a graphical look

            x - x position of the entry
            y - y position of the entry
            default - default text of the entry (changing this has no effect)
            font - font of the entry

            blinking - caret is visible or not visible

            length - length of the text in the entry
            max - maximum amount of characters in the entry

            text - displayed text of the entry
            selection - selected text of the entry
            layout_colors - layout colors of the entry
            validate - validation of the characters in the entry
            index - index of the caret (position)
            view - view vector of the entry

        methods:
            blink - blink the caret and switch its visibility
            insert - insert some text in the entry
            delete - delete some text from the entry
        """

        self._document = decode_attributed(text)

        self.layout = IncrementalTextLayout(self._document, 190, 24,
                                            batch=application.batch
                                           )

        self.image = Image(entry_normal, x, y)
        self.caret = Caret(self.layout)

        Widget.__init__(self, self.image)

        self.children = [self.image]

        self.application = application
        self.x = x
        self.y = y
        self.font = font
        self.default = text
        self.colors = BLACK

        self.width = width
        self.height = height

        self.layout.anchor_x = LEFT
        self.layout.anchor_y = CENTER

        self.history = []
        self.edit_bold = False
        self.edit_italic = False

        self.max = 2**32

        self.text_options = {
            "title_case" : True,
        }
        
        if self.ENABLE_BLINK:
            self.caret.PERIOD = self.PERIOD / 100

        else:
            self.caret.PERIOD = 0

        self.length = len(self.text)

        self._document.set_style(0, len(text), dict(font_name=DEFAULT_FONT[0],
                                                    font_size=DEFAULT_FONT[1],
                                                    color=four_byte(color)
                                                   )
                                )

        resize_bordered_images(self, Point(width, height), (5, 5, 5, 5))

        self.window.push_handlers(
            self.on_text,
            self.on_text_motion
        )

    def _update_position(self, x, y):
        """Update the position of the widget. This is called internally
        whenever position properties are modified.
        """

        self.layout.x = self.top - self.layout.width / 2
        self.image.x = x

        self.layout.y = y - 5
        self.image.y = y

    def _udpate_size(self, width, height):
        """Update the sizing of the widget. This is called internally whenever
        sizing properties are modified.
        """

        print("a")

    @property
    def document(self):
        """Pyglet document of the entry. This is far less efficient than
        modifying the current document, as relayout and recalculating glyphs
        is very costly.

        :type: :py:class:`~pyglet.text.document.FormattedDocument`
        """

        return self.layout.document

    @document.setter
    def document(self, document):
        self.layout.document = document

    @property
    def text(self):
        """Text of the entry. This should technically become a method and the
        "parameter" ``change_index`` is set to ``True``. This cannot be
        configured, only by subclassing this class.

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_edit` event if
        the text is different.

        :Parameters:
            ``text`` : ``str``
                Text to be displayed. This can be a string or a tuple, with the
                second indice the ``change_index`` parameter.
            ``change_index`` : ``bool``
                Index is changed after text input. If ``True``, the index is
                set to the end of the entry.

        :type: ``str``
        """

        return self.document.text

    @text.setter
    def text(self, text):
        before = self.text

        text = text or ""

        if isinstance(text, Tuple):
            self.document._delete_text(0, self.max)
            self.document._insert_text(0, text[0], None)

            self.dispatch_event("on_text_edit", before, text)

            # self.document.text = text

            if text[1]:
                # Put the caret to the end
                self.index = self.max

            return

        self.document._delete_text(0, self.max)
        self.document._insert_text(0, text, None)

        self.dispatch_event("on_text_edit", before, text)

        # self.document.text = text

    @property
    def index(self):
        """Index of the current caret position within the document. If the
        index exceeds the document length, the end of the document will be
        used instead.

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_interact` event
        if the index is different.

        :type: ``int``
        """

        return self.caret.position

    @index.setter
    def index(self, index):
        if self.caret.position == index:
            return

        self.caret.position = index

        self.dispatch_event("on_text_interact", index, None)

    def _get_mark(self):
        """Mark of the caret within the document.

        An interactive text selection is determined by its immovable end (the
        caret's position when a mouse drag begins) and the caret's position,
        which moves interactively by mouse and keyboard input.

        This property is ``None`` when there is no selection. It should not be
        set to zero, because that would just set the selection start index in
        the first position.

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_interact` event
        if the mark is different.

        :type: ``int``
        """

        return self.caret.mark

    def _set_mark(self, mark):
        if self.caret.mark == mark:
            return

        self.caret.mark = mark

        selection = None

        if self.selection[2]:
            selection = self.selection[2]

        self.dispatch_event("on_text_interact",
                            self.index,
                            selection
                            )

    def _get_selection(self):
        """Selection indices of the entry, which are defined with the property
        :py:attr:`~futura.widgets.Entry.layout_colors`. This is in the format
        ``(start, end)``.

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_interact` event
        when the selection is different.

        :type: ``tuple(int, int)``
        """

        # Pretty neat, but kind of long

        return (
                self.layout.selection_start,
                self.layout.selection_end,
                self.text[
                    self.layout.selection_start : self.layout.selection_end
                ]
               )

    def _set_selection(self, selection):
        self.mark = selection[1]

        self.layout.selection_start = selection[0]
        self.layout.selection_end = selection[1]

        if selection is not self.selection:
            self.dispatch_event("on_text_interact", self.index, selection)

    def _get_layout_colors(self):
        """Pyglet layout-specific colors of the entry. This is a tuple of three
        colors, defined here. Defaults are listed beside.

        1. Background color of the selection (46, 106, 197)
        2. Caret color (0, 0, 0)
        3. Text color of the selection (0, 0, 0)

        ``(selection, caret, text)``

        :type: ``list(tuple, tuple, tuple)``
        """

        return (
                self.layout.selection_background_color,
                self.caret.color,
                self.layout.selection_color
                )

    def _set_layout_colors(self, colors):
        self.layout.selection_background_color = colors[0]
        self.layout.selection_color = colors[2]

        self.caret.color = colors[1]

    @property
    def validate(self):
        """Validation of the entry. This is a string containing all of the
        characters the user is able to type. Common charsets can be found in
        the string module. Several validations are already provided::

        * :py:attr:`~futura.widgets.Entry.VALIDATION_LOWERCASE`
        * :py:attr:`~futura.widgets.Entry.VALIDATION_ADVANCED_DIGITS`
        * :py:attr:`~futura.widgets.Entry.VALIDATION_UPPERCASE`
        * :py:attr:`~futura.widgets.Entry.VALIDATION_PUNCTUATION`
        * :py:attr:`~futura.widgets.Entry.VALIDATION_LETTERS`
        * :py:attr:`~futura.widgets.Entry.VALIDATION_WHITESPACE`
        * :py:attr:`~futura.widgets.Entry.VALIDATION_DIGITS`
        * :py:attr:`~futura.widgets.Entry.VALIDATION_REGULAR`

        Using ``regex`` for real numerical inputs, password inputs, and other
        various types is currently in progress, with many bugs and possible
        errors.

        TODO: replace string validation with ``regex`` (IN PROGRESS)

        :type: ``re.compile``
        """

        return self._validate

    @validate.setter
    def validate(self, validate):
        self._validate = validate

    @property
    def placeholder(self):
        """Placeholder text of the entry. This is just "default" text, which is
        removed when the entry gains focus. When the entry loses focus, the
        placeholder text is displayed again. This can be used for instructions.

        :type: ``str``
        """

        return self._placeholder

    @placeholder.setter
    def placeholder(self, placeholder):
        self._placeholder = placeholder

    @property
    def view(self):
        """View vector as a :py:class:`~futura.Point` of the entry.

        :type: :py:class:`~futura.Point`
        """

        return Point(self.layout.view_x, self.layout.view_y)

    @view.setter
    def view(self, view):
        self.layout.view_x = view.x
        self.layout.view_y = view.y

    def blink(self, delta=0.5):
        """Toggle the caret between white and black colors. This is called
        every 0.5 seconds, and only when the caret has focus.

        :Parameters:
            ``delta`` : ``float``
                Delta time in seconds since the function was last called.
                Varies about 0.5 seconds give or take, because of calling
                delay, lags, and other inefficiencies. Defaults to ``0.5``.

        :rtype: ``bool``
        :returns: New alpha channel the caret's vertex list is currently in.
        """

        if not self.caret._list.colors[3] or \
            not self.caret._list.colors[7]:
            alpha = 255
        else:
            alpha = 0

        statemode = True
        
        if not alpha: statemode = False

        self.caret._list.colors[3] = alpha
        self.caret._list.colors[7] = alpha

        self.dispatch_event("on_blink", statemode)
        
        return alpha

    def insert(self, index, text, change_index=True):
        """Insert some text at a given index one character before the index.

            >>> entry.text = "Hello!"
            >>> entry.insert(5, " world")
            >>> entry.text
            "Hello world!"

            "Hello world!"
                   ^^^^^^^
                   678...

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_edit` event if
        text is deleted.

        :Parameters:
            ``index`` : ``int``
                Caret index/position of the text addition.
            ``text`` : ``str``
                Text to be added in the caret index.
            ``change_index`` : ``bool``
                Whether the index is updated to the end of the addition. This
                value usually just needs to be left where it is. Defaults to
                ``True``.
        """

        # self.text = insert(index, self.text, text)

        before = self.text

        self.document._insert_text(index, text, None)

        if not before == self.text:
            self.dispatch_event("on_text_edit", text, before)

        if change_index:
            self.index = self.index + len(text)

    def delete(self, start, end):
        """Delete some text at a start and end index, one character after the
        start position and a character after the end position.

        Text will be deleted between this range.

            >>> entry.text = "Hello world!"
            >>> entry.delete(5, 10)
            >>> entry.text
            "Hello!"

            "Hello world!"
                  ^^^^^^
                  6... 11

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_edit` event if
        text is deleted.

        :Parameters:
            ``start`` : ``int``
                Start index of the text to be deleted
            ``end`` : ``int``
                End index of the text to be deleted

        :rtype: ``str``
        :returns: Text deleted from the entry
        """

        # self.text = delete(start, end, self.text)

        before = self.text

        self.document._delete_text(start, end)

        if not before == self.text:
            self.dispatch_event("on_text_edit", self.text[start:end], before)

        self.mark = None

        return self.text[start:end]

    def clear(self, text=False, mark=0, index=0):
        """Clear the text in the entry and remove all of its caret properties.
        This is just a shortcut for setting the index, text, and mark to
        ``None``.

        :Parameters:
            ``text`` : ``bool`` or ``str``
                Clear the text in the entry. If a string is supplied, the text
                will be set to that. See
                :py:attr:`~futura.widgets.Entry.text`. Defaults to ``False``.
             ``mark`` : ``int``
                Reset the mark in the entry. See
                :py:attr:`~futura.widgets.Entry.mark`.
            ``index`` : ``int``
                Move the index of the caret to the first position. See
                :py:attr:`~futura.widgets.Entry.index`.
        """

        self.text = text or None
        self.mark = mark
        self.index = index

    # Text formatting functions

    def set_format(self, *args, **kwargs):
        selection = self.selection[0], self.selection[1]

        if self.mark: # Has mark (selection)
            if "bold" in kwargs:
                self.format_insert(*selection, bold=True)
            if "italic" in kwargs:
                # if "italic" in self.document.get_style_runs("italic"):
                self.format_insert(*selection, italic=True)
        # else:
        #     for key in kwargs:
        #         setattr(self, f"self.edit_{key}")

    def format_insert(self, *args, **kwargs):
        """Insert a formatted range to a range of indices in the entry. Formats
        are specified in **kwargs. Keep in mind that this is pyglet document
        formatting, not the custom formatting that has been provided by this
        module.

            >>> entry.format_insert(5, 10, bold=True, color=(255, 0, 0, 255))

        Overlapping formats are supported, so you can call this over the same
        range of text. This fixes the problem in tkinter, where overlapping
        tags are not supported.

        Dictionary from arguments credit to:
        https://stackoverflow.com/a/44412830/19573533/

        .. warning::

            This is still experimental and **currently does not work**. It is
            designed for rich text format for the entry (**bold**, *italic*,
            :u:`underline`\).
        """

        indices = args or (0, self.length)

        formats = {("arg" + str(index + 1)): argument for index, argument in enumerate(args)}
        formats.update(kwargs)

        del formats["arg1"]
        del formats["arg2"]

        self.document.set_style(*indices, formats)

    def format_replace(self, indices=None, **kwargs):
        """Replace a formatted range to new formatted text given indices. This
        has no effect if there are no styles over the range. Formats are
        specified in **kwargs. Keep in mind that this is pyglet document
        formatting, not the custom formatting that has been provided by this
        toolkit.

        :Parameters:
            ``indices`` : ``tuple(int, int)``
                A tuple of the start and end indices of the range. Defaults to
                ``None``, which is the whole range of the text.
        """

        indices = indices or (0, self.length)

        self.document.set_style(*indices, {})
        self.document.set_style(*indices, dict(kwargs))

    def draw(self):
        """Draw the entry. The layout is drawn with pyglet rendering.

        1. Image component
        2. Layout

        FIXME: there is a bug here. The
               :py:attr:`~pyglet.text.layout.TextLayout.anchor_x` and
               :py:attr:`~pyglet.text.layout.TextLayout.anchor_y` properties of
               the layout have to be set again and again. This makes
               performance deadly slow. (FIXED)
        """

        self.layout.begin_update()

        self.layout.anchor_x = LEFT

        self._document.set_style(0, len(self.text),
                                 dict(font_name=DEFAULT_FONT[0],
                                      font_size=DEFAULT_FONT[1],
                                      color=four_byte(self.colors)
                                     )
                                )
        self.layout.anchor_y = CENTER

        self.layout.end_update()

    def on_key(self, keys, modifiers):
        """A key is pressed. This is used for keyboard shortcuts.

        :kbd:`Control-A`\    Select all of the text.
        :kbd:`Control-V`\    Paste the clipboard's latest text.
        :kbd:`Control-C`\    Copy the selected text and add it to the clipboard
        :kbd:`Control-X`\    Cut the selected text and add it to the clipboard.
                             Essentially copying and deleting text; useful for
                             moving incorrectly placed text.

        If history is enabled, the user can hold :kbd:`Alt`\ and press
        :kbd:`Left`\ and :kbd:`Right`\ to scroll back history.
        """

        if modifiers & CONTROL:
            if keys == V:
                self.insert(self.index, clipboard_get(), change_index=True)
            elif keys == C:
                clipboard_append(self.selection[2])
            if keys == X:
                clipboard_append(self.selection[2])
                self.delete(self.selection[0], self.selection[1])
            elif keys == A:
                self.index = 0
                self.selection = (0, self.length, self.text)

            if keys == B:
                self.set_format(bold=True)
            if keys == I:
                self.set_format(italic=True)

        if modifiers & ALT and self._history_enabled:
            # This code is a little messy...

            if keys == KEY_LEFT:
                try:
                    self._history_index -= 1
                    self.index = self.history[self._history_index]

                except IndexError:
                    # Get the first item in the history
                    index = 0

                    self._history_index = index
                    self.index = self.history[index]

            if keys == KEY_RIGHT:
                try:
                    self._history_index += 1
                    self.index = self.history[self._history_index]

                except IndexError:
                    # Get the last item in the history
                    index = len(self.history) - 2 # Compensate for added index

                    self._history_index = index
                    self.index = self.history[index]

    def on_focus(self, approach):
        """The entry has focus, activating events. This activates the caret
        and stops a few errors.
        """

        if self.text == self.default:
            self.clear()

    def on_text(self, text):
        """The entry has text input. The entry adds text to the end.

        Internally, the entry does a few things::

            - Remove and delete all selected text
            - Update the caret position
            - Appends text to the end of the layout

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_edit` event.
        """

        if self.text_options["title_case"]:
            if not self.text:
                text = text.capitalize()

        if self.focus and \
            self.length < self.max:
            if self.validate:
                before = self.text
                self.caret.on_text(text)
                after = self.text

                if before is not after:
                    self.dispatch_event("on_text_edit", text, before)

                if not self.validate.match(after):
                    self.text = before

                return

            before = self.text
            self.caret.on_text(text)
            after = self.text

            if before is not after:
                self.dispatch_event("on_text_edit", text, before)

    def on_text_motion(self, motion):
        """The entry has caret motion. This can be moving the caret's position
        to the left with the :kbd:`Left`\ key, deleting a character previous
        with the :kbd:`Backspace`\ key, and more.

        This filters out :kbd:`Alt`\ key and the :kbd:`Left`\ or :kbd:`Right`\
        key is being pressed, as this is used for history.

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_edit` or the
        :py:meth:`~futura.widgets.Entry.on_text_interact` event, depending on
        if text is selected or deleted.

        :Paraneters:
            ``motion`` : ``int``
                Motion made by the user. This can be one of many motions,
                defined by keyboard constants found in the
                :py:mod:`~futura.application.key` module::

                * :py:const:`~futura.application.key.MOTION_LEFT`
                * :py:const:`~futura.application.key.MOTION_RIGHT`
                * :py:const:`~futura.application.key.MOTION_UP`
                * :py:const:`~futura.application.key.MOTION_DOWN`
                * :py:const:`~futura.application.key.MOTION_NEXT_WORD`
                * :py:const:`~futura.application.key.MOTION_PREVIOUS_WORD`
                * :py:const:`~futura.application.key.MOTION_BEGINNING_OF_LINE`
                * :py:const:`~futura.application.key.MOTION_END_OF_LINE`
                * :py:const:`~futura.application.key.MOTION_NEXT_PAGE`
                * :py:const:`~futura.application.key.MOTION_PREVIOUS_PAGE`
                * :py:const:`~futura.application.key.MOTION_BEGINNING_OF_FILE`
                * :py:const:`~futura.application.key.MOTION_END_OF_FILE`
                * :py:const:`~futura.application.key.MOTION_BACKSPACE`
                * :py:const:`~futura.application.key.MOTION_DELETE`
                * :py:const:`~futura.application.key.MOTION_COPY`
                * :py:const:`~futura.application.key.MOTION_PASTE`

                You can get the list of all text motions with
                :py:func:`~futura.application.key.motions_string` in the
                keyboard module. You can also get their keyboard combinations
                with :py:func:`~futura.application.key.motions_combinations`.
        """

        if not self.focus:
            return

        if self.keys[ALT]:
            if motion == MOTION_LEFT or motion == MOTION_RIGHT:
                return

        before = self.text
        self.caret.on_text_motion(motion)

        selection = None

        if self.selection[2]:
            selection = self.selection[:2]

        if motion == MOTION_BACKSPACE or motion == MOTION_DELETE:
            self.dispatch_event("on_text_edit", "", before)

            return

        self.dispatch_event("on_text_interact", self.index, selection)

    def on_text_select(self, motion):
        """Some text in the entry is selected. When this happens, the
        selected text will have a blue background to it. Moving the caret
        with a text motion removes the selection (does not remove the text).

        .. note:: Not called with caret mouse selections.

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_interact` event.
        """

        if not self.focus:
            return

        self.caret.on_text_motion_select(motion)
        self.dispatch_event("on_text_interact",
                            self.index,
                            self.selection[:2]
                           )

    def on_press(self, x, y, buttons, modifiers):
        """The entry is pressed. This will do a number of things::

            - The caret's position is set to the nearest character.
            - The history will add the caret's position.
            - If text is selected, the selection will be removed.
            - If the Shift key is being held, a selection will be created
              between the current caret index and the closest character to
              the mouse.
            - If two clicks are made within 0.5 seconds (double-click), the
              current word is selected.
            - If three clicks are made within 0.5 seconds (triple-click), the
              current paragraph is selected.
            - If there is a placeholder text, the text is removed.

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_interact` event.
        """

        # This previously had to be used, then did not. In arcade's GUI toolkit
        # it is used.
        #
        # Probably related to pyglet glyph rendering, anchoring position and
        # the fact that the pyglet coordinate system is vastly different from
        # arcade's in some areas.
        #
        # For some places in pyglet, the coordinate (0, 0) is in the center of
        # the screen, but in other places it is at the very bottom right.
        _x, _y = x - self.layout.x, y - self.layout.y

        if self.text == self.placeholder:
            self.text = None

        index_before = self.index

        self.caret.on_mouse_press(x, y, buttons, modifiers)

        index_after = self.index

        self.mark = None

        if index_before is not index_after:
            # Add history
            self.history.append(index_after)
            self.dispatch_event("on_text_interact", self.index, None)

        if self.keys[SHIFT]:
            # Not required, but cleaner
            indices = sorted((index_before, index_after))

            self.selection = indices
            self.mark = max(indices)

    def on_drag(self, x, y, dx, dy, buttons, modifiers):
        """The user dragged the mouse when it was pressed. This can create
        selections on entries.

        Dispatches the :py:meth:`~futura.widgets.Entry.on_text_interact` event.
        """

        _x, _y = x - self.layout.x, y - self.layout.y

        if self.press:
            self.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
            self.dispatch_event("on_text_interact",
                                self.index,
                                self.selection[:2]
                               )

            self.index = self.caret.position
        else:
            if self.focus:
                self.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
                self.dispatch_event("on_text_interact",
                                    self.index,
                                    self.selection[:2]
                                   )

                self.index = self.caret.position

    def update(self):
        """Update the caret and entry. This schedules caret blinking and
        keeps track of focus.
        """

        if not self.length == len(self.text):
            self.length = len(self.text)

        if self.hover and not self.focus:
            self.image.texture = self.hover_image
        if self.focus:
            self.image.texture = self.focus_image

        if not self.hover and \
            not self.press and \
            not self.disable:
            self.image.texture = self.normal_image

        if self.focus:
            self.caret.on_activate()

        else:
            self.index = 0
            self.mark = None

            self.caret.on_deactivate()

    def on_text_edit(self, text, previous):
        """Text in the entry has been edited or modified. This may be done via
        user interaction or script. Text deletions can be found by checking the
        difference between the previous text and the new text.

        :Parameters:
            ``text`` : ``str``
                Text that was entered. Usually just a character in length. If a
                deletion was made, then the text will be a blank string (`""`).
            ``previous`` : ``str``
                Previous text before modification.

        :type: event
        """

    def on_text_interact(self, index, selection):
        """Text in the entry was interacted somehow by the user. This is
        dispatched on text selection, or motion related the caret. Deletions
        do not trigger this event or other text modifications.

        :Parameters:
            ``index`` : ``int``
                Index of the caret. This can be accessed by the
                :py:attr:`~futura.widgets.Entry.index` property. See
                :py:attr:`~futura.widgets.Entry.index` for more details.
            ``selection`` : ``list``
                Selection of the text (ranges) made by the user. See
                :py:attr:`~futura.widgets.Entry.selection` for more details.

        :type: event
        """
    
    def on_blink(self, state):
        """The caret was blinked. Used to indicate whether or not a text input
        has the current application focus.
        
        This event takes a ``state`` parameter; this is the blink state of the
        caret. A ``state`` parameter of ``True`` means that the caret has been
        solid; a ``state`` of ``False`` means that the caret has been
        deactivated.
        
        :Parameters:
            ``state`` : ``bool``
                Current blink state of the caret. See above docs for details.
        
        :type: event
        """

Entry.register_event_type("on_text_edit")
Entry.register_event_type("on_text_interact")
