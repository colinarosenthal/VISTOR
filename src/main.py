"""
VISTOR
Application Entry Point
"""

from core.version import APP_NAME, APP_SUBTITLE, VERSION


def main():
    """Application entry point."""

    print("=" * 60)
    print(f"{APP_NAME} v{VERSION}")
    print(APP_SUBTITLE)
    print("=" * 60)
    print()

    print("Initializing...")
    print("Ready.")


if __name__ == "__main__":
    main()