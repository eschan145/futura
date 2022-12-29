**************************
Useful interactive widgets
**************************

Many high-level widgets are provided and built-in by futura. This in-depth
tutorial covers how to use them and harness their full functionality. These
widgets have predefined methods, such as invoking, editing, or viewing, and
they have many easily accessible.

The associated filename is :py:mod:`~futura.widgets`. It has three submodules::

1. :py:mod:`~futura.widgets.widgets` - user interface interactive widgets
2. :py:mod:`~futura.widgets.shapes` - various object-oriented shapes
3. :py:mod:`~futura.widgets.base` - base widgets, foundations

Support for states is still in progress. The chart below shows the current
supported and not supported states.
    
+---------------+---------+---------+---------+---------+---------+
|Widget type    |Label    |Button   |Entry    |Slider   |Toggle   |
+===============+=========+=========+=========+=========+=========+
|Hover          |X        |X        |X        |X        |X        |
+---------------+---------+---------+---------+---------+---------+
|Press          |X        |X        |X        |X        |X        |
+---------------+---------+---------+---------+---------+---------+
|Focus          |Not supported      |X        |X        |X        |
+---------------+---------+---------+---------+---------+---------+
|Disable        |X        |X        |Not supported                |
+---------------+---------+---------+---------+---------+---------+

The widgets below are essential components, with either one or the other used
as components in all built-in widgets. All built-in widgets are interactive,
except :py:class:`~futura.widgets.Image` widgets.

-------------------------------------------------------------------------------

Label
=====

A :py:class:`~futura.widgets.Label` widget can display a modified subset of
HTML 4.0 transitional. It is an essential component in many other widgets. The
:py:class:`~futura.widgets.Label` widget uses a modified pyglet text label
(subclassed from :py:class:`~pyglet.text.DocumentLabel`).

Similar to :py:class:`~futura.widgets.Button` widgets, a
:py:class:`~futura.widgets.Label` supports a minimal
:py:meth:`~futura.widgets.Label.invoke` command and commands can be specified
in the parameters. Label widgets can have multiple colors, for different
states. This is why their color looks like this::

    [normal, (hover, press, disable)]

This is ignored by multiline labels; it doesn't make sense.

A focus color can additionally be specified in the tuple (index ``[1][2]``).

.. important::

   In the future, the HTML format may be changed to a futura custom one.
   Support for HTML will still be enabled and will not change, but maybe a
   ``format`` option for a label will be in the parameters.

   There would be two decoders::

   * :py:class:`~futura.text.formats.HTMLDecoder` - deprecated support
     for HTML decoding. Should still work.
   * ``AttributedDecoder`` - preferred custom-made futura format

If it's too complicated for you, you can leave it as is.

Label widgets are designed for speed, and tens of thousands can be drawn. If
the text content is changed regularly, this might be different. It can be fixed
using the :py:attr:`~futura.widgets.Label.UPDATE_RATE` property.

The update rate can be modified. The higher the update rate, the faster the
label's text will be updated, but it will cause a small performance drop. To
force the text of the label (ignore the update rate), call
:py:meth:`~futura.widgets.Label.force_text`. The update rate is set on default
once every two frames (2).

You may want to modify the update rate depending on what you want. For a timer
or a score display, you may want to raise the update rate, but for an
instructions label, this can be set to zero.

.. hint::

    :py:meth:`~futura.widgets.Label.force_text` is called on label
    initialization. A label that does not change its text after creation can
    have an update rate of zero.

See https://pyglet.readthedocs.io/en/latest/programming_guide/text.html for
details regarding text specification and drawing.

Speedups
--------

A label is sped up by the
:py:meth:`~pyglet.text.layout.TextLayout.begin_update` and
:py:meth:`~pyglet.text.layout.TextLayout.end_update` methods for the
:py:class:`~pyglet.text.layout.TextLayout` pyglet class. This waits until all
modifications have passed and are registered, then pushes it to the update
stack. This means multiple modifications can take the same amount of time.

