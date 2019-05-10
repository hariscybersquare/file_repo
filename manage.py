#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from scanfiles.uploadfilemetadata import scanfiles
import threading


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_repo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    thread1 = threading.Thread(target = scanfiles)
    if(thread1.is_alive() is False):
        thread1.start()
    execute_from_command_line(sys.argv)



if __name__ == '__main__':
    main()
