"""
VISTOR

Application Entry Point
"""

from core.application import Application
from core.version import APP_NAME, APP_SUBTITLE, VERSION


def main():
    """Application entry point."""

    print("=" * 60)
    print(f"{APP_NAME} v{VERSION}")
    
    if APP_SUBTITLE:
        print(APP_SUBTITLE)
    print("=" * 60)
    print()

    app = Application()
    app.start()


if __name__ == "__main__":
    main()