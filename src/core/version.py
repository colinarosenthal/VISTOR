"""
VISTOR Version Information
"""

APP_NAME = "VISTOR"

APP_SUBTITLE = (
    "Vintage Interactive Television Operating Runtime"
)

VERSION = "0.6.0"


def get_application_title():

    if APP_SUBTITLE:

        return f"{APP_NAME} - {APP_SUBTITLE}"

    return APP_NAME


def get_version_string():

    return f"{get_application_title()} v{VERSION}"