Updates enabled
```````````````

:py:meth:`~pyglet.text.layout.TextLayout.begin_update`

    label.text = new_text
    label.x = new_x_position

:py:meth:`~pyglet.text.layout.TextLayout.end_update`

    # (Update glyph vertices)

Updates disabled
````````````````

    label.text = new_text
    # (Update glyph vertices)

    label.x = new_x_position
    # (Update glyph vertices)

In this visualization, using the speedups requires only one glyph update, but
without requires two.

Glyph updates are extremely performance-expensive, especially for text format
decoding.

Image
=====

The :py:class:`~futura.widgets.Image` widget is an instance of an arcade
:py:class:`~arcade.Sprite`. It is used to display images on various widgets.

.. important::

    It is recommended to use this instead of regular sprites in the widget
    tree, or you will need to create your own to fit the guidelines.

Parameters are similar to its parent.

It's recommended to use a regular, rectangular bounding box for an image unless
it must be detailed. You can set the bounding box to either ``"simple"`` or
``"detailed"``. Detailed bounding boxes make collision calculations much, much,
slower. Especially if the bounding box is a polygon with hundreds and hundreds
of points (e.g. a circle). This is currently not used (yet).

There usually is no reason to insert a game sprite into the GUI tree, the
inverse should be done instead.

---

Button
======

The :py:class:`~futura.widgets.Button` widget is designed to create a clickable
widget, capable of invoking commands. A callable can be given in the
``command`` parameter to specify a function (``callable``) to be called
whenever the button is pressed. Optional parameters can follow, as a list.

    button = Button("Click me!", 50, 20, command=self.fire)

.. hint::

    You should not call a function directly in the ``command`` parameter. Nor
    should you use ``lambda``.

Arguments can be passed for customization of the button. It also supports
border resizing, so you can customize pixel width and height. Buttons have
several parameters :py:class:`~futura.widgets.Label` s inherit, like ``font``.

+-----------+-------------------------------------------------------+
|Event      |Description                                            |
+===========+=======================================================+
|``on_push``|The command associated with the button has been invoked|
+-----------+-------------------------------------------------------+

Commands and Invoking
---------------------

If you want to bind a key to a button, you can use the
:py:attr:`~futura.widgets.Button.keys` property, which can be a list of keys or
a single key. When any of these keys are pressed, the command associated with
the button will be invoked. You can also use the
:py:meth:`~futura.widgets.Button.bind` and
:py:meth:`~futura.widgets.Button.unbind` methods.

.. warning:: Modifiers are not supported

Binding keys looks like this::

    button.keys = [ENTER, KEY_UP]
    button.unbind(KEY_UP)

In this example, only pressing the :kbd:`Enter`\ key will invoke the button.

A button can be programmatically invoked by calling the
:py:meth:`~futura.widgets.Button.invoke` command.

Entry
=====

An :py:class:`~futura.widgets.Entry` widget can display user-editable text and
allow selecting and deleting that text. It uses pyglet's
:py:class:`~pyglet.text.layout.IncrementalTextLayout` and its
:py:class:`~pyglet.text.caret.Caret`. Unlike pyglet, it supports selecting all
text, copying/pasting/cutting selected text, and more.

Here is a quick example of creating an entry::

    entry = Entry(None, 50, 50)

You can try activating its focus and typing in it, as well as selcting and
deleting text. Also feel free to play around with the clipboard.

.. note:: Rich text formatting is currently in-progress

.. shouldn't be exact to API docs. Should be paraphrased.

Entries have many properties. These are listed below.

* :py:attr:`~futura.widgets.Entry.text` - text of the entry. This uses the
  :py:attr:`~futura.widgets.Entry.UPDATE_RATE` property to determine if it will
  be updated. Dispatches the :py:meth:`~futura.widgets.Entry.on_text_edit`
  event if the text is changed. Will have no effect if the text is the same as
  the current.
* :py:attr:`~futura.widgets.Entry.document` - HTML document of the label. It is
  far less efficient than changing the text.
* :py:attr:`~futura.widgets.Entry.index` - index of the caret. If the index
  exceeds the document length, the end of the document will be used instead.
  Dispatches the :py:meth:`~futura.widgets.Entry.on_text_interact` event if the
  index is different.
* :py:attr:`~futura.widgets.Entry.mark` - mark of the caret within the
  document. An interactive text selection is determined by its immovable end
  (the caret's position when a mouse drag begins) and the caret's position,
  which moves interactively by mouse and keyboard input. Set to ``None`` when
  there is no selection. **Should not be set to zero** (mark set to first
  character).
  Dispatches the :py:meth:`~futura.widgets.Entry.on_text_interact` event.
* :py:attr:`~futura.widgets.Entry.selection` - selection of text within the
  layout. Defined with the property
  :py:attr:`~futura.widgets.Entry.layout_colors`. This is in the format
  ``(start, end)``. Dispatches the
  :py:meth:`~futura.widgets.Entry.on_text_interact` event.
* :py:attr:`~futura.widgets.Entry.layout_colors` - colors of the pyglet
  layout::

   1. Background color of the selection ``(46, 106, 197)``
   2. Caret color ``(0, 0, 0)``
   3. Text color of the selection ``(0, 0, 0)``

* :py:attr:`~futura.widgets.Entry.view` - view vector of the
  :py:class:`~pyglet.text.layout.IncrementalTextLayout`. It is a
  :py:class:`~futura.Point`, with :py:attr:`~futura.Point.x` and
  :py:attr:`~futura.Point.y` properties. You can set the view by ``view.x``
  or ``view.y``.

Other properties include :py:attr:`~futura.widgets.Entry.layout` for the
entry's :py:class:`~pyglet.text.layout.IncrementalTextLayout` and
:py:attr:`~futura.widgets.Entry.caret`, for its pyglet caret. Any unlisted
property does not have ``setters`` or ``getters`` or has less importance.

Text editing
------------

.. Just one character away!

The entry widget comes with several methods for modifying text
programmatically.

Inserting text
``````````````

You can use the :py:meth:`~futura.widgets.Entry.insert` method to insert some
text, given an index, text to be inserted, and whether or not the index should
be changed. The :py:meth:`~futura.widgets.Entry.on_text_edit` event may be
dispatched.

``insert(index, text, change_index=True)``

    >>> entry.text = "Hello!"
    >>> entry.insert(6, " world")
    >>> entry.text
    "Hello world!"

Text indices look like this::

.. rst-class:: plain

    "Hello world!"
           ^^^^^^
     0 2 4 6 8...
      1 3 5 7

Note that it starts at index 0.

The parameter ``change_index`` determines if the index is added to the end of
the addition. This is enabled by default. Any marks or selections will be
removed.

.. warning::

    Do not use the document's
    :py:meth:`~pyglet.text.document.AbstractDocument.insert_text` method. This
    will not work correctly. This method uses
    :py:meth:`~pyglet.text.document.AbstractDocument._insert_text` instead.

Deleting text
`````````````

