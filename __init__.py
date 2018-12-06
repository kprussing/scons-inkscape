# coding: utf-8
from __future__ import unicode_literals
__doc__="""SCons.Tool.Inkscape

Builders for converting vector graphics using Inkscape.  Specifically,
converting SVG to PDF, PDF + ``\LaTeX``, and PNG and PDF to PNG.

There normally shouldn't be any need to import this module directly.  It
will usually be imported through the generic SCons.Tool.Tool() selection
method.

"""

#
# Copyright (c) 2016-2018 Keith F. Prussing
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 

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


def _latex_emitter(target, source, env):
    """The emitter for PDF + LaTeX exporting
    """
    target.append(str(target[0]) + "_tex")
    return target, source

#
# Builders
# ~~~~~~~~
#

_builder = SCons.Builder.Builder(
        action=SCons.Action.Action("$INKSCAPECOM", "$INKSCAPECOMSTR"),
        single_source=True
    )

# _params = {
        # "inkscape" : {"flags" : [""],
                      # "src_suffix" : "",
                      # "suffix" : "",
                      # "emitter" : None},

        # "svg2pdf" : {"flags" : ["--export-pdf"],
                     # "src_suffix" : "svg",
                     # "suffix" : "pdf",
                     # "emitter" : None},

        # "svg2png" : {"flags" : ["--export-png"],
                     # "src_suffix" : "svg",
                     # "suffix" : "png",
                     # "emitter" : None},

        # "pdf2svg" : {"flags" : ["--export-plain-svg"],
                     # "src_suffix" : "pdf",
                     # "suffix" : "svg",
                     # "emitter" : None},

        # "svg2pdf_tex" : {"flags" : ["--export-pdf", "--export-tex"],
                         # "src_suffix" : "svg",
                         # "suffix" : "pdf",
                         # "emitter" : _latex_emitter}
    # }

# _builders = {}
# for key, val in _params.items():
    # _params[key]["COM"] = "$" + key.upper() + "COM"
    # _params[key]["COMSTR"] =  "$" + _params[key]["COM"] + "STR"
    # _params[key]["action"] = SCons.Action.Action(_params[key]["COM"],
                                                 # _params[key]["COMSTR"])
    # _builders[key] = SCons.Builder.Builder(action=_params[key]["action"],
                                           # **val)

#
# SCons functions
# ~~~~~~~~~~~~~~~
#

def generate(env):
    """Add the builders to the :class:`SCons.Environment.Environment`
    """
    env["INKSCAPE"] = _detect(env)
    command = " ".join(["$INKSCAPE",
                        "--without-gui",
                        "$INKSCAPEFLAGS",
                        "--file", "$SOURCE",
                        "$TARGET"])
    env.SetDefault(# Command line flags
                   INKSCAPEFLAGS=SCons.Util.CLVar("--without-gui"),

                   # Commands
                   INKSCAPECOM=command,
                   INKSCAPECOMSTR="",
        )
    # kwargs = {}
    # for key, val in _params.items():
        # kwargs[val["COM"]] = " ".join(["$INKSCAPE",
                                       # "$INKSCAPEFLAGS",
                                       # "--without-gui",
                                       # *val["flags"], 
                                       # "--file", "$SOURCE",
                                       # "$TARGET"])
        # kwargs[val["COMSTR"]] = ""

    # env.SetDefault(**kwargs)
    env["BUILDERS"]["Inkscape"] = _builder

def exists(env):
    return _detect(env)

