****
Text
****

Futura supports rich text and various text formatting options throughout its widgets, primarily the ``Label`` widget. There are two decoders provided; a ``HTMLDecoder`` that can decode a subset of HTML 4.0 transitional and a ``AttributedDecoder`` for a custom-made futura format with more features and preferred.

Formats
=======

Both formats are abstract and require a bit of usage and tutorials to learn them.

Futura
------

Futura's format is very easy to learn. It is very similar to _Markdown or _reStructuredText if you are familiar with those document formats.

Inline markup
`````````````

Inline markup is similar to Markdown. These should be inserted before and after the ranges.

* **\*Bold\*** text can be made by inserting asterisks (``*``)
* *\Italic\* text can be made by inserting backslashes (``\``)
* :u:_Underline_\ text can be made by inserting (``_``)
* :sup:Superscript\ text can be made by inserting (``^``) 
* :sub:Subscript\ text can be made by inserting (``__``)
* ``\``Code`\`` blocks can be made by inserting (``\```)



.. _reStructuredText: https://docutils.sourceforge.io/rst.html