import os
import configparser

from svst import constants

from typing import Optional, Dict


def _get_configuration_path() -> Optional[str]:
    """Get configuration file path from working directory."""

    root_directory: str = os.getcwd()

    file_name: str
    for file_name in constants.POSSIBLE_CONFIGURATION_FILES:
        file_path: str = os.path.join(root_directory, file_name)
        if os.path.exists(file_path):
            return file_path
    else:
        return None


def read_configuration() -> Optional[Dict[str, str]]:
    """Get configuration keys from file.

    Returns:
        The configuration dictionary when a configuration file is available the config dict is returned.
    """

    config_path: str = _get_configuration_path()

    if not config_path:
        return None

    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_path)

    return config["svst"] if "svst" in config else None
