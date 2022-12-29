from html import entities
from html.parser import HTMLParser

from pyglet.image import load
from pyglet.text import DocumentLabel
from pyglet.text.formats.html import (_block_containers, _block_elements,
                                      _metadata_elements, _parse_color,
                                      _whitespace_re)
from pyglet.text.formats.structured import (ImageElement, OrderedListBuilder,
                                            StructuredTextDecoder,
                                            UnorderedListBuilder)


class HTMLDecoder(HTMLParser, StructuredTextDecoder):
    """A custom HTML decoder based off pyglet's built-in one. This has limited
    functionality but still feature-rich. It is possible to modify styling and
    tag names by overriding this.

    See :py:class:`~pyglet.text.formats.html.HTMLDecoder` for the provided
    pyglet HTML decoder.
    """

    default_style = {
        "font_name" : "Montserrat",
        "font_size" : 12,
        "margin_bottom" : "1pt",
        "bold" : False,
        "italic" : False,
    }

    font_sizes = {
        1 : 8,
        2 : 10,
        3 : 12,
        4 : 14,
        5 : 18,
        6 : 24,
        7 : 48
    }

    def decode_structured(self, text, location):
        """Decode some structured text and convert it to the pyglet attributed
        text with (MIME type ``vnd.pyglet-attributed``).

        :Parameters:
            ``text`` : ``str``
                Given HTML text to be decoded into pyglet attributed text
            ``location`` : ``str``
                Location of images and filepaths for the document
        """

        self.location = location
        self._font_size_stack = [3]
        self.list_stack.append(UnorderedListBuilder({}))
        self.strip_leading_space = True
        self.block_begin = True
        self.need_block_begin = False
        self.element_stack = ["_top_block"]
        self.in_metadata = False
        self.in_pre = False

        # Set default style

        self.push_style("_default", self.default_style)

        self.feed(text)
        self.close()

    def get_image(self, filename):
        return load(filename, file=self.location.open(filename))

    def prepare_for_data(self):
        if self.need_block_begin:
            self.add_text("\n")
            self.block_begin = True
            self.need_block_begin = False

    def handle_data(self, data):
        if self.in_metadata:
            return

        if self.in_pre:
            self.add_text(data)

        else:
            data = _whitespace_re.sub(" ", data)

            if data.strip():
                self.prepare_for_data()

                if self.block_begin or self.strip_leading_space:
                    data = data.lstrip()
                    self.block_begin = False
                self.add_text(data)

            self.strip_leading_space = data.endswith(" ")

    def handle_starttag(self, tag, case_attributes):
        """Handle the start of tags for all HTML elements. This creates a map
        of all the elements and pushes its style to a pyglet structured text
        decoder. They may be upper or lowercase. Note that you can use
        :py:func:`~futura.text.parse_distance` to calculate the pixel distance
        from standard units like inches, millimeters, etc.

        Pyglet and futura use a subset of HTML 4.01 transitional.

        TODO: make code blocks have a gray background, keyboard blocks with a
              glowing gray background

        The following elements are currently supported::

            ALIGN B BLOCKQUOTE BR CODE DD DIR DL EM FONT H1 H2 H3 H4 H5 H6 I
            IMG KBD LI MENU OL P PRE Q STRONG SUB SUP U UL VAR

        The mark (bullet or number) of a list item is separated from the body
        of the list item with a tab, as the pyglet document model does not
        allow out-of-stream text. This means lists display as expected, but
        behave a little oddly if edited. Multi-level lists are supported.

        No style or script elements are currently supported, and will never.

        A description of each tag is found below.

        ``ALIGN`` - alignment of the text. This can be
        :py:const:`~futura.LEFT`, :py:const:`~futura.CENTER`, or
        :py:const:`~futura.RIGHT`.

        ``B`` - **bold or heavy text**. This has no parameters and is defined
        in Markdown or reStructuredText as two asterisks (**). Alias of
        ``<strong>``.

        ``BLOCKQOUTE`` - a quote of some text. Later, a line drawn on the left
        side may be implemented. The left margin is indented by 60 pixels but
        can be changed by specifying a ``padding`` parameter. In Markdown, this
        is a greater than equal sign, with the level on the number of signs.

        ``BR`` - a line break. This draws a horizontal line below the text.

        ``CODE`` - a code block. This is displayed as backticks in Markdown,
        and indented in reStructuredText. This is an alias for ``<pre>``.

        ``DD`` - description, definition, or value for an item

        ``DIR`` - unordered list. This takes a ``type`` parameter, either
        :py:const:`~futura.CIRCLE` or :py:const:`~futura.SQUARE`. Defaults to
        a bullet point. Alias for ``<ul>`` and ``<menu>``.

        ``DL`` - description list. This just sets the bottom margin to nothing.

        ``EM`` - *italic or slanted text*. This has no parameters. Alias for
        ``<i>`` and ``<var>``.

        FONT - font and style of the text. It takes several parameters.
            ``family``       font family of the text. This must be a pyglet
                             loaded font.
            ``size``         size changes of the text. If negative the text
                             will shrink, and if positive the text will be
                             enlarged. If not specified the text size will
                             be 3.
            ``real_size``    actual font size of the text. This only accepts
                             positive values.
            ``color``        font color of the text in RGBA format

        ``H1`` - largest HTML heading. This sets the font size to 24 points.
        All headings except ``<h6>`` are bold.

        ``H2`` - second largest HTML heading. This sets the font size to 18
        points.

        ``H3`` - third largest HTML heading. This sets the font size to 16
        points.

        ``H4`` - fourth largest HTML heading. This sets the font size to 14
        points.

        ``H5`` - fifth largest HTML heading. This sets the font size to 12
        points.

        ``H6`` - a copy of ``<h5>``, but with *italic* instead of **bold** text

        ``I`` - *italic or slanted text*. This has no parameters. Alias for
        ``<em>`` and ``<var>``.

        ``IMG`` - display an image. This takes several parameters.
            ``filepath``    filepath of the image. This is not a loaded image.
            ``width``       width of the image. This must be set to a value
                            greater than 0, or the image will not be rendered.
            ``height``      height of the image. This must be set to a value
                            greater than 0, or the image will not be rendered.

        ``KBD`` - display keyboard shortcut

        ``LI`` - display a list item. This should be inserted in an ordered or
        unordered list, like this.

            <ul> My special list
                <li> My first list item </li>
                <li> My second list item </li>
            </ul>

        ``MENU`` - unordered list. This takes a ``type`` parameter, either
        :py:const:`~futura.CIRCLE` or :py:const:`~futura.SQUARE`. It defaults
        to a bullet point. Alias for ``<dir>`` and ``<ul>``.

        ``OL`` - ordered list
        
        Instead of having symbols, this uses sequential titles. Parameters and options are listed below::
        
            ``start``       start title of ordered list. (``int``)

            ``format``      list format. Pyglet's ordered list supports...

                            ``1``       Decimal Arabic ``(1, 2, 3)``
                            ``a``       Lowercase alphanumeric ``(a, b, c)``
                            ``A``       Uppercase alphanumeric ``(A, B, C)``
                            ``i``       Lowercase roman ``(i, ii, i)``
                            ``I``       Uppercase roman ``(I, II, III)``

            These values can contain prefixes and suffixes,
            like ``"1."``, ``"(1)"``, and so on. If the format is
            invalid a question mark will be used instead.

        See :py:class:`~pyglet.text.formats.structured.OrderedListBuilder`
        for details regarding text format.

        ``P`` - paragraph. This is different than just plain HTML text, as it
        will be formatted to the guidelines of a paragraph. This takes a align
        parameter, either :py:const:`~futura.LEFT`, :py:const:`~futura.CENTER`,
        or :py:const:`~futura.RIGHT`. Defaults to :py:const:`~futura.LEFT`.

        ``PRE`` - a preformatted code block. This is displayed as backticks in
        Markdown, and indented in reStructuredText. This is an alias for
        ``<code>``.

        ``Q`` - inline quotation element. This adds formal quotation marks
        around enclosed text. NOTE: not a regular quotation mark.

        ``STRONG`` - **bold or heavy text**. This has no parameters and is
        defined in Markdown or reStructuredText as two asterisks (**).  Alias
        of ``<b>``

        ``SUB`` - subscript text. Enclosed text is offset by points given in
        the ``baseline`` parameter. This has two parameters.
            ``size``        size decrement of the enclosed text. This is the
                            amount the text is leveled down.
            ``baseline``    offset of the enclosed text. This should be
                            negative. Defaults to -3 points.

        ``SUP`` - superscript text. Enclosed text is offset by points given in
        the ``baseline`` parameter. This has two parameters.
              ``size``      size increment of the enclosed text. This is the
                            amount the text is leveled up.

              ``baseline``  offset of the enclosed text. This should be
                            positive. Defaults to 3 points.

        ``U`` - :u:`underlined text`\. This can take an optional ``color``
        argument for the color of the underline. If not specified this defaults
        to :py:const:`~futura.color.BLACK`.

        ``UL`` - unordered list. This takes a ``type`` parameter, either
        :py:const:`~futura.CIRCLE` or :py:const:`~futura.SQUARE`. It defaults
        to a bullet point. Alias for ``<dir>`` and ``<menu>``.

        ``VAR`` - *italic or slanted text*. This has no parameters. Alias for
        ``<i>`` and ``<em>``.
        """

        if self.in_metadata:
            return

        element = tag.lower()
        attributes = {}

        for key, value in case_attributes:
            attributes[key.lower()] = value

        if element in _metadata_elements:
            self.in_metadata = True

        elif element in _block_elements:
            # Pop off elements until we get to a block container

            while self.element_stack[-1] not in _block_containers:
                self.handle_endtag(self.element_stack[-1])

            if not self.block_begin:
                self.add_text("\n")

                self.block_begin = True
                self.need_block_begin = False

        self.element_stack.append(element)

        style = {}

        if element in ("b", "strong"):
            style["bold"] = True

        elif element in ("i", "em", "var"):
            style["italic"] = True

        elif element in ("tt", "code", "kbd"):
            color = self.current_style.get("color")

            if color is None:
                color = attributes.get("background_color") or \
                    (246, 246, 246, 255)

            style["font_name"] = "Courier New"
            style["background_color"] = color

        elif element == "u":
            color = self.current_style.get("color")

            if color is None:
                color = attributes.get("color") or [0, 0, 0, 255]

            style["underline"] = color

        elif element == "font":
            if "family" in attributes:
                style["font_name"] = attributes["family"].split(",")

            if "size" in attributes:
                size = attributes["size"]

                try:
                    if size.startswith("+"):
                        size = self._font_size_stack[-1] + int(size[1:])

                    elif size.startswith("-"):
                        size = self._font_size_stack[-1] - int(size[1:])

                    else:
                        size = int(size)

                except ValueError:
                    size = 3

                self._font_size_stack.append(size)

                if size in self.font_sizes:
                    style["font_size"] = self.font_sizes.get(size, 3)

            elif "real_size" in attributes:
                size = int(attributes["real_size"])

                self._font_size_stack.append(size)
                style["font_size"] = size

            else:
                self._font_size_stack.append(self._font_size_stack[-1])

            if "color" in attributes:
                try:
                    style["color"] = _parse_color(attributes["color"])

                except ValueError:
                    pass

        elif element == "sup":
            size = self._font_size_stack[-1] - (attributes.get("size") or 1)

            style["font_size"] = self.font_sizes.get(size, 1)
            style["baseline"] = attributes.get("baseline") or "3pt"

        elif element == "sub":
            size = self._font_size_stack[-1] - (attributes.get("size") or 1)

            style["font_size"] = self.font_sizes.get(size, 1)
            style["baseline"] = attributes.get("baseline") or "-3pt"

        elif element == "h1":
            style["font_size"] = 24
            style["bold"] = True

        elif element == "h2":
            style["font_size"] = 18
            style["bold"] = True

        elif element == "h3":
            style["font_size"] = 16
            style["bold"] = True

        elif element == "h4":
            style["font_size"] = 14
            style["bold"] = True

        elif element == "h5":
            style["font_size"] = 12
            style["bold"] = True

        elif element == "h6":
            style["font_size"] = 12
            style["italic"] = True

        elif element == "br":
            self.add_text(u"\u2028")

            self.strip_leading_space = True

        elif element == "p":
            if attributes.get("align") in ("left", "center", "right"):
                style["align"] = attributes["align"]

        elif element == "align":
            style["align"] = attributes.get("type")

        elif element == "pre":
            style["font_name"] = "Courier New"
            style["margin_bottom"] = 0

            self.in_pre = True

        elif element == "blockquote":
            padding = attributes.get("padding") or 60

            left_margin = self.current_style.get("margin_left") or 0
            right_margin = self.current_style.get("margin_right") or 0

            style["margin_left"] = left_margin + padding
            style["margin_right"] = right_margin + padding

        elif element == "q":
            self.handle_data(u"\u201c")

        elif element == "ol":
            try:
                start = int(attributes.get("start", 1))
            except ValueError:
                start = 1

            format = attributes.get("format", "1.")

            builder = OrderedListBuilder(start, format)

            builder.begin(self, style)
            self.list_stack.append(builder)

        elif element in ("ul", "dir", "menu"):
            type = attributes.get("type", "circle").lower()
            detail = attributes.get("detail")

            if detail and not type:
                raise TypeError("If a detail is specified, then a type must " \
                                "also be specified. Built-in styles include " \
                                "circles, squares, arrows, and checkboxes."
                                )

            elif type == "square":
                mark = u"\u25a1" # □
            else:
                if type:
                    mark = type
                else:
                    mark = u"\u25cf"

            if detail:
                if type == "circle":
                    if detail == "empty":
                        mark = u"\u25CB" # ○
                    elif detail == "filled":
                        mark = u"\u25CF" # • # ●‿●
                if type == "arrow":
                    if detail == "black-white":
                        mark = u"\u27A3" # ➢
                    elif detail == "white-black":
                        mark = u"\u27A2" # ➣
                elif type == "checkbox":
                    if detail == "check":
                        # Might not work on some platforms and fonts
                        mark = u"\u2611" # ☑
                    elif detail == "cross":
                        mark = u"\u2612" # ☒

            else:
                if type == "arrow":
                    mark = u"\u27A4" # ➤
                elif type == "checkbox":
                    mark = u"\u2610" # ☐
                elif type == "circle":
                    mark = u"\u25CF"
                elif type == "dash":
                    mark = u"\u2014"

            builder = UnorderedListBuilder(mark)

            builder.begin(self, style)
            self.list_stack.append(builder)

        elif element == "li":
            self.list_stack[-1].item(self, style)
            self.strip_leading_space = True

        elif element == "dl":
            style["margin_bottom"] = 0

        elif element == "dd":
            left_margin = self.current_style.get("margin_left") or 0
            style["margin_left"] = left_margin + 30

        elif element == "img":
            image = self.get_image(attributes.get("filepath"))

            if image:
                width = attributes.get("width")

                if width:
                    width = int(width)

                height = attributes.get("height")

                if height:
                    height = int(height)

                self.prepare_for_data()

                self.add_element(ImageElement(image, width, height))
                self.strip_leading_space = False

        self.push_style(element, style)

    def handle_endtag(self, tag):
        """Handle the end tags for the HTML document. They may be upper or
        lowercase. This function makes sure that tags are processed correctly.

        The string's ``lower()`` function is used.
        """

        element = tag.lower()

        if element not in self.element_stack:
            return

        self.pop_style(element)

        while self.element_stack.pop() != element:
            pass

        if element in _metadata_elements:
            self.in_metadata = False
        elif element in _block_elements:
            self.block_begin = False
            self.need_block_begin = True

        if element == "font" and len(self._font_size_stack) > 1:
            self._font_size_stack.pop()
        elif element == "pre":
            self.in_pre = False
        elif element == "q":
            self.handle_data(u"\u201d")
        elif element in ("ul", "ol"):
            if len(self.list_stack) > 1:
                self.list_stack.pop()

    def handle_entityref(self, name):
        """Handle entity references from the HTML document.
        """

        if name in entities.name2codepoint:
            self.handle_data(chr(entities.name2codepoint[name]))

    def handle_charref(self, name):
        name = name.lower()

        try:
            if name.startswith("x"):
                self.handle_data(chr(int(name[1:], 16)))
            else:
                self.handle_data(chr(int(name)))

        except ValueError:
            pass


class HTMLLabel(DocumentLabel):

    def __init__(self, text="", location=None,
                 x=0, y=0, width=None, height=None,
                 anchor_x='left', anchor_y='baseline',
                 multiline=False, batch=None):

        self._text = text
        self._location = location

        document = HTMLDecoder().decode(text, location)

        DocumentLabel.__init__(self, document, x, y, width, height,
                               anchor_x, anchor_y, multiline, None,
                               batch, None)

    def _get_text(self):
        return self._text

    def _set_text(self, text):
        if text == self._text:
            return

        self._text = text

        self.document = HTMLDecoder().decode(text)

    text = property(_get_text, _set_text)
