import os
import inspect
import configparser

from svst import constants

from typing import Optional, Dict, Union


def _get_caller_directory() -> Union[str, None]:
    """Get the project root directory."""
    frame: inspect.FrameInfo = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if module:
        filename: str = module.__file__
        return os.path.dirname(filename)
    return None


def _get_configuration_path() -> Optional[str]:
    """Get configuration file path."""

    root_directory: str = os.path.dirname(_get_caller_directory())
    if root_directory:
        file_name: str
        for file_name in constants.POSSIBLE_CONFIGURATION_FILES:
            file_path: str = os.path.join(root_directory, file_name)
            if os.path.exists(file_path):
                return file_path
    return None


def read_configuration() -> Optional[Dict[str, str]]:
    """Get configuration keys from file."""

    config_path: str = _get_configuration_path()

    if not config_path:
        return None

    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_path)

    return config["svst"] if "svst" in config else None
