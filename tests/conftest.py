import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PACKAGES_DIR = os.path.join(ROOT, "packages")
if os.path.isdir(PACKAGES_DIR):
    for entry in sorted(os.scandir(PACKAGES_DIR), key=lambda item: item.name):
        if entry.is_dir() and entry.path not in sys.path:
            sys.path.insert(0, entry.path)
