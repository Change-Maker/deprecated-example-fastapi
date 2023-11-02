import os

from loguru import logger
from pydantic import ValidationError

from models import Cfg


def get_config(config_path: str) -> Cfg | None:
    config_relpath = os.path.relpath(config_path)
    try:
        with open(config_relpath, "r") as f:
            return Cfg.model_validate_json(f.read())
    except ValidationError as validation_err:
        logger.error(
            f"The configuration '{config_relpath}' is invalid:"
            f" {validation_err}",
        )
    except Exception as err:
        logger.error(f"Failed to get configuration: {err}")
