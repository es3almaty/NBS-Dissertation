from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
required = [
    "Dockerfile",
    "render.yaml",
    "netlify.toml",
    "netlify/build.sh",
    ".github/workflows/test.yml",
    "app/main.py",
    "formatter_core_v0_2.py",
    "masters_dissertation_rules_v0.2.yaml",
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required deployment files:")
    for p in missing:
        print(" -", p)
    sys.exit(1)
print("Repository deployment structure OK")
