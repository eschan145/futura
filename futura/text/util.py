"""Text utilities used by futura.

All functions are listed below::

:py:func:`~futura.text.add_prefix_and_suffix`

Adds a given prefix and suffix to the given text. Parameters are ``prefix``,
``suffix``, and ``text``. This is a convenience function instead of using
``join``.

:py:func:`~futura.text.insert`

Insert a string of text at a given position. This method was originally used
for the :py:class:`~futura.widgets.Entry` widget, but was deprecated in favor
of pyglet's native text inserting. 

It's been left as a convenience function.

:py:func:`~futura.text.delete`

Delete a string of text given a set of ranges. See the above documentation for
details.

:py:func:`~futura.text.convert_to_roman`

Convert an integer to a Roman numeral. This utility function is used for lsit
generation for the futura text format. There are limitations in this function;
for example the given integer must be between 0 and 4,000.

A ``custom`` parameter specifies a custom list of numerals to convert to, while
a ``number`` parameter specifies the inputed number to be converted to Roman.


**Exceptions**::

A :py:exc:`ValueError` may be invoked if the inputed number exceeds 4,000.
A :py:exc:`LookupError` may be raised if the custom list is invalid.

Credit to http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81611. 
"""

def add_prefix_and_suffix(text, prefix, suffix):
    """Add a prefix and suffix before and after text. Though this seems like
    overkill, it provides a quick way to do this. For example, adding
    ``" fps"`` right after a fps display's text.

    :Parameters:
        ``text`` : ``str``
            Text that will receive the modification of the prefix and suffix.
        ``prefix`` : ``str``
            Prefix to be added *before* the text.
        ``suffix`` : ``str``
            Suffix to be added *after* the text.

    :rtype: ``str``
    :returns: Text with the added prefix and suffix.
    """

    return prefix.join([text, suffix])

def insert(index, text, add):
    """Insert some text to a string given an index. This was originally used
    for the entry widget but was deprecated when we found a faster and more
    efficient way to insert text.
    """

    return text[:index] + add + text[index:]

def delete(start, end, text):
    """Delete some text to a string given an index. This was originally used
    for the entry widget but was deprecated when we found a faster and more
    efficient way to delete text.
    """

    if len(text) > end:
        text = text[:start] + text[end + 1::]
    return text

def convert_to_roman(number, custom=None):
    """Convert an integer to a Roman number, as in I, II, III, etc. Used for
    list generation in document text formatting.

    From http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81611.

    :Parameters:
        ``number`` : ``int`` or ``float``
            Number to be converted to Roman. Must be between ``0`` and
            ``3999`` unless a custom list is provided.
            
            There are two error catches::
            
            * *If the number is a string or float*, the string is attempted
              to be converted to an integer.
            * *If the number does not fit the requirements*, a helpful error
              message is raised.

        ``custom`` : ``list(integers, numerals)``
            Custom list format for Roman conversion. May be used for additional
            numbers. **This overrides the current list.**

    :rtype: ``int``
    :return: Converted Roman numeral.
    """

    if not 0 < number < 4000:
        raise ValueError("Number must be between 1 and 3999.")

    assert isinstance(custom, list), "The custom parameter must be a " \
                                     "two-dimensional list. See function " \
                                     "API docs for more information.\n\n"\
                                     "A %s was used instead." % type(custom)
     
    # Typically don't format like this, but it makes it neater and readable

    integers = (1000, 900,  500, 400, 100, 90,  50, 40,  10, 9,   5,  4,   1)
    numerals = ("M",  "CM", "D", "CD","C", "XC","L","XL","X","IX","V","IV","I")
    result = ""

    if custom:
        integers = custom[0] # Fixed a small bug. This used to be set to 1...
        numerals = custom[1]

    try:
        for i in range(len(integers)):
            count = int(int(number) // integers[i])
            result += numerals[i] * count
            number -= integers[i] * count
    
    except Exception as e:
        raise LookupError("Unable to decrypt custom list. Please check the "
                          "datatypes of each item in the list.\n\n"
                          "The full error stack is shown below:\n"
                          "%s" % e)
    return result
