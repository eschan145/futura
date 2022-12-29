************************
Keyboard and mouse input
************************

Futura provides work with the keyboard and mouse, including key and mouse state
handlers and various constants.

The associated filename is :py:mod:`~futura.key`.

State handlers
==============

A state handler is designed to keep track of which buttons or keys are being
pressed or held down. Instead of using an event, which is not called when
something is held down, you can use this if you want to rapidly call something
when a key or mouse button is being pressed.

Events are pushed automatically.

Key state handler
-----------------

A key state handler can check if keys are being held down by mapping. It was
inspired by pyglet's :py:class:`~pyglet.key.KeyStateHandler`.

    >>> keys = Keys()

    # Press and hold down the "right" key...

    >>> keys[RIGHT]
    True
    >>> keys[LEFT]
    False

The key state handler only uses a pyglet window's
:py:meth:`~pyglet.Window.on_key_press` and
:py:meth:`~pyglet.window.Window.on_key_release` events. The two properties it
has are :py:attr:`~futura.key.Keys.window` (the pyglet window) and
:py:attr:`~futura.key.Keys.data` (used internally for mapping).

Mouse state handler
-------------------

A mouse state handler is very similar to a key state handler, in that it pushes
events automatically and uses mapping.

    >>> mouse = Mouse()

    # Press and hold down the left mouse button...

    >>> mouse[MOUSE_BUTTON_LEFT]
    True
    >>> mouse[MOUSE_BUTTON_RIGHT]
    False
    >>> mouse.x
    200

It uses more window events, though.

* :py:meth:`~pyglet.window.Window.on_mouse_press`
* :py:meth:`~pyglet.window.Window.on_mouse_release`
* :py:meth:`~pyglet.window.Window.on_mouse_motion``
* :py:meth:`~pyglet.window.Window.on_mouse_drag`

But it has more properties. It has :py:attr:`~futura.keys.Mouse.x` and
:py:attr:`~futura.key.Mouse.y` properties (also a
:py:attr:`~futura.key.Mouse.point` property), and a
:py:attr:`~futura.key.Mouse.press` property. This is only for the left mouse
button, as only that invokes a widget's
:py:meth:`~futura.widgets.base.Widget.on_press` event.

Keyboard and mouse constants
============================

Futura provides a host of keyboard and mouse constants. This aids so that you
do not have to define your own. All modifiers are done in powers of two, so you
can use a bit-wise ``"and"`` to detect multiple modifiers.

   if modifiers & CONTROL and \
      modifiers & ALT and \
      modifiers & DELETE:
      # Control-Alt-Delete

Do not use::

    if modifiers == CONTROL:

There are three mouse constants::

* :py:const:`~futura.key.MOUSE_BUTTON_LEFT`
* :py:const:`~futura.key.MOUSE_BUTTON_MIDDLE`
* :py:const:`~futura.key.MOUSE_BUTTON_RIGHT``

Keyboard constants are pretty straight-forwards, like
:py:const:`~futura.key.PERIOD`, :py:const:`~futura.key.B`,
:py:const:`~futura.key.CONTROL`, :py:const:`~futura.key.KEY_UP`,
:py:const:`~futura.key.KEY_1`, :py:const:`~futura.key.NUM_1`, and
:py:const:`~futura.key.UNDO`. Many of these are motions or modifiers. **All
motions start with the ``MOTION`` prefix.**

A full list of keys can be found in the API docs.

Helper functions
================

A few helper functions are provided. Their names are self-descriptive. The
functions are :py:func:`~futura.key.modifiers_string`,
:py:func:`~futura.key.key_string`, :py:meth:`~futura.key.motions_string`,
:py:func:`~futura.key.motions_combinations`, and
:py:func:`~futura.key.user_key`.

    >> modifiers_string(SHIFT | CONTROL|)
    "SHIFT|CONTROL"

All the functions that end with the ``-string`` prefix return a string of the
type. The layout for :py:func:`~futura.key.motions_combinations` is
``key (name, control?) : motion``, as it returns a map of the motion
combinations. :py:func:`~futura.key.user_key`` returns a key symbol for a key
not supported by futura or pyglet.

Key types
=========

The motion key type describes a motion made by an entry widget, or more
specifically, a pyglet :py:class:`~pyglet.text.layout.IncrementalTextLayout`.
