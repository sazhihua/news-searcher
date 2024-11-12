#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def printBanner():
    print("")
    print(
        """
        ______  ____  ______   _____________       _________
        ___   |/  / \/ /__  | / /__  ____/_ |     / /_  ___/
        __  /|_/ /__  /__   |/ /__  __/  __ | /| / /_____ \ 
        _  /  / / _  / _  /|  / _  /___  __ |/ |/ / ____/ / 
        /_/  /_/  /_/  /_/ |_/  /_____/  ____/|__/  /____/  
        """
    )
    print("")
    print("\tNews Searcher System is for learning purposes only.")
    print("\tIf you encounter problems during use, please contact me through the service account.")
    print("")
    print("\tv1.3 Powered By JackSa (email: sazhihua123@outlook.com)")
    print(
        """
----------------------------------------------------------------------------------------------------------------
        """
          )


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_searcher.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    printBanner()
    main()
