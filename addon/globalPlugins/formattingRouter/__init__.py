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

from . import formattingRotorUtils
from .worldState import WorldState

ConfigValidationData = config.ConfigValidationData
FormattingItem = namedtuple('FormattingItem', ['name', 'configKey'])


class LastChangedState(Enum):
    ITEM = auto()
    CATEGORY = auto()
    SETTING = auto()


# There's no generic layeredKeystrokeNVDAObject, but math uses the technique, and we can piggyback.
class FormattingRotor(FakeUi):
    # We don't want NVDA calling this math, and there's no layered keystrokes AFAIK that we can use without reporting some role. Menuitem just has the nice sideaffect that name changes report and it feels native.
    role = controlTypes.role.Role.MENUITEM
    description = 'Press left/right to cycle through categories, then press up/down to select the formatting setting you want. Press space to cycle through the available settings. Press enter to save, or escape to cancel.'

    def _get_name(self):
        match self.lastChanged:
            case LastChangedState.ITEM:
                return self.getItem().name
            case LastChangedState.CATEGORY:
                return self.getCategory()
            case LastChangedState.SETTING:
                configKey = self.getItem().configKey
                return formattingRotorUtils.makeHumanReadableConfigValue(configKey, self.config[configKey])
    _cache_name = False

    ROTOR_CATEGORIES = [
        # Translators: This is a category in the document formatting rotor.
        _("Font"),
        # Translators: This is a category in the document formatting rotor.
        _("Document information"),
        # Translators: This is a category in the document formatting rotor.
        _("Pages and spacing"),
        # Translators: This is a category in the document formatting rotor.
        _("Table information"),
        # Translators: This is a category in the document formatting rotor.
        _("Elements"),
    ]

    ROTOR_ITEMS = [
        [
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Font name"),
                "reportFontName",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Font size"),
                "reportFontSize",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Font attributes"),
                "reportFontAttributes",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Superscripts and subscripts"),
                "reportSuperscriptsAndSubscripts",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Emphasis"),
                "reportEmphasis",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Highlighted (marked) text"),
                "reportHighlight",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Style"),
                "reportStyle",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Colors"),
                "reportColor",
            ),
        ],
        [
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Notes and comments"),
                "reportComments",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Bookmarks"),
                "reportBookmarks",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Editor revisions"),
                "reportRevisions",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Spelling errors"),
                "reportSpellingErrors",
            ),
        ],
        [
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Pages"),
                "reportPage",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Line numbers"),
                "reportLineNumber",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor. Options are Off, Speech, Tones, or Both.
                _("Line indentation reporting"),
                "reportLineIndentation",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Ignore blank lines for line indentation reporting"),
                "ignoreBlankLinesForRLI",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Paragraph indentation"),
                "reportParagraphIndentation",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Line spacing"),
                "reportLineSpacing",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Alignment"),
                "reportAlignment",
            ),
        ],
        [
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Tables"),
                "reportTables",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Headers"),
                "reportTableHeaders",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Cell coordinates"),
                "reportTableCellCoords",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Cell borders"),
                "reportCellBorders",
            ),
        ],
        [
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Headings"),
                "reportHeadings",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Links"),
                "reportLinks",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Graphics"),
                "reportGraphics",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Lists"),
                "reportLists",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Block quotes"),
                "reportBlockQuotes",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Groupings"),
                "reportGroupings",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Landmarks and regions"),
                "reportLandmarks",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Articles"),
                "reportArticles",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Frames"),
                "reportFrames",
            ),
            FormattingItem(
                # Translators: This is an item in the document formatting rotor.
                _("Clickable"),
                "reportClickable",
            ),
        ],
    ]

    buffer = []
    categoryIndex = 0
    lastChanged = LastChangedState.CATEGORY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deep copy the config object, so that we only write it explicitly.
        self.config = config.conf['documentFormatting'].copy()
        # This is not the most elegant way to do this, but other methods of doing it require patching getScript.
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            self.bindGesture(F'kb:{letter}', 'addToBuffer')
            self.bindGesture(F'kb:shift+{letter}', 'addToBuffer')

    def reportInitialFocus(self):
        api.getFocusObject().reportFocus()
        self.description = None

    def filterItems(self, fuzzyString):
        self.fuzzyItems = (item for item in chain.from_iterable(self.items) if self.buffer in item.name)

    def getItem(self):
        return self.ROTOR_ITEMS[self.categoryIndex][self.item]

    def getCategory(self):
        return self.ROTOR_CATEGORIES[self.categoryIndex]


    def reportChange(self):
        eventHandler.executeEvent("nameChange", self)

    @script(gesture="kb:upArrow")
    def script_previousItem(self, gesture):
        self.item = (self.item - 1 + len(self.ROTOR_ITEMS[self.categoryIndex])
                     ) % len(self.ROTOR_ITEMS[self.categoryIndex])
        self.lastChanged = LastChangedState.ITEM
        self.reportFocus()

    @script(gesture='kb:downArrow')
    def script_nextItem(self, gesture):
        self.item = (self.item + 1) % len(self.ROTOR_ITEMS[self.categoryIndex])
        self.lastChanged = LastChangedState.ITEM
        self.reportFocus()

    @script(gesture="kb:leftArrow")
    def script_previousCategory(self, gesture):
        self.categoryIndex = (
            self.categoryIndex - 1 + len(self.ROTOR_CATEGORIES)) % len(self.ROTOR_CATEGORIES)
        self.item = 0
        self.lastChanged = LastChangedState.CATEGORY
        self.reportFocus()

    @script(gesture="kb:rightArrow")
    def script_nextCategory(self, gesture):
        self.categoryIndex = (self.categoryIndex + 1) % len(self.ROTOR_CATEGORIES)
        self.item = 0
        self.lastChanged = LastChangedState.CATEGORY
        self.reportFocus()

    @script(gesture="kb:space")
    def script_cycleSetting(self, gesture):
        formattingItem = self.getItem()
        validateInfo = config.conf.getConfigValidation(
            ['documentFormatting', formattingItem.configKey])
        match validateInfo:
            case ConfigValidationData(validationFuncName='boolean'):
                self.config[formattingItem.configKey] = not self.config[formattingItem.configKey]
            case ConfigValidationData(validationFuncName='integer'):
                min, max = validateInfo.args
                cur = self.config[formattingItem.configKey]+1
                if cur > int(max):
                    cur = int(min)
                self.config[formattingItem.configKey] = cur
            case _:
                # There shouldn't be any str, or other funcs.
                pass
        self.lastChanged = LastChangedState.SETTING
        self.reportFocus()

    def script_addToBuffer(self, gesture):
        if not gesture.isCharacter:
            return
        key = gesture.mainKeyName
        self.buffer += key
        ui.message(key) # do not submit me

    @script(gesture="kb:enter")
    def script_save(self, other):
        config.conf['documentFormatting'] = self.config
        # Translators: Configuration saved for document formatting rotor.
        ui.message(_("Config saved"))
        eventHandler.executeEvent("gainFocus", self.parent)

    @script(gesture='kb:backspace')
    def script_remove(self, gesture):
        if not self.buffer:
            ui.message('nothing to delete')
            return
        ui.message('%s deleted' % self.buffer[-1])
        self.buffer = self.buffer[:-1]


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    @script(gesture='kb:nvda+g',
            # Translators: Script category for the document formatting rotor.
            category=_('Document Formatting Rotor'),
            # Translators: Documentation for the document formatting rotor's main script.
            description=_("Open the document formatting rotor"))
    def script_open_rotor(self, gesture):
        focus = api.getFocusObject()
        ui = FormattingRotor(focus)
        ui.setFocus()
        # Don't read the help again after first open.
        ui.description = None
