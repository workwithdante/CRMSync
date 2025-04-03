import logging

from rich.logging import RichHandler


def setup_logging():
    logger = logging.getLogger("company_sync")
    logger.setLevel(logging.INFO)

    # Evita duplicar handlers si ya existen
    if not logger.handlers:
        console_handler = RichHandler(rich_tracebacks=True)
        formatter = logging.Formatter("%(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Evita que se propague al logger raíz
    logger.propagate = False
    return logger
