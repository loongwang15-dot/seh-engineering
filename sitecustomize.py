import os
import sys


def _register_package_paths() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    packages_dir = os.path.join(root, "packages")
    if not os.path.isdir(packages_dir):
        return
    for entry in sorted(os.scandir(packages_dir), key=lambda item: item.name):
        if entry.is_dir() and entry.path not in sys.path:
            sys.path.insert(0, entry.path)


_register_package_paths()
