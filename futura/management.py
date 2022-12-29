"""Undocumented tools for management. This includes clipboard functionality and
border resizing, as well as a variety of other things.
"""

from tkinter import TclError, Tk

from arcade import Window
from PIL import Image

from futura.file import path
from futura.key import Keys, Mouse

container = None

clipboard = Tk()
clipboard.withdraw()

def set_container(_container):
    """Set the current container. This can be used for multiple views or
    windows. It just sets container to the given parameter.

    _container - main container to be used

    parameters: Container
    """
    
    global container

    container = _container

def get_container():
    """Get the current container.

    returns: Container
    """

    return container

def clipboard_get():
    """Get some text from the clipboard. This cathces exceptions if an image
    is copied in the clipboard instead of a string.

    _tkinter.TclError:
    CLIPBOARD selection doesn't exist or form "STRING" not defined

    returns: str
    """

    try:
        return clipboard.clipboard_get()

    except TclError:
        return

def clipboard_append(text):
    """Append some text to the clipboard.

    text - text to append to the clipboard

    parameters: str
    """

    clipboard.clipboard_append(text)


class Application(Window):
    
    def __init__(self, *args, **kwargs):
        Window.__init__(self, *args, **kwargs)
        
        self.mouse = Mouse()
        self.keys = Keys()
    
    def _get_title(self):
        """pyglet window title or caption. This is the text displayed on the
        toolbar. This is implemented because arcade only has functions to
        change the caption.
        
        type: property, str
        """
        
        return self.get_caption()
    
    def _set_title(self, title):
        self.set_caption(title)
    
    title = property(_get_title, _set_title)


def resize_bordered_image(image, size, width):
    """ 
    newSize = (new_width, new_height)
    borderWidths = (leftWidth, rightWidth, topWidth, bottomWidth)
    """
    
    if len(width) == 1:
        width = (width, width, width, width) # Something more neater
    
    sXr, sYr = size.x, size.y # ( 800, 120 ) # resized size X, Y
    lWx, rWx, tWy, bWy = width
    
    filepath = f"{path}/dump/widget.png"
    
    __image = image
    
    _image = image.image

    sX, sY  = _image.size
    sXi, sYi = sXr - (lWx + rWx), sYr - (tWy + bWy)

    pl_lft_top = _image.crop((0, 0, lWx, tWy)) 
    pl_rgt_top = _image.crop((sX - rWx, 0, sX, tWy))
    pl_lft_btm = _image.crop((0, sY-bWy, lWx, sY))
    pl_rgt_btm = _image.crop((sX - rWx, sY - bWy, sX, sY))

    pl_lft_lft = _image.crop((0, tWy, lWx, sY - bWy)).resize((lWx, sYi))
    pl_rgt_rgt = _image.crop((sX - rWx, tWy, sX, sY - bWy)).resize((rWx, sYi))
    pl_top_top = _image.crop((lWx, 0, sX - rWx, tWy)).resize((sXi, tWy))
    pl_btm_btm = _image.crop((lWx, sY - bWy, sX - rWx, sY)).resize((sXi, bWy))

    pl_mid_mid = _image.crop((lWx, tWy, sX - rWx, sY - bWy)).resize((sXi, sYi))

    image = Image.new(_image.mode, (sXr, sYr)) 

    image.paste(pl_mid_mid, (lWx, tWy))

    image.paste(pl_top_top, (lWx, 0))
    image.paste(pl_btm_btm, (lWx, sYr - bWy))
    image.paste(pl_lft_lft, (0, tWy))
    image.paste(pl_rgt_rgt, (sXr - rWx, tWy))

    image.paste(pl_lft_top, (0, 0))
    image.paste(pl_rgt_top, (sXr - rWx, 0))
    image.paste(pl_lft_btm, (0, sYr - bWy))
    image.paste(pl_rgt_btm, (sXr - rWx, sYr - bWy))

    filepath = f"{path}/dump/image.png"
    
    image.save(filepath)
    
    __image.image = image
    
def resize_bordered_images(widget, size, width):
    resize_bordered_image(widget.normal_image, size, width)
    resize_bordered_image(widget.hover_image, size, width)
    resize_bordered_image(widget.focus_image, size, width)
    
# from pyglet.window import Window
# from pyglet.text import HTMLLabel
# from pyglet.app import run

# class MyApplication(Window):
    
#     def __init__(self, *args, **kwargs):
#         Window.__init__(self, *args, **kwargs)
        
#         self.label = HTMLLabel("This is some <u>underlined</u> text.",
#                                None, self.width / 2, self.height / 2
#                               )
        
#     def on_draw(self):
#         self.label.draw()

# if __name__ == "__main__":
#     application = MyApplication()
    
#     run()
