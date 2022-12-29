# GUI images and themes

In this folder are images for the gui module. Images for all types of widgets
are supported. You can add themes to this directory, by moving their folder here.

Built-in themes include:

1. Futura

More themes are going to be added in the near future. Be sure that not all
themes are compatible. See filenames and included files in the built-in themes
for creating your own.

For adding customized images made by an external application that are vector
(where images are saved as shapes and text), you may create a folder called
`custom`. Vector graphics are the best, because it allows easy modification of
shapes after you select another.

## Graphics guidelines

Graphics and images must have a transparent background. Not having them will
prevent overlapping widgets. Additionally, if the background color is changed,
the widget will be visible with a white background.

It is customary to make the images pleasing to the eye. Here are some tips:

1. Rounded corners - this makes the image look comfy and soft. All widgets
should have them.
2. Color theme - most images shouldn't be too flashy or have too many colors.
They also shouldn't be too bright. All widgets must fall into a color theme.
A theme should have a color palette - a selection of various colors. You can
add more colors to widgets in parameters (not supported by all). Custom colors
will work, as long as they are consistent.
3. Consistency - this is very important. If there are three different button
images, their states should have the same color, border radius, gradient,
border thickness, etc.

## Directory structure

All custom themes should have a certain directory structure for it to be able
to be detected.