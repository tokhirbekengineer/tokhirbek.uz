#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import shutil

def clear_pycache_dirs():
    """Loyihadagi barcha __pycache__ kataloglarini rekursiv o'chiradi."""
    project_root = os.path.dirname(os.path.abspath(__file__))  # manage.py joyi

    for root, dirs, files in os.walk(project_root):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(pycache_path)
                    print(f"✅ Removed: {pycache_path}")
                except Exception as e:
                    print(f"❌ Could not remove {pycache_path}: {e}")

def main():
    """Run administrative tasks."""
    clear_pycache_dirs()  # manage.py ishga tushganda pycache o'chiriladi

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
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
