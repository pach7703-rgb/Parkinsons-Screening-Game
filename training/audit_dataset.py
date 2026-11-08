"""
Read-only dataset audit for Parkinsons_project.
Save this file in the project's training/ folder.
Run from the project root: python training/audit_dataset.py
"""
from pathlib import Path
from collections import Counter, defaultdict
import hashlib

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "datasets"
TASKS = ("spiral", "wave")
SPLITS = ("training", "testing")
CLASSES = ("healthy", "parkinsons")
EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    report = [
        "PARKINSON'S SCREENING PROJECT — DATASET AUDIT",
        "=" * 52,
        f"Project: {ROOT}",
        f"Datasets: {DATA}",
        ""
    ]
    duplicates = defaultdict(list)
    total = 0
    missing = []

    for task in TASKS:
        report.append(f"\n[{task.upper()}]")
        task_total = 0
        for split in SPLITS:
            split_total = 0
            report.append(f"  {split}:")
            for cls in CLASSES:
                folder = DATA / task / split / cls
                if not folder.is_dir():
                    missing.append(str(folder.relative_to(ROOT)))
                    report.append(f"    {cls}: MISSING FOLDER")
                    continue
                files = sorted(p for p in folder.rglob("*")
                               if p.is_file() and p.suffix.lower() in EXTS)
                formats = Counter(p.suffix.lower() for p in files)
                report.append(f"    {cls}: {len(files)} image(s)")
                if formats:
                    report.append("      Formats: " + ", ".join(
                        f"{ext}={n}" for ext, n in sorted(formats.items())))
                split_total += len(files)
                task_total += len(files)
                total += len(files)
                for p in files:
                    duplicates[(task, sha256(p))].append(
                        (split, str(p.relative_to(ROOT))))
            report.append(f"  Total {split}: {split_total}")
        report.append(f"  Total {task}: {task_total}")

    report.append("\n[IDENTICAL FILE CHECK ACROSS TRAINING/TESTING]")
    found = []
    for (task, _), entries in duplicates.items():
        if {s for s, _ in entries} == {"training", "testing"}:
            found.append((task, entries))
    if found:
        report.append(f"WARNING: {len(found)} identical image(s) appear in both splits.")
        for task, entries in found:
            report.append(f"  {task}:")
            report.extend(f"    {split}: {path}" for split, path in entries)
    else:
        report.append("No byte-identical files found across the two splits.")

    report.append("\n[EXPECTED FOLDERS]")
    if missing:
        report.append("Missing folders:")
        report.extend(f"  - {x}" for x in missing)
    else:
        report.append("All expected class/split folders exist.")

    report += [
        f"\nTotal images found: {total}",
        "",
        "IMPORTANT: This check cannot establish participant-level separation.",
        "If multiple drawings belong to one participant, all that participant's",
        "drawings must remain in the same split to prevent data leakage.",
        "This audit does not establish clinical validity; the project is an",
        "experimental screening prototype, not a diagnostic tool."
    ]

    text = "\n".join(report)
    out = ROOT / "documentation" / "dataset_audit_report.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"\nReport saved to: {out}")

if __name__ == "__main__":
    main()
