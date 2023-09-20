import re


from svst.config import read_configuration


config = read_configuration()


def is_ignored_file(root: str, file: str) -> bool:
    """Return if the file is ignored by the configuration.

    Args:
        root: Directory path string.
        file: Name of the file.

    Returns:
        Everything that is not a `.py` extension file is ignored.
        Checks if a path prefix, a directory or a file need to be ignored based on the configurations.
    """

    if not file.endswith(".py"):
        return True

    if not config:
        return False

    for prefix_path in (
        [item for item in config["ignore_path_prefix"].split("\n") if item]
        if "ignore_path_prefix" in config
        else []
    ):
        if root.replace("./", "", 1).startswith(prefix_path):
            return True

    for directory in (
        [item for item in config["ignore_directory"].split("\n") if item]
        if "ignore_directory" in config
        else []
    ):
        if directory in root:
            return True

    if (
        file in [item for item in config["ignored_file_names"].split("\n") if item]
        if "ignored_file_names" in config
        else []
    ):
        return True

    return False
