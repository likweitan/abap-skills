"""Open a .drawio file via fallback methods.

Order:
    1. macOS `open` command (uses default app for .drawio)
    2. xdg-open on Linux
    3. Print the diagrams.net base64 URL to stdout

The agent runtime should detect any draw.io MCP tool itself and call it directly;
this script is the last-resort opener that needs no MCP.
"""
from __future__ import annotations

import argparse
import base64
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path


def open_diagram(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(path)

    # Try OS opener
    opener = None
    system = platform.system()
    if system == "Darwin":
        opener = shutil.which("open")
    elif system == "Linux":
        opener = shutil.which("xdg-open")
    elif system == "Windows":
        opener = shutil.which("start")

    if opener:
        try:
            subprocess.run([opener, str(path)], check=False)
            return f"opened with {opener}"
        except Exception:
            pass

    # Fallback: print app.diagrams.net URL
    xml = path.read_text(encoding="utf-8")
    m = re.search(r"<mxGraphModel.*</mxGraphModel>", xml, re.DOTALL)
    inner = m.group() if m else xml
    b64 = base64.b64encode(inner.encode()).decode()
    url = f"https://app.diagrams.net/?pv=0&grid=0#create=data:text/xml;base64,{b64}"
    print(url)
    return f"printed app.diagrams.net URL ({len(url)} chars)"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("file", help="Path to .drawio file")
    args = p.parse_args()
    result = open_diagram(Path(args.file))
    print(f"# {result}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