The :py:meth:`~futura.widgets.Entry.delete` method deletes text given indices.

``delete(start, end)``

    >>> entry.text = "Hello world!"
    >>> entry.delete(5, 10)
    >>> entry.text
    "Hello!"

The :py:meth:`~futura.widgets.Entry.on_text_edit` event can be dispatched. Any
marks or selections will be removed, and the caret position will force change
to the first specified position.

Other methods and features
--------------------------

There are some other not largely used methods.

* :py:meth:`~futura.widgets.Entry.blink` - blink the caret. It sets the caret's
  :py:attr:`~pyglet.text.caret.Caret._list` alpha colors to either ``255`` or
  ``0``. It requires a ``delta`` parameter because it was used before caret
  blink was stable and working correctly. It is now unused.
* :py:meth:`~futura.widgets.Entry.clear` - removes and resets the entry.
  Largely used internally as a shortcut.

A largely experimental property, :py:attr:`~futura.widgets.Entry.text_options`,
is a extra validation for the entry. It is a map and only one option is
supported; ``title_case``. If ``title_case`` is set to True, then the first
word of the entry will be forced to be capitalized (for a title).

Constants and properties
````````````````````````

The :py:class:`~futura.widgets.Entry` widget comes with a few properties that
can be used to enhance customization of the entry.

To set any constant, modify it with the class attribute::

    Entry.[CONSTANT] = VALUE

This will change the constant. You do not have to do this multiple times, and
it will *only* affect new entries, not existing ones.

Blink period
^^^^^^^^^^^^

**Type**: ``int``
**Source**: :py:attr:`~futura.widgets.Entry.PERIOD`

Blink period of the caret, in milliseconds. Once set this can not be changed,
except for modifying the pyglet caret's
:py:attr:`~pyglet.text.caret.Caret.PERIOD` property directly.

A default blinking period for a regular caret (this may vary from system to
system), is twice every second. Futura's default blink period is 500 ms.

Enable blink
^^^^^^^^^^^^

