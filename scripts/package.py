#!/usr/bin/env python3
"""Build or verify the deterministic flights plugin package."""

import argparse
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "plugin.json"
PACKAGE = ROOT / "flights.aimplugin"


def build_package() -> bytes:
    manifest = MANIFEST.read_bytes()
    json.loads(manifest)
    archive_bytes = io.BytesIO()
    info = ZipInfo("plugin.json", (1980, 1, 1, 0, 0, 0))
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    with ZipFile(archive_bytes, "w") as archive:
        archive.writestr(info, manifest)
    return archive_bytes.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the committed package")
    args = parser.parse_args()
    expected = build_package()
    if args.check:
        if not PACKAGE.is_file() or PACKAGE.read_bytes() != expected:
            parser.error(f"{PACKAGE.name} differs from plugin.json; rebuild it")
        with ZipFile(PACKAGE) as archive:
            if archive.namelist() != ["plugin.json"]:
                parser.error("package must contain only plugin.json")
        print(f"Package OK: {hashlib.sha256(expected).hexdigest()}")
    else:
        PACKAGE.write_bytes(expected)
        print(f"Built {PACKAGE.name}: {hashlib.sha256(expected).hexdigest()}")


if __name__ == "__main__":
    main()
