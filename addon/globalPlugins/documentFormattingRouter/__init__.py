"""
Document formatting requires specifying keyboard shortcuts for rarely toggled settings. instead, this addon gives an easy to use rotor as a keyboard layer.
"""

from collections import namedtuple
from enum import Enum, auto
from itertools import chain

import api
import config
import controlTypes
import core
import eventHandler
import globalPluginHandler
import globalVars
import ui
from core import callLater
from mathPres import MathInteractionNVDAObject as FakeUi
from scriptHandler import script

from .formattingRotor import FormattingRotor


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    @script(gesture='kb:nvda+g',
            # Translators: Script category for the document formatting rotor.
            category=_('Document Formatting Rotor'),
            # Translators: Documentation for the document formatting rotor's main script.
            description=_("Open the document formatting rotor"))
    def script_open_rotor(self, gesture):
        focus = api.getFocusObject()
        fakeUi = FormattingRotor(focus)
        fakeUi.setFocus()
        # Don't read the help again after first open.
        fakeUi.description = None
