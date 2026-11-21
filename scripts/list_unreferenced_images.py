"""List public/images files whose names do not appear in src files."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "public" / "images"
SOURCE = ROOT / "src"

source_text = "\n".join(
    path.read_text(encoding="utf-8", errors="ignore")
    for path in SOURCE.rglob("*")
    if path.is_file()
)

for image in sorted(path for path in IMAGES.rglob("*") if path.is_file()):
    if image.name not in source_text:
        print(image.relative_to(ROOT).as_posix())