**Type**: ``bool``
**Source**: :py:attr:`~futura.widgets.Entry.ENABLE_BLINK``

Whether caret blinking should be enabled on default. A disabled caret leaves
the effect of a bug in the display. The user may also find this ambiguous.

+--------------------+------------------------+-------------------------------+
|Event               |Parameters              |Description                    |
+====================+========================+===============================+
|``on_text_edit``    |``text``, ``previous``  |Text in the entry has been     |
|                    |                        |edited or modified. This may be|
|                    |                        |done via user interaction or   |
|                    |                        |script. Deletions can be found |
|                    |                        |if the ``text`` parameter is a |
|                    |                        |blank string (``""``).        |
+--------------------+------------------------+-------------------------------+
|``on_text_interact``|``index``, ``selection``|Text in the entry was somehow  |
|                    |                        |interacted by the user. This is|
|                    |                        |dispatched on text selection or|
|                    |                        |motion related to the caret.   |
|                    |                        |Deletions do not trigger this  |
|                    |                        |event or other text-related    |
|                    |                        |modifications.                 |
+--------------------+------------------------+-------------------------------+

Keyboard functionality
----------------------

Keyboard functionality is provided by futura.

.. warning::

    The ```tkinter`` <https://docs.python.org/3/library/tkinter.html>`_ library
    must be installed for any interaction with the clipboard. On default,
    ``tkinter`` is already pre-installed, but can be modified via installation
    settings or ```pip`` <https://pypi.org/project/pip/>`_.

* :kbd:`Control—C`\ 🖨️ for copying selected text
* :kbd:`Control—X`\ ✂️ for copying and then deleting selected text (cut)
* :kbd:`Control—V`\ 📋 for pasting selected text in the clipboard
* :kbd:`Control—A`\ ☑️ for selecting all text
* :kbd:`Alt—←`\     ⬅️ for moving the caret to the last position of mouse press
* :kbd:`Alt—→`\     ➡️ inverse of :kbd:`Alt-←`\

History management is an experimental feature and may be buggy or glitchy.

Below are the constants used for moving the caret and/or deleting text.

* :py:const:`~futura.key.MOTION_LEFT`
* :py:const:`~futura.key.MOTION_RIGHT`
* :py:const:`~futura.key.MOTION_UP`
* :py:const:`~futura.key.MOTION_DOWN`
* :py:const:`~futura.key.MOTION_NEXT_WORD`
* :py:const:`~futura.key.MOTION_PREVIOUS_WORD`
* :py:const:`~futura.key.MOTION_BEGINNING_OF_LINE`
* :py:const:`~futura.key.MOTION_END_OF_LINE`
* :py:const:`~futura.key.MOTION_NEXT_PAGE`
* :py:const:`~futura.key.MOTION_PREVIOUS_PAGE`
* :py:const:`~futura.key.MOTION_BEGINNING_OF_FILE`
* :py:const:`~futura.key.MOTION_END_OF_FILE`
* :py:const:`~futura.key.MOTION_BACKSPACE`
* :py:const:`~futura.key.MOTION_DELETE`
* :py:const:`~futura.key.MOTION_COPY`
* :py:const:`~futura.key.MOTION_PASTE`

These can dispatch :py:meth:`~futura.widgets.Entry.on_text_interact` events.
The :kbd:`Control`\ modifier may be held down on some of these keys, like
:py:const:`~futura.key.MOTION_BACKSPACE`, which will delete the previous word.

Mouse functionality
-------------------

🖱️ Mouse press can do a number of things.

* The caret's position is set to the nearest character relative to the mouse
  press.
* The history will add the caret's position.
* If text is selected, the selection will be removed.
* If the :kbd:`Shift`\ key is being held, a selection will be created between the
  current caret index and the closest character to the mouse.
* If two clicks are made within 0.5 seconds (double-click), the current word is
  selected.
* If three clicks are made within 0.5 seconds (triple-click), the current
  paragraph is selected.
* If there is a placeholder text, the text is removed.

Additionally, if the index is changed, then it is added to the history and the
:py:meth:`~futura.widgets.Entry.on_text_interact` event is dispatched.

Validation
----------

❌ Validation is minimally supported and is still an experimental feature.
The :py:class:`~futura.widgets.Entry` widget has a
:py:attr:`~futura.widgets.Entry.validate` property, which is a regular
expression pattern (made by ``re.compile()``). On text input, futura checks if
the validation is valid, then if it is valid, the text passes.

Validations are listed below::

    # (from re import compile)

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

An empty validation, such as ``None``, will have no effect.

Toggle
======

