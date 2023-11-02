import logging

from loguru import logger

from models import LoggerCfg


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info,
        ).log(level, record.getMessage())


def init_logger(logger_cfg: LoggerCfg, disable_console_log: bool = False):
    if disable_console_log:
        logger.remove()

    if logger_cfg.enable:
        logger.add(
            sink=logger_cfg.path,
            level=logger_cfg.level,
            encoding=logger_cfg.encoding,
            enqueue=True,
            rotation=logger_cfg.rotation,
            retention=logger_cfg.retention,
            compression=logger_cfg.compression,
            format=logger_cfg.format_,
        )


def override_uvicorn_logger():
    for name in ("uvicorn", "uvicorn.access"):
        logging.getLogger(name).handlers = [InterceptHandler()]
