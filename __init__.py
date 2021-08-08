# MIT License
#
# Copyright 2016-2021 Keith F Prussing
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
__doc__="""SCons.Tool.Inkscape

Builders for converting vector graphics using Inkscape.  Specifically,
converting SVG to PDF, PDF + ``\LaTeX``, and PNG and PDF to PNG.

There normally shouldn't be any need to import this module directly.  It
will usually be imported through the generic SCons.Tool.Tool() selection
method.

"""

#
# Acknowledgements
# ----------------
#
# The format of this Tool is highly influenced by the JAL Tool on the
# ToolsForFools_ page from the SCons Wiki.
#
# .. ToolsForFools: https://github.com/SCons/scons/wiki/ToolsForFools
#

import SCons.Action
import SCons.Builder
import SCons.Errors
import SCons.Util
import SCons.Warnings

import itertools

#
# Preliminary details
# ~~~~~~~~~~~~~~~~~~~
#
# Begin by defining local errors

class ToolInkscapeWarning(SCons.Warnings.Warning):
    pass

class InkscapeNotFound(ToolInkscapeWarning):
    pass

SCons.Warnings.enableWarningClass(ToolInkscapeWarning)

# 
# Utility functions
# ~~~~~~~~~~~~~~~~~
#
def _detect(env):
    """Try to locate the Inkscape executable
    """
    try:
        # Check if we've already found it
        return env["INKSCAPE"]
    except KeyError:
        pass

    # Next try searching the Path.  This should work on *nix and nicely
    # configured Windows systems.
    inkscape = env.WhereIs("inkscape")
    if inkscape:
        return inkscape

    # That didn't work so we must be on Windows or Inkscape is not
    # installed.  As a last resort, we can try “known” installation
    # locations on Windows.  This assumes proper binary compatibility
    # and considers the user may be running under CygWin.
    import os
    prog = os.path.join("PROGRA~1", "Inkscape", "inkscape.com")
    for root in ("C:" + os.sep, os.path.join("/cygdrive", "c")):
        inkscape = env.WhereIs(os.path.join(root, prog))
        if inkscape:
            return inkscape

    # And the last ditch failed.  Time to just error out
    raise SCons.Errors.StopError(InkscapeNotFound,
                                 "Could not find Inkscape executable")


#
# Emitters
# ~~~~~~~~
#
def _latex_emitter(target, source, env):
    """Define a generic emitter for the LaTeX exporting"""
    target.append(str(target[0]) + "_tex")
    return target, source

#
# Builders
# ~~~~~~~~
#

# Many of the outputs have the same format with only source and target
# extensions changed.
_params = {}
_sources = ("svg", "pdf", "eps")
_targets = ("svg", "pdf", "eps", "ps", "png", "emf", "wmf")
for s, t in itertools.product(_sources, _targets):
    if s == t:
        continue

    plain = "plain-" if t == "svg" else ""
    _params[s + "2" + t] = {"out"       : "--export-" + plain + t,
                            "src_suffix": s,
                            "suffix"    : t,
                            "emitter"   : None}

    if t in ("pdf", "eps", "ps"):
        _params[s + "2" + t + "_tex"] = {
                "out"           : "--export-latex --export-" + t,
                "src_suffix"   : s,
                "suffix"       : t,
                "emitter"      : _latex_emitter
            }

_builders = {
        "Inkscape" : SCons.Builder.Builder(
                action=SCons.Action.Action("$INKSCAPECOM",
                                           "$INKSCAPECOMSTR"),
                single_source=True)
    }
for key, val in _params.items():
    com = key.upper() + "COM"
    comstr = com + "STR"
    flags = key.upper() + "FLAGS"
    action = SCons.Action.Action("$" + com, "$" + comstr)
    _params[key].update( dict(com=com, comstr=comstr,
                              action=action, flags=flags) )
    _builders[key] = SCons.Builder.Builder(single_source=True,
                                           **_params[key])

#
# SCons functions
# ~~~~~~~~~~~~~~~
#

def generate(env):
    """Add the builders to the :class:`SCons.Environment.Environment`
    """
    env["INKSCAPE"] = _detect(env)
    comroot = "$INKSCAPE $INKSCAPEFLAGS --file $SOURCE "
    kwargs = dict(# Generic command line flags
            INKSCAPEFLAGS=SCons.Util.CLVar("--without-gui"),

            # Generic command
            INKSCAPECOM="$INKSCAPE --file $SOURCE $INKSCAPEFLAGS $TARGET",
            INKSCAPECOMSTR=""
            )

    for key, val in _params.items():
        kwargs[val["flags"]] = ""
        kwargs[val["comstr"]] = ""
        kwargs[val["com"]] = " ".join([comroot, "$" + val["flags"],
                                       val["out"], "$TARGET"])

    env.SetDefault(**kwargs)
    env["BUILDERS"].update( _builders )

def exists(env):
    return _detect(env)

