DATASET AUDIT — QUICK START

1. Copy audit_dataset.py into Parkinsons_project/training/
2. Open Parkinsons_project in VS Code.
3. Run in the terminal:
   python training/audit_dataset.py
4. Read the printed summary. A copy is saved to:
   documentation/dataset_audit_report.txt

The script is read-only: it does not rename, move, delete, or edit images.
It counts common image formats and checks for byte-identical images appearing
in both training and testing splits.

Important: identical-file checking does not prove participant-level separation.
If the dataset has participant IDs, verify that one person's drawings do not
appear in both training and testing.
