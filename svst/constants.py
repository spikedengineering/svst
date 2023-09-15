STANDARD_LOGGING_LEVEL = "DEBUG"

IGNORED_FILE_NAMES = [
    "models.py",
    "admin.py",
    "tests.py",
    "serializers.py",
    "api_response.py",
    "send_slack_daily_message.py",
    "checks.py",
    "constants.py",
]

IGNORED_PATH_STARTS_WITH = [".local/lib/", ".mypy_cache/", "venv", ",venv"]

IGNORED_INSIDE_DIRECTORY = ["migrations"]
