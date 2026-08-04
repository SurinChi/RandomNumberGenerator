"""
utils
======================
A utilities library, which includes logger, generator, validator, convertor, and timer.
It also have a Setting module customised for this app.

:copyright: (c) 2026 by SurinChi.
:license: GPLv3 for non-commercial project.
"""

from .logger import logger
from .generator import Generator
from .validator import Validator, CountZeroError, CountFloatError, InputValueError, ValueRangeException
from .convertor import Convertor
from .config import config
from .timer import Timer
from .history_manager import HistoryManager

__Author__ = "SurinChi"

__name__ = "utils"

__package__ = "utils"