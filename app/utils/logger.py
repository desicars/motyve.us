import logging
from sys import stdout
from os import environ
from functools import wraps
from time import perf_counter
from typing import cast

from fastapi.requests import Request
from fastapi.responses import Response

# remove firebase/gRPC logs
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("google.cloud").setLevel(logging.ERROR)
logging.getLogger("google.auth").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("firebase_admin").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

environ["GRPC_VERBOSITY"] = "NONE"
environ["GRPC_LOG_SEVERITY_LEVEL"] = "ERROR"


class ShortNameFormatter(logging.Formatter):
    def __init__(
        self, fmt: str | None = None, datefmt: str | None = None, colorful: bool = True
    ) -> None:
        super().__init__(fmt, datefmt)
        self.colorful = colorful

    def format(self, record):
        if record.name == "desicars":
            record.display_name = ""
        elif self.colorful:
            record.display_name = f"[bold]{record.name.split('.')[-1]}:[/bold] "
        else:
            record.display_name = f"{record.name.split('.')[-1]}: "
        return super().format(record)


def setup_logging(level: str = "INFO", colorful: bool = False) -> logging.Logger:
    level = level.upper()

    base_logger = logging.getLogger("desicars")
    base_logger.propagate = False

    for h in list(base_logger.handlers):
        base_logger.removeHandler(h)

    if colorful:
        from rich.logging import RichHandler

        handler = RichHandler(rich_tracebacks=True, markup=True)
        formatter = ShortNameFormatter("%(display_name)s%(message)s")
    else:
        handler = logging.StreamHandler(stream=stdout)
        formatter = ShortNameFormatter(
            "%(asctime)s [%(levelname)s] %(display_name)s%(message)s",
            "%Y-%m-%d %H:%M:%S",
            False
        )

    handler.setFormatter(formatter)

    base_logger.setLevel(level)
    base_logger.addHandler(handler)

    firestore_logger = logging.getLogger("desicars.firestore")
    firestore_logger.setLevel(level)
    firestore_logger.propagate = True

    return base_logger


def format_request(request: Request, response: Response) -> str:
    if 200 <= response.status_code < 300:
        color = "green"
    elif 300 <= response.status_code < 400:
        color = "yellow"
    elif 400 <= response.status_code < 500:
        color = "red"
    else:
        color = "bold red"

    return f"{request.method} {request.url.path} -> [{color}]{response.status_code}"

def get_logger(name: str | None = None):
    """Get current logger and add support for timed_log decorator to it."""
    prefix = "desicars"
    return logging.getLogger(f"{prefix}.{name}" if name else prefix)
