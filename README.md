# FUTURA

Every game and application needs a high-end user interface that is easily customizable and versatile. Futura is designed to create such a user interface toolkit. As GUI toolkit and extension for the Python [`arcade`](https://api.arcade.academy/en/latest/) library, Futura can also be minimally modified for use with [`pyglet`](https://pyglet.org/), a OpenGL wrapper that Arcade is based on.

Futura comes with several widgets provided, including API to create your own. These built-in widgets include `Label`, `Button`, `Entry`, `Slider`, and `Toggle`. Each of these widgets have many features and can be adapted to most circumstances. All of these widgets are object-oriented, allowing customization after creation and methods.

Widgets are based off a `Widget` class, which manages events. At the basis are the `Label` and `Button` widgets. All of the other widgets are based off them, using the [`pyglet.text.layout.TextLayout`](https://pyglet.readthedocs.io/en/latest/modules/text/layout.html#pyglet.text.layout.TextLayout) and [`arcade.sprite.Sprite`](https://api.arcade.academy/en/latest/api/sprites.html#arcade-sprite) classes. More of these can be added as necessary. They may contain children widgets. For example, a `Combobox` widget may contain several `Pushable` widgets (more customizable buttons) and an `Entry` widget. This makes Futura both easy to use and very flexible.

Themes can be installed and moved into the `themes` folder. This can change the look of any provided widget. Custom-made widgets can also be customized with themes. Themes must follow a specific guideline, and must have a theme configuration file, which specifies the parameters of each widget's border. This is used to change the pixel size of a widget, in which a PIL algorithm is used to adjust the size without messing up the borders, or outline.

Futura only needs Arcade to function, though there are some extensions.

- [`shapely`](https://shapely.readthedocs.io/en/stable/manual.html) - optionally used for Cython speedups in calculating geometry and other geometry-related functions. If not installed, geometry-related functions will be a little slower.
- `tkinter` - user-interface library for handling clipboard interactions (<kbd>Cut</kbd>, <kbd>Copy</kbd>, <kbd>Paste</kbd>)

Rich text formatting is set in a subset of the HTML 5 (HyperText Markup Language) format for any widget's text or document. It has been slightly modified for additional features.

## Example

Here is a minimal demonstration showing some basic capabilities. It uses all of the built-in widgets, but does not show their full features. Look at the source code and documentation for all features.

  from futura.container import Container, set_container
  from futura.file import blank1, blank2
  from futura.key import ENTER
  from futura.management import Application
  from futura.widgets import Button, Entry, Label, Slider, Toggle

  from pyglet.app import run
  from pyglet.clock import get_frequency
  from pyglet.image import load


  class MyWindow(Window):
      """Minimal example showing the different types of interactive widgets and a
      quick demonstration of their look and feel.
      """

      def __init__(self, title, width, height):

          Window.__init__(
              self, width, height, title
          )

          self.set_icon(load(blank1), load(blank2))
          
          self.container = Container()

          set_container(self.container)

          self.label = Label(
              None,
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
              width=200,
              height=50,
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
              self.label.text = "<b>Bold</b>, <i>italic</i>, and <u>underline</u> text in <font color='red'>HTML</font>."

          self.slider.text = str(int(self.slider.value))


  if __name__ == "__main__":
      window = MyWindow(" ", 500, 400)

      run()

## Contact information

You can reach me in several ways.

|Method|Information|
|-|-|
|Discord|EthanC145#8543|
|Email|esamuelchan@gmail.com|
|Github|eschan145|
