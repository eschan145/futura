"""An application class is provided by futura to manage widgets and update them
in a batch. You *must* use an instance of the
:py:class:`~futura.application.Application` class to do anything with widgets.
"""

from arcade import SpriteList, Window
from pyglet.clock import get_frequency
from pyglet.graphics import Batch

from futura.color import BLACK
from futura.key import SHIFT, TAB
from futura.widgets import Image
from futura.text import add_prefix_and_suffix

from collections import namedtuple

_GlTuple = namedtuple("GlTuple", ["version", "api"])

GlTuple = _GlTuple(version=(3, 3),
                   api="gl"
                  )

class WindowException(Exception):
    """Base class for all window-related exceptions."""

    pass


class Application(Window):
    """Application object to draw and update widgets. It updates and draws
    widgets in a batch, which helps with speed.

    Use the :py:meth:`~futura.application.Application.add` method to add
    widgets to the event stack and list::

        >>> application.add(widget)

    We recommend subclassing the application class::

        >>> from futura import Application
        >>> class MyApplication(Application):
                ...

    The application is heavily linked to the arcade :py:class:`~arcade.Window`,
    so any function calls are sent to the arcade window event manager, as well
    as any property interaction.

    Previously the application class was separate from the ``Container`` class;
    however these have been merged to avoid conflicts with current containers
    and whatnot.

    A window is a "heavyweight" object occupying operating system resources.
    The "client" or "content" area of a window is filled entirely with an
    OpenGL viewport. Applications have no access to operating system widgets or
    controls; all rendering must be done via OpenGL.

    Windows may appear as floating regions or can be set to fill an entire
    screen (fullscreen).  When floating, windows may appear borderless or
    decorated with a platform-specific frame (including, for example, the
    title bar, minimize and close buttons, resize handles, and so on).

    While it is possible to set the location of a window, it is recommended
    that applications allow the platform to place it according to local
    conventions.  This will ensure it is not obscured by other windows
    and appears on an appropriate screen for the user.

    Once an application is destroyed, using the
    :py:meth:`~futura.application.Application.exit` method, its GL context will
    be invalid and cannot be reused.

    Windows are platform-independent. (Windows, OS X, Linux, Raspbian)
    """

    # Valid style names. Used for error checking.
    valid_style_names = (
                         # Default window style
                         Window.WINDOW_STYLE_DEFAULT,
                         # Window style for pop-up dialogs
                         Window.WINDOW_STYLE_DIALOG,
                         # Window style for toolbar windows
                         Window.WINDOW_STYLE_TOOL,
                         # Window style without any border or decoration
                         Window.WINDOW_STYLE_BORDERLESS,
                         # Window style for transparent, interactable windows
                         Window.WINDOW_STYLE_TRANSPARENT,
                         # Window style for transparent, topmost,
                         # click-through-able overlays
                         Window.WINDOW_STYLE_OVERLAY
                        )

    def __init__(
                 self, title=None, width=None, height=None,
                 resizable=False, fullscreen=False,
                 style=Window.WINDOW_STYLE_DEFAULT,
                 visible=True, vsync=False, antialiasing=True,
                 file_drops=True, background=BLACK,
                 gl_setting=GlTuple,
                 gc_mode="context_gc", samples=4
                ):

        """Create a container group to draw and update widgets, connected to
        its :py:class:`~arcade.Window` "parent".
        
        :Parameters:
            ``title`` : ``str`` or ``None``
                Initial title/caption which appears in the toolbar.
            ``width`` : ``int``
                Width of the window. The window size **does not** include the
                title bar. Defaults to 960.
            ``height`` : ``int``
                Height of the window. The window size **does not** include the
                title bar. Defaults to 540.
            ``resizable`` : ``bool``
                If ``True`` the window can be resized by dragging the mouse on
                the corners and edges of the window.
                
                It is recommended to enable supporting this, but changing the
                window size can mess up game coordinates and settings.
                
                If set to ``False``, setting the application width and height
                will not function properly until it is enabled once again.
                
                Defaults to ``False``.
            ``fullscreen`` : ``bool``
                If ``True`` the window will start at fullscreen, which means
                that the toolbar is hidden and the dimensions take up the
                entire screen space instead of floating.
                
                It is usually triggered with the key :kbd:`F11`\ on most
                applications. Defaults to ``False``.
            ``style`` : ``str``
                Toolbar or background style of the window. A window style is
                determined by an attribute with the prefix ``"-WINDOW_STYLE"``.
                
                The window style cannot be modified after initialization. You
                can get the full list of style attributes with the property
                :py:attr:`~futura.application.Application.valid_style_names`.
                Defaults to
                :py:attr:`~futura.application.Application.WINDOW_STYLE_DEFAULT`
            ``visible`` : ``bool``
                Determines if the window is visible immediately after creation.
                Set this to ``False`` if you would like to change any
                attributes of the window before having it appear to the user.
                Defaults to ``True``.
            ``vsync`` : ``bool``
                If ``True`` buffer flips are synchronized to the primary
                screen's vertical retrace, eliminating flicker. It waits until
                they are synchronized, so your fps (frames per second) may
                drop.

                .. important::

                    Only use this if your application experiences screen
                    tearing. *It waits until the vertical retrace is
                    synchronized*, so your fps (frames per second) may
                    experience a frame drop.

                Defaults to ``False`` to keep the fps up.
            ``antialiasing`` : ``bool``
                If ``True`` then OpenGl's anti-aliasing will be enabled. It
                helps in adding greater realism to the display by smoothing
                jagged edges on curved lines and diagonals. Defaults to
                ``True``.
            ``file_drops`` : ``bool``
                If ``True`` then file drops will be enabled. Can dispatch the
                :py:meth:`~futura.widgets.Widget.on_file_drop` event. Defaults
                to ``True``.
            ``background`` : :py:class:`~futura.color.Color` or ``tuple``
                Background color of the application. Currently has no effect.
                Defaults to ``(0, 0, 0)``.
            ``gl_setting`` : ``NamedTuple``
                The OpenGL settings of the window GL context. It is a
                ``NamedTuple``, with two attributes::

                    * ``version`` (``(3.3)``) - requested OpenGL version. It
                      can be overridden when using more advanced OpenGL
                      features.
                    * ``api`` (``"gl"``) - requested OpenGL API.

            ``gc_mode`` : ``str``
                Decides how OpenGL objects should be garbage collected. The
                default is ``"context_gc"``, but can be changed to ``"auto"``.
            ``samples`` : ``int``
                Number of samples used in antialiasing. Usually, this can be
                set to 2, 4, 6, or 8, but defaults to 4.
        """

        # 1. NoneType capabilities and defaults

        # 1-1 Width and height to 960 and 540

        # Set the width and the height to 960 and 540 if no width or height is
        # set. This is also the default value for a pyglet window, but not for
        # an arcade window (800x600)
        if not width or not height:
            # Kind of inefficient, but too small of a difference to think
            # about. But it keeps stuff consistent when initializing the
            # pyglet window.
            width = 960
            height = 540

        # 1-2 Background color
        if not background:
            # Only used once, so import it here
            from futura.color import WHITE
            background = WHITE

        # 1-3 OpenGL settings
        
        # Usually this should not be in a NamedTuple, but it's better than a
        # regular tuple and we don't want two different parameters.
        _gl_version = gl_setting.version
        _gl_api = gl_setting.api

        # 2. Error catching

        # Sanity check values
        if width < 0 or height < 0:
            raise ValueError("The specified width or height is less than "
                             "zero. Double-check that it is a positive "
                             "number. The minimum size %s was entered. "
                             % min(width, height)
                            )

        if style not in self.valid_style_names:
            raise WindowException("The style name \"%s\" cannot be found. "
                                  "Check for typos or misspellings. The list "
                                  "of style names can be accessed by the "
                                  "attribute \"valid_style_names\"." % style
                                 )

        if not gc_mode == "context_gc" and \
           not gc_mode == "auto":
            raise TypeError("The parameter \"gc_mode\" must be either one of "
                            "two options: \"context_gc\" or \"auto\". The "
                            "option \"%s\" is not valid." % gc_mode
                           )

        Window.__init__(self,
                        width=width,
                        height=height,
                        title=title,
                        resizable=resizable,
                        fullscreen=fullscreen,
                        style=style, visible=visible,
                        vsync=vsync,
                        antialiasing=antialiasing,
                        gl_version=_gl_version,
                        gc_mode=gc_mode,
                        samples=samples
                       )

        # 2. Set application properties

        self.focus = None
        self.enable = True

        self.widgets = []
        self.fps_list = []
        self._widgets = []
        self.groups = []

        self.track_fps = True

        self.batch = Batch()
        self.widget_sprites = SpriteList()
        
    def _get_title(self):
        """Title or caption of the window. This is the text that is displayed
        on the top of the screen. Currently, changing text color, font, and
        other styles is not supported. In the future, a custom toolbar could be
        implemented, for customization of colors and styles.

        Raises an ``AssertionError`` if there is no set window.

        :type: ``str``
        """

        assert self.window, (
                             "No window is active. It has not been created "
                             "yet, or it was closed. Be sure to set the "
                             "window property of the container before adding "
                             "any widgets."
                            )

        return self.window.get_caption()

    def _set_title(self, title):
        assert self.window, (
                             "No window is active. It has not been created "
                             "yet, or it was closed. Be sure to set the "
                             "window property of the container before adding "
                             "any widgets."
                            )

        title = str(title or "")

        self.window.set_caption(title)

    title = property(_get_title, _set_title)

    def get_fps(self):
        """Current update rate in frames per second (fps). This should not vary
        between multiple containers. Drawing an fps display can aid in
        profiling and measuring of the time between code.

        NOTE: this is not the refresh rate. The refresh rate is how fast the
              monitor redraws itself. Most monitors have a refresh rate of 60
              hertz or 120 hertz. Fps is the number of update frames per
              second. Higher fps will speed up events and collision checks.

        :rtype: ``float``
        :returns: Current speed measured in frames per second
        """

        # Don't use arcade.get_fps(). This measures incorrectly.

        return get_frequency()

    def get_average_fps(self, prefix=None, suffix=None):
        """Average update rate in frames per second (fps). The items of the fps
        list are averaged and returned.

        :Parameters:
            ``prefix`` : ``str``
                Prefix characters to add *before* text. Defaults to ``None``.
            ``suffix`` : ``str``
                Suffix characters to add *after* text. It could be something
                like ``" fps"``. Defaults to ``None``.

        :rtype: ``float``
        :returns: Averaged speed measured in frames per second
        """

        text = sum(self.fps_list) / len(self.fps_list)

        if prefix or suffix:
            text = add_prefix_and_suffix(str(text), prefix, suffix)

        return text    

    def add(self, *widgets):
        """Add widgets to the drawing list. It is the equivalent of tkinter's
        ``pack``, ``place``, or ``grid`` methods, Kivy's ``add_widget``, and
        PyQt5's ``show`` method.
        
        In the future groups may be able to be taken in the ``widgets``
        parameter.

        Raises an ``AssertionError`` if there is no set window.

        :Parameters:
            ``widgets`` : ``List[``:py:class:`~futura.widgets.Widget``]``
                Widget(s) to add to the list. Multiple can be specified with
                one call, but it is neater to do them separately. 
        """

        for widget in widgets:
            widget.application = self
            
            widget._create()
            
            widget._created = True
            
            if widget.children:
                self.widgets.append(widget)

            self._widgets.append(widget)

        self.focus = widgets[-1]
        
    def draw(self):
        """Draw the container's widgets. This should be manually called in the
        draw function of your application.
        """
        
        [widget.draw() for widget in self._widgets]

        for group in self.groups:
            group.draw()

        if self.track_fps:
            self.fps_list.append(self.get_fps())

        with self.ctx.pyglet_rendering():
            self.batch.draw()
            
            # A shadow effect not in progress anymore

            # Interesting feature:
            # Press Control + slash when on the line with "shade = 1"
            # The text "shade" will turn light green for a second.

    def draw_bbox(self, width=1, padding=0):
        """Draw the bounding box of each widget in the list. The drawing is
        cached in a :py:class:`~arcade.ShapeElementList` so it won't take up
        more time. This can also be called ``draw_hitbox`` or ``draw_hit_box``.

        :see: :py:meth:`~futura.widgets.Widget.draw_bbox`
        """

        [widget.draw_bbox(width, padding) for widget in self.widgets]

    draw_hitbox = draw_bbox # Alias
    draw_hit_box = draw_bbox

    def exit(self):
        """Exit the event sequence and delete all widgets.

        1. The :py:meth:`~futura.widgets.Widget.delete` method is called on all
           of the widgets.
        2. The widget list is cleared.
        3. The :py:meth:`~futura.application.Application.enable` property is
           set to ``False``.
        """

        [widget.delete() for widget in self.widgets]

        self.widgets = []

        self.enable = False

    def on_key_press(self, keys, modifiers):
        """A key is pressed. This is used to detect focus change by pressing
        :kbd:`Tab`\ and :kbd:`Shift-Tab`\.
        """

        if keys == TAB:
            if modifiers & SHIFT:
                direction = -1
            else:
                direction = 1

            if self.focus in self.widgets:
                i = self.widgets.index(self.focus)
            else:
                i = 0
                direction = 0

            self.focus = self.widgets[(i + direction) % len(self.widgets)]

            if self.focus.children:
                self.focus.focus = True

            for widget in self.widgets:
                if not widget == self.focus:
                    if widget.children:
                        widget.focus = False
