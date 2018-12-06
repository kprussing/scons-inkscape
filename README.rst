SCons tool for using Inkscape to convert images
===============================================

A common occurrence when writing is needing to convert an image format
to include in your document.  You will spend valuable (and important)
time adjusting your plot with ``pgfplots`` for ``\LaTeX`` only to
discover that the journal expects a Word document.  Alternatively, you
realize that you want to use an particular vector graphic from a journal
article you submitted in a conference presentation requiring PowerPoint.
One way to handle these situations is to simply regenerate the image in
an appropriate format.  However, that is a very manual and time
consuming process and does not sound like fun.  If your image is a high
quality SVG hand crafted in a drawing tool, you could easily reduce the
quality of the image by exporting the wrong format or lose your high
quality professional fonts.

You, on the other hand, are enlightened enough to use a `build tool`_ to
automate away most of this tediousness (otherwise you would not be
here).  This is a :class:`SCons.Tool` for teaching SCons_ how to use
Inkscape_ to convert vector images between formats.  The native format
of Inkscape is SVG, but it is also able to easily export PDF, PDF plus
the boiler plate ``\LaTeX`` for directly including in a ``\LaTeX``
document, or even an PNG for inclusion into Word or PowerPoint document.
(The inclusion of the last two formats is to facilitate working with
Pandoc_ and the `associated tool`_)

.. _SCons: https://scons.org
.. _build tool: SCons_
.. _Inkscape: https://inkscape.org
.. _Pandoc: https://pandoc.org
.. _associated tool: https://github.com/kprussing/scons-pandoc

Installation
------------

The tool follows the convention described in the ToolsIndex_.  Simply
clone this repository into your ``site_scons/site_tools`` directory
under the name ``inkscape``.  Then add::

   env = Environment(tools=["inkscape"])

to your ``SConstruct`` and you are ready to go.  Alternatively, you
could just copy the ``__init__.py`` to you tools directory, but why
would you want to do that?

.. _ToolsIndex: https://github.com/SCons/scons/wiki/ToolsIndex

Usage
-----

This tool provides the ``Inkscape`` builder.  Further, it provides
convenience builders for common conversions:

-  ``svg2pdf``
-  ``svg2pdf_tex``
-  ``svg2png``
-  ``pdf2svg``

.. todo:: Describe the environment variables that control the builders.