The :py:class:`~futura.widgets.Toggle` widget can switch between ``True`` or
``False`` values. It is similar to a checkbox, but there is a knob that slides
from the left to the right. If creating your own theme for this, make sure that
it is unambiguous.

A toggle theme may accidentally be ambiguous by having colored states for the
on-and-off state. The user may be stuck on whether left or right means on or
off. 

A toggle takes three parameters. ``default`` is the default value of the
toggle, ``padding`` is the space between the label and the bar, and
``callback`` is how the toggle is invoked. It is similar to a button callback.

The toggle has several properties. A few of those not mentioned are its text
properties. The :py:attr:`~futura.widgets.Toggle.on_left` property is ``True``
when the knob is on the left side of the toggle. There is an
:py:attr:`~futura.widgets.Toggle.on_right` property. It's not recommended to
change these. The :py:attr:`~futura.widgets.Toggle.switch` property determines
if the toggle should change values. Finally, the
:py:attr:`~futura.widgets.Toggle.value` property is the toggle's value (either
``True`` or ``False``).

+------------------------+----------+-----------------------------------------+
|Event                   |Parameters|Description                              |
+========================+==========+=========================================+
|:meth:`Toggle.on_toggle`|value     |The toggle has been completed. This means|
|                        |          |the knob has moved from one side of the  |
|                        |          |toggle to the other.                     |
+------------------------+----------+-----------------------------------------+

Slider
======

The :py:class:`~futura.widgets.Slider` widget can display a slidable bar. It is
used for numerical input. There is a knob, which can slide and move around,
responding to mouse press, drag, and keyboard input.

.. warning::

    There are currently some bugs with this. Please file a pull
    request if you want to help or contribute.

A slider has several parameters. It has ``color`` and ``font`` options for the
label but also has a ``default`` parameter, which is the default value of the
slider. Additionally, the ``size`` parameter modifies the number of values that
can be displayed on the slider, ``padding`` changes the spacing between the
label and the slider, and ``round`` is the number of decimal digits the label
display and value rounds to.

Sliders have a few properties. Of course, they have the label properties, but
they also have others. :py:attr:`~futura.widgets.Slider.destination` is the
destination point for the knob to glide to. This creates a glide effect.
:py:attr:`~futura.widgets.Slider.value` is the currently displayed value of the
slider.

Knob-related methods
--------------------

There are two methods used for changing the knob's value and position.

Knob velocity
`````````````

The method :py:meth:`~futura.widgets.Slider.update_knob` sets a velocity for
the knob to glide, and takes a ``x`` parameter to set the destination to.

Instead of directly moving the knob, the
:py:attr:`~futura.widgets.Slider._value` property is changed and the
:py:attr:`~futura.widgets.Slider.destination` is set.
The :py:meth:`~futura.widgets.Slider.on_slide_start` event can
be dispatched by this.

This formula below is used for determination and calculation of the value::

.. math::

    \text{abs}(((\text{slider.knob.x} - \text{slider.left}) \cdot
    \text{slider.size})
    \ (\text{slider.left} - \text{slider.right}))

It is also used for :py:meth:`~futura.widgets.Slider.reposition_knob`.

Knob coordinates
````````````````

The method :py:meth:`~futura.widgets.Slider.reposition_knob` is a little
different; it snaps the knob to the position, regardless of the destination.
It's used for the knob gliding internally.

The :py:meth:`~futura.widgets.Slider.on_slide_motion` event can be dispatched
by this method.

Knob movement
-------------

There are a few ways to move the knob:

* **Mouse press** - the knob snaps to the position relative to the mouse press
* **Mouse drag** - see above for details. The knob moves along with the mouse.
* **Keyboard** - pressing :kbd:`Left`\ or :kbd:`Right`\ will change the value
  by 1.
* **Program** - setting the value will cause the knob to glide to the adjacent
  position. This may use the :py:meth:`~futura.widgets.Slider.update_knob` or
  :py:meth:`~futura.widgets.Slider.reposition_knob` methods.

The knob increases its scale when hovered by a factor of
:py:const:`~futura.widgets.KNOB_HOVER_SCALE`.

.. CHANGELOG

    October 16 2022             Creation of basic tutorial
    October 17 2022             Code block and formatting fixes
    October 18 2022             Grammarly suggestions and slider and toggle

.. _python: http://www.python.org/
.. _arcade: https://arcade.academy/
.. _pyglet: https://pyglet.org/
.. _tkinter: https://docs.python.org/3/library/tkinter.html
