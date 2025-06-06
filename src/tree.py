#!/usr/bin/env python3
import os
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


def print_tree(start_path='.', prefix=''):
    clear_pycache_dirs()
    entries = sorted(os.listdir(start_path))
    entries_count = len(entries)

    for index, name in enumerate(entries):
        path = os.path.join(start_path, name)
        connector = '└── ' if index == entries_count - 1 else '├── '

        print(prefix + connector + name)

        if os.path.isdir(path):
            extension = '    ' if index == entries_count - 1 else '│   '
            print_tree(path, prefix + extension)

if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))  # tree.py joylashgan joy
    print(os.path.basename(root))
    print_tree(root)
