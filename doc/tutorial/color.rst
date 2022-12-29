*************************
Color constants and tools
*************************

Futura has a color module, for use with colors and many helper functions.

The associated filename is :py:mod:`~futura.color`.

Color constants
===============

About 1,000 named colors are given as constants. These names are fairly easy to
find, like :py:const:`~futura.color.RED``,
:py:const:`~futura.color.SPANISH_CADET``, and many others, which are in RGB
values. You can view these colors in the API.

Color class and helper functions
================================

Several functions and a ``Color`` class are provided by futura.

Named colors
------------

A :py:class:`~futura.color.Color` class is a named color, with several properties
and aids in conversion. It can convert hexadecimal values to RGB, reverse, change
the opacity or alpha channel of a color, and supports simple dunder functions,
like :py:meth:`~futura.color.Color.__add__`,
:py:meth:`~futura.color.Color.__sub__`,
:py:meth:`~futura.color.Color.__getitem__`,
:py:meth:``~futura.color.Color.__setitem__`.

You can use or set the color by its :py:attr:`~futura.color.Color.rgb` and
:py:attr:`~futura.color.Color.hex` properties. It also provides several features
like scaling color brightness with :py:meth:`~futura.color.Color.scale`,
:py:meth:`~futura.color.Color.pale`, and :py:meth:`~futura.color.Color.solidify`.

.. warning:: Currently does not work with widgets or shapes.

Helper functions and color support
----------------------------------

Several helper functions are defined. These include
:py:func:`~futura.color.clamp`, :py:func:`~futura.color.four_byte`,
:py:func:`~futura.color.convert_to_hex`,
:py:func:`~futura.color.convert_to_rgb`,
:py:func:`~futura.color.change_format`, and
:py:func:`~futura.color.scale_color`.

:py:func:`~futura.color.change_format` toggles the value of a color by RGB to
hex, or back again. :py:func:`~futura.color.scale_color` scales the brightness
of a color by a given factor. If the factor is greater than 1, the color is
brightened, and if it is less than 1, the color is darkened.
