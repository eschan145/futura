# Set up variables and filepaths

import getpass
import os

username = getpass.getuser() # Get username [DEPRECATED]

# Get directory paths
directory = __file__[:-7]

print("Directory: %s" % directory)

path = f"{directory}assets".replace("\\", "/")
theme = "futura"

# To be put into settings

blank1 = f"{path}/application/blank1.png"
blank2 = f"{path}/application/blank2.png"

widgets = {}
colors = ["blue", "green", "silver", "red", "yellow"]

for color in colors:
    widgets[f"{color}_button_normal"] = f"{path}/themes/{theme}/images/button/{color}_button_normal.png"
    widgets[f"{color}_button_hover"] = f"{path}/themes/{theme}/images/button/{color}_button_hover.png"
    widgets[f"{color}_button_press"] = f"{path}/themes/{theme}/images/button/{color}_button_press.png"
    widgets[f"{color}_button_disable"] = f"{path}/themes/{theme}/images/button/{color}_button_disable.png"
    widgets[f"{color}_button_square_normal"] = f"{path}/themes/{theme}/images/button/{color}_button_square_normal.png"
    widgets[f"{color}_button_square_hover"] = f"{path}/themes/{theme}/images/button/{color}_button_square_hover.png"
    widgets[f"{color}_button_square_press"] = f"{path}/themes/{theme}/images/button/{color}_button_square_press.png"

# TODO: add all of the filepaths into entry map, toggle map, etc.
entry_normal = f"{path}/themes/{theme}/images/entry/entry_normal.png"
entry_hover = f"{path}/themes/{theme}/images/entry/entry_hover.png"
entry_focus = f"{path}/themes/{theme}/images/entry/entry_focus.png"

toggle_true = f"{path}/themes/{theme}/images/toggle/toggle_true.png"
toggle_false = f"{path}/themes/{theme}/images/toggle/toggle_false.png"
toggle_true_hover = f"{path}/themes/{theme}/images/toggle/toggle_true_hover.png"
toggle_false_hover = f"{path}/themes/{theme}/images/toggle/toggle_false_hover.png"

slider_horizontal = f"{path}/themes/{theme}/images/slider/slider_horizontal.png"

# combobox_top_normal = f"{path}/{theme}/combobox_top_normal.png"
# combobox_top_hover = f"{path}/{theme}/combobox_top_hover.png"
# combobox_middle_normal = f"{path}/{theme}/combobox_middle_normal.png"
# combobox_middle_hover = f"{path}/{theme}/combobox_middle_hover.png"
# combobox_bottom_normal = f"{path}/{theme}/combobox_bottom_normal.png"
# combobox_bottom_hover = f"{path}/{theme}/combobox_bottom_hover.png"

knob = f"{path}/themes/{theme}/images/accessories/knob.png"

colorchooser = f"{path}/{theme}/images/colorchooser.png"


if not os.path.exists(path):
    raise FileNotFoundError(f"{path} does not exist. Try opening the folder " \
                            "of the program.")
