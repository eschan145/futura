"""Experimental widgets not yet finished."""

from pyglet.event import EventDispatcher
from widgets import Entry, Pushable, Widget


class Listbox(Widget):
    """Listbox widget to display a list of values, enable selecting them, and
    modifing and setting selections of values.
    """

    _options = []

    class Option:
        """Object-oriented approach to listbox items.
        """

        selected = False
        listbox = None

        def __init__(self, text, width=170, height=25):
            """Create an option.

            text - text to be displayed on the listbox
            width - width of the option
            height - height of the option

            parameters: str, int, int
            """

            self.text = text
            self.width = width
            self.height = height

    def __init__(self, x, y):
        """Create a listbox widget.

        Apparently, labels are removed as soon as a user event is triggered.
        The same goes with shapes. Adding them to a list avoids this problem.

        options - list of values that should be rendered in the listbox
        x - x position of the listbox
        y - y position of the listbox
        """

        Widget.__init__(self)

        self.x = x
        self.y = y
    
    def _get_options(self):
        """Get the values and options of the listbox.

        returns: list of Options
        """

        return self._options

    def _set_options(self, options):
        """Set the values and options of the listbox. This is a list of the
        object-oriented options, not strings containing their text.

        options - list of values and options

        parameters: list of Options
        """

        from shapes import Rectangle
        
        self._options = options

        self.shapes_ = []

        for option in options:
            option.listbox = self

        for i in range(len(options)):
            y = self.y - i * options[i].height

            label = Label(options[i].text, self.x + 5, y + options[i].height / 2)
            rectangle = Rectangle(self.x, y, options[i].width, options[i].height)
            
            self.shapes_.append(rectangle)
            self.shapes_.append(label)
        
    options = property(_get_options, _set_options)

    def draw(self):
        from shapes import Rectangle
        
        for shape in self.shapes_:
            if shape.hover and isinstance(shape, Rectangle):
                shape.colors[1] = BLUE

# class Combobox(Widget, EventDispatcher):

#     _display = []
#     _view = None
#     displayed = False
#     last_text = None
#     scroller = None

#     def __init__(self, x, y, options, color="yellow", default=0):

#         self.entry = Entry(x, y)
#         self.button = Pushable(None, x, y, self.reset_display,
#                                images=(widgets[f"{color}_button_square_normal"],
#                                        widgets[f"{color}_button_square_hover"],
#                                        widgets[f"{color}_button_square_press"])
#                                )
#         self.button.image.scale = 0.5

#         self.buttons = []

#         Widget.__init__(self)

#         self.x = x
#         self.y = y
#         self.options = options
#         self.display = options


#     def _get_text(self):
#         return self.entry.text

#     def _set_text(self, text):
#         self.entry.text = text

#     def _get_x(self):
#         """Get the x position of the Combobox.

#         returns: int
#         """

#         return self.entry.x

#     def _set_x(self, x):
#         """Set the x position of the Combobox.

#         x - new x position of the Combobox

#         parameters: int
#         """

#         self.entry.x = x

#     def _get_y(self):
#         """Get the y position of the Combobox.

#         returns: int
#         """

#         return self.entry.y

#     def _set_y(self, y):
#         """Set the y position of the Combobox.

#         y - new y position of the Combobox

#         parameters: int
#         """

#         self.entry.y = y

#     def _get_view(self):
#         """Get the vertical view of the Combobox.

#         returns: int
#         """

#         return self._view

#     def _set_view(self, view):
#         """Set the vertical view of the Combobox.

#         view - vertical view of the Combobox

#         parameters: int
#         """

#         self._view = view
#         self.display = self.display[view : view + 3]

#     x = property(_get_x, _set_x)
#     y = property(_get_y, _set_y)
#     view = property(_get_view, _set_view)

#     def _get_display(self):
#         return self._display

#     def _set_display(self, display):
#         self.buttons.clear()

#         identifier = 1

#         for option in display:
#             identifier += 1

#             if identifier == 2: image = (combobox_top_normal, combobox_top_normal)
#             elif identifier == len(display) + 1: image = (combobox_bottom_normal, combobox_bottom_normal)
#             else: image = (combobox_middle_normal, combobox_middle_normal)

#             button = Pushable(
#                       option, 0,
#                       Y,
#                       images=image,
#                       command=self.switch,
#                       parameters=identifier
#                       )

#             button.y = (self.x - 70) - 24 * identifier

#             self.buttons.append(button)

#     text = property(_get_text, _set_text)
#     display = property(_get_display, _set_display)

#     def switch(self, identifier):
#         if len(self.buttons) > 1:
#             self.text = self.buttons[identifier - 2].text
#         elif len(self.buttons) == 1:
#             self.text = self.buttons[0].text

#     def reset_display(self):
#         self.display = self.options

#     def draw(self):
#         self.button.x = self.right - 16

#         for button in self.buttons:
#             button.image.left = self.left
#             button.label.x = self.left + 10

#         self.component = self.entry

#         if not self.displayed:
#             self.display = self.options[:3]
#             self.displayed = True

#         if self.last_text is not self.entry.text and \
#             self.entry.text:

#             if self.entry.text == "" and \
#                 self.display is not self.options:
#                 self.display = self.options[:3]
#                 return

#             self.display = []
#             self.increment = (0, 0)
#             # If filter removed show all data

#             filtered_data = list()
#             for item in self.options:
#                 if self.entry.text in item:
#                     filtered_data.append(item)

#             self.display = filtered_data[:3]
#             self.last_text = self.entry.text