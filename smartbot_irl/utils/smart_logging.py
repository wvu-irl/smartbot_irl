import logging
import re
import time
from typing import Any
import sys
from colorama import init as colorama_init

colorama_init(strip=not sys.stdout.isatty())


class RegexRateLimitFilter(logging.Filter):
    """Rate limit specific log messages using regex to match similar base strings"""

    _FLOAT_RE = re.compile(r"-?\d+\.\d+")
    _INT_RE = re.compile(r"\b\d+\b")

    def __init__(self):
        super().__init__()
        self._last_emit: dict[str, float] = {}

    def _normalize(self, msg: str) -> str:
        msg = self._FLOAT_RE.sub("*", msg)
        msg = self._INT_RE.sub("*", msg)
        return msg

    def filter(self, record: logging.LogRecord) -> bool:
        rate = getattr(record, "_rate_limit_interval", 0.0)
        if rate <= 0.0:
            return True

        msg = record.getMessage()
        key = self._normalize(msg)
        now = time.time()
        last = self._last_emit.get(key, 0.0)
        if now - last < rate:
            return False
        self._last_emit[key] = now
        return True


class ColorFormatter(logging.Formatter):
    """Inject ANSI colors into log levelnames."""

    COLORS = {
        logging.DEBUG: "\033[36m",  # cyan
        logging.INFO: "\033[32m",  # green
        logging.WARNING: "\033[33m",  # yellow
        logging.ERROR: "\033[31m",  # red
        logging.CRITICAL: "\033[1;35m",  # bold magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


class SmartLogger:
    """Minimal logger with rate limiting and levels.

    :class:`SmartLogger` wraps the Python standard library's :mod:`logging`
        module. Rate limiting allows logging of high frequency code (e.g. sensor
        reads) at a fixed rate so as to avoid flooding your console.

    Args:
        name (str, optional):

        level (int, optional):
            Minimum threshold of log statements severity to print (Options are:
            :data:`logging.DEBUG`, :data:`logging.INFO`, :data:`logging.WARN`,
            :data:`logging.ERROR`, :data:`logging.FATAL`). Default level is
            :data:`logging.INFO`.

    Example::
        from smartbot_irl.utils.logging import SmartLogger import math

        log = SmartLogger("demo", level=logging.DEBUG)

        for i in range(10):
            # These will only print every ~2 seconds for identical patterns
            log.info(f"Robot at position {math.sin(i):.2f}", rate=2.0)
            log.debug(f"Loop iteration {i}", rate=1.0)

    See Also::
        * :class:`RegexRateLimitFilter` -- Log string matcher.
        * :mod:`logging`-- Pythons standard logging library.
    """

    def __init__(self, name: str = "smartbot", level: int = logging.INFO):
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:  # avoid duplicate handlers
            handler = logging.StreamHandler()
            fmt = "[%(asctime)s] %(levelname)s: %(message)s"
            handler.setFormatter(ColorFormatter(fmt))
            self._logger.addHandler(handler)
        self._logger.setLevel(level)
        self._logger.addFilter(RegexRateLimitFilter())

    def log(self, msg: Any, *, rate: float = 0.0, level: int = logging.INFO):
        try:
            msg_str = str(msg)
        except Exception:
            msg_str = f"<unprintable {type(msg).__name__}>"
        # just call logger.log() normally, passing rate info
        self._logger.log(level, msg_str, extra={"_rate_limit_interval": rate})

    # convenience
    def info(self, msg: Any, rate: float = 0.0):
        self.log(msg, rate=rate, level=logging.INFO)

    def debug(self, msg: Any, rate: float = 0.0):
        self.log(msg, rate=rate, level=logging.DEBUG)

    def warn(self, msg: Any, rate: float = 0.0):
        self.log(msg, rate=rate, level=logging.WARNING)

    def error(self, msg: Any, rate: float = 0.0):
        self.log(msg, rate=rate, level=logging.ERROR)
