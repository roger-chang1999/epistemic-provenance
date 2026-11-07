"""把 skills/epistemic-provenance 打包成 claude.ai 可上傳的 zip（zip 根目錄為 epistemic-provenance/）。"""
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "epistemic-provenance")
DIST = os.path.join(ROOT, "dist")


def main():
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, "epistemic-provenance.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(SKILL):
            dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "evals")]
            for fn in filenames:
                if fn.endswith((".pyc",)):
                    continue
                full = os.path.join(dirpath, fn)
                arc = os.path.join("epistemic-provenance", os.path.relpath(full, SKILL))
                z.write(full, arc)
    print("已產生", out)


if __name__ == "__main__":
    main()
