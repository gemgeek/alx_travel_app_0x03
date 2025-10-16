#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# --- START OF FIX ---
# Forcefully add the project root directory to Python's search path.
# This solves the persistent ModuleNotFoundError for the 'listings' app.
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
# --- END OF FIX ---

def main():
    """Run administrative tasks."""
    # Make sure this line matches your settings folder name
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
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
    main()

