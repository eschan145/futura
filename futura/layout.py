from futura.management import get_container

WINDOW_POPUP_SIMPLE = "window_popup_simple"


class Group:
    """A group of widgets to manipulate them and add graphical backgrounds
    like borders and popups.
    """

    def __init__(self, x=0, y=0, background=WINDOW_POPUP_SIMPLE):
        self.x = x
        self.y = y
        self.background = background

        self.image = None

        self.widgets = []

        get_container().groups.append(self)

    def add(self, widget):
        """Add a widget to the group. This can be done by passing a group
        parameter for any widget or calling this manually.
        """

        widget.x += self.x
        widget.y += self.y

    def draw(self):
        pass
