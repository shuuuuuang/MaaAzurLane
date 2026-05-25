from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    for path in sorted(root.glob("resource/pipeline/**/*.json")):
        with path.open("r", encoding="utf-8") as file:
            json.load(file)
        print(f"valid json: {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
