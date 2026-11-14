"""Package skills/prove-it into a zip that can be uploaded to claude.ai (zip root is prove-it/)."""
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "prove-it")
DIST = os.path.join(ROOT, "dist")


def main():
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, "prove-it.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(SKILL):
            dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "evals")]
            for fn in filenames:
                if fn.endswith((".pyc",)):
                    continue
                full = os.path.join(dirpath, fn)
                arc = os.path.join("prove-it", os.path.relpath(full, SKILL))
                z.write(full, arc)
    print("Created", out)


if __name__ == "__main__":
    main()
