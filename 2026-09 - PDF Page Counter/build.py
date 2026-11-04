"""Build a single-file Python CLI archive and optionally a Windows GUI executable."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import zipapp
from pathlib import Path

import pypdf
from icon_art import render_icon


HERE = Path(__file__).resolve().parent
DIST = HERE / "dist"


def build_script() -> Path:
    DIST.mkdir(exist_ok=True)
    target = DIST / "document-page-counter.pyz"
    with tempfile.TemporaryDirectory() as temp:
        staging = Path(temp)
        for filename in ("cli.py", "counter.py"):
            shutil.copy2(HERE / filename, staging / filename)
        shutil.copytree(Path(pypdf.__file__).parent, staging / "pypdf", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        zipapp.create_archive(staging, target=target, main="cli:main", compressed=True)
    return target


def build_exe() -> Path:
    DIST.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        icon = Path(temp) / "document-page-counter.ico"
        render_icon().save(icon, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--windowed",
             "--name", "Document Page Counter", "--icon", str(icon), "--distpath", str(DIST),
             "--workpath", str(Path(temp) / "build"), "--specpath", temp, str(HERE / "gui.py")],
            check=True,
        )
    return DIST / "Document Page Counter.exe"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", action="store_true", help="Also build a Windows GUI EXE (requires PyInstaller)")
    arguments = parser.parse_args()
    print(f"Script archive: {build_script()}")
    if arguments.exe:
        print(f"Desktop app: {build_exe()}")