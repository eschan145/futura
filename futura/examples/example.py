from futura.application import Application
from futura.file import blank1, blank2
from futura.key import ENTER
# from futura.management import Application, set_container
from futura.widgets import Button, Entry, Label, Slider, Toggle

from pyglet.app import run
from pyglet.clock import get_frequency
from pyglet.image import load


class MyWindow(Application):
    """Minimal example showing the different types of interactive widgets and a
    quick demonstration of their look and feel.
    """

    def __init__(self, title, width, height):

        Application.__init__(
            self, width, height, title
        )

        # self.set_icon(load(blank1), load(blank2))
        
        self.label = Label(
            "<b>Bold</b>, <i>italic</i>, and underline text.",
            10,
            60,
            multiline=True,
            width=500)

        self._label = Label(
            None,
            10,
            80)

        self.button = Button(
            "Click me!",
            250,
            250,
            command=self.click,
            link="office.com")

        self.toggle = Toggle(
            "Show fps",
            250,
            350)

        self.slider = Slider(
            250,
            300,
            size=100)

        self.entry = Entry(
            300,
            160,
        )
            #["apple", "banana", "mango", "orange"])

        # self.circle = Star(
        #     100,
        #     150,
        #     30,
        #     1000,
        #     10000,
        #     color=BLUE_YONDER,
        #     opengl_error=False)

        self.container.add(self.label)
        self.container.add(self._label)
        self.container.add(self.button)
        self.container.add(self.toggle)
        self.container.add(self.slider)
        self.container.add(self.entry)
        
        self.button.bind(ENTER)

        self.background_color = (255, 255, 255, 50)

    def click(self):
        self._label.text = self.entry.text

    def on_draw(self):
        self.clear()
        self.set_caption(f"{int(get_frequency())} fps")

        self.container.draw()

        self.label.UPDATE_RATE = self.slider.value + 1  # Compensate for zero

        if self.toggle.value:
            self.label.text = f"{int(get_frequency())} fps"
        else:
            self.label.text = "<b>Bold</b>, <i>italic</i>, and underline text in <font color='red'>HTML</font>."

        self.slider.text = str(int(self.slider.value))


if __name__ == "__main__":
    window = MyWindow(" ", 500, 400)
    
    run()
    
    print(window.container.average_fps, max(window.container.fps_list))
