"""Remove the score bar and complete partial weeks with empty decorative cells."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def style_snake(path: Path) -> tuple[int, int]:
    tree = ET.parse(path)
    root = tree.getroot()
    cells = [
        node
        for node in root.iter(f"{{{SVG}}}rect")
        if "c" in node.get("class", "").split()
    ]
    rows = sorted({node.attrib["y"] for node in cells}, key=float)
    columns = sorted({node.attrib["x"] for node in cells}, key=float)
    if len(rows) != 7 or not columns:
        raise ValueError("Expected a seven-row contribution grid")

    removed = 0
    for parent in root.iter():
        for node in list(parent):
            if "u" in node.get("class", "").split():
                parent.remove(node)
                removed += 1

    occupied = {(node.attrib["x"], node.attrib["y"]) for node in cells}
    # Insert behind the real cells and snake; padding never represents activity.
    added = 0
    for x in columns:
        for y in rows:
            if (x, y) not in occupied:
                attributes = {
                    **cells[0].attrib,
                    "class": "c",
                    "x": x,
                    "y": y,
                    "data-placeholder": "true",
                }
                root.insert(0, ET.Element(f"{{{SVG}}}rect", attributes))
                added += 1
    tree.write(path, encoding="unicode")
    return removed, added


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", type=Path, nargs="+")
    args = parser.parse_args()
    for path in args.files:
        removed, added = style_snake(path)
        print(f"{path}: removed {removed} score segments, added {added} empty cells")


if __name__ == "__main__":
    main()
