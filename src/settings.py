from typing import Final

from src.i18n import I18n

_ = I18n().trans

TAG: Final[str] = "QuickMklink"
TAGCOPY: Final[str] = "QuickMklinkCopy"
TAGMOVE: Final[str] = "QuickMklinkMove"
VERSION: Final[str] = "0.12.1"
WATING_INTERVAL: Final[int] = 100
ABOUT_TEXT: Final[str] = _("""
QuickMklink is a tool that helps you create symbolic links quickly.
The software is open source software, please do not carry out secondary trafficking or commercial purposes

author: PythonImporter
""")
