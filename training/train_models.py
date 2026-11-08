"""
Parkinson's Screening Project — Spiral and Wave Random Forest Training
========================================================================
Save this file as:
    Parkinsons_project/training/train_models.py

Expected dataset structure:
    datasets/
      spiral/
        training/healthy/
        training/parkinsons/
        testing/healthy/
        testing/parkinsons/
      wave/
        training/healthy/
        training/parkinsons/
        testing/healthy/
        testing/parkinsons/

What this script does:
  1. Loads PNG/JPG/BMP/TIFF images from the folders above.
  2. Converts each image to grayscale and resizes it to 200 x 200.
  3. Extracts HOG (Histogram of Oriented Gradients) features.
  4. Trains one Random Forest for spiral images and one for wave images.
  5. Tunes hyperparameters using cross-validation on TRAINING data only.
  6. Evaluates each final model once on the separate TESTING data.
  7. Saves model bundles and evaluation reports.

IMPORTANT:
  - This is an experimental academic screening prototype, not a diagnostic tool.
  - Keep the original dataset split. Do not move testing images into training.
  - If participant IDs exist, verify that one participant does not contribute
    images to both training and testing. A paper being peer-reviewed does not
    by itself prove participant-level separation or clinical validity.
"""

from pathlib import Path
from collections import Counter
import json
import warnings

import joblib
import numpy as np
from PIL import Image, ImageFile
from skimage.feature import hog

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

ImageFile.LOAD_TRUNCATED_IMAGES = False

# ---------------------------------------------------------------------
# PATHS AND SETTINGS
# ---------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_ROOT = PROJECT_ROOT / "datasets"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "documentation" / "model_evaluation"

TASKS = ("spiral", "wave")
CLASSES = ("healthy", "parkinsons")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}

IMAGE_SIZE = (200, 200)  # width, height
HOG_ORIENTATIONS = 9
HOG_PIXELS_PER_CELL = (16, 16)
HOG_CELLS_PER_BLOCK = (2, 2)

RANDOM_STATE = 42
CV_SPLITS = 5

# Small, deliberately limited search. All tuning uses training data only.
PARAM_GRID = {
    "n_estimators": [200, 400],
    "max_depth": [None, 10],
    "min_samples_leaf": [1, 2],
    "max_features": ["sqrt"],
    "class_weight": ["balanced"],
}

# ---------------------------------------------------------------------
# IMAGE LOADING AND FEATURE EXTRACTION
# ---------------------------------------------------------------------
def find_images(folder: Path):
    """Return supported image files in a class folder, recursively."""
    return sorted(
        p for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def image_to_hog(path: Path) -> np.ndarray:
    """Load image, convert to grayscale, resize, and calculate HOG features."""
    try:
        with Image.open(path) as image:
            image = image.convert("L")
            image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
            pixels = np.asarray(image, dtype=np.float32) / 255.0
    except Exception as exc:
        raise RuntimeError(f"Could not read image: {path}\nReason: {exc}") from exc

    features = hog(
        pixels,
        orientations=HOG_ORIENTATIONS,
        pixels_per_cell=HOG_PIXELS_PER_CELL,
        cells_per_block=HOG_CELLS_PER_BLOCK,
        block_norm="L2-Hys",
        transform_sqrt=True,
        feature_vector=True,
    )
    return features.astype(np.float32)


def load_split(task: str, split: str):
    """Load one task/split and return HOG matrix, labels, and file paths."""
    features = []
    labels = []
    paths = []

    for label in CLASSES:
        class_folder = DATASET_ROOT / task / split / label
        if not class_folder.is_dir():
            raise FileNotFoundError(
                f"Required folder is missing:\n{class_folder}\n"
                "Check the folder names and project structure."
            )

        image_paths = find_images(class_folder)
        if not image_paths:
            raise RuntimeError(f"No supported images found in: {class_folder}")

        print(f"  {split}/{label}: {len(image_paths)} image(s)")
        for image_path in image_paths:
            features.append(image_to_hog(image_path))
            labels.append(label)
            paths.append(str(image_path.relative_to(PROJECT_ROOT)))

    X = np.vstack(features)
    y = np.asarray(labels)
    return X, y, paths


def check_class_counts(y, task, split):
    counts = Counter(y)
    for label in CLASSES:
        if counts[label] < CV_SPLITS and split == "training":
            raise ValueError(
                f"{task}: only {counts[label]} {label} training images. "
                f"At least {CV_SPLITS} are needed for {CV_SPLITS}-fold CV."
            )
    if set(counts) != set(CLASSES):
        raise ValueError(
            f"{task}/{split}: expected both classes {CLASSES}; found {dict(counts)}"
        )


# ---------------------------------------------------------------------
# TRAIN, TUNE, AND EVALUATE
# ---------------------------------------------------------------------
def train_one_task(task: str):
    print(f"\n{'=' * 68}\nTASK: {task.upper()}\n{'=' * 68}")

    print("\nLoading training images and extracting HOG features...")
    X_train, y_train, train_paths = load_split(task, "training")
    check_class_counts(y_train, task, "training")

    print("\nLoading testing images and extracting HOG features...")
    X_test, y_test, test_paths = load_split(task, "testing")
    check_class_counts(y_test, task, "testing")

    print(f"\nTraining feature matrix: {X_train.shape}")
    print(f"Testing feature matrix:  {X_test.shape}")
    print("Training class counts:", dict(Counter(y_train)))
    print("Testing class counts: ", dict(Counter(y_test)))

    cv = StratifiedKFold(
        n_splits=CV_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    base_model = RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1)
    search = GridSearchCV(
        estimator=base_model,
        param_grid=PARAM_GRID,
        scoring="f1_macro",
        cv=cv,
        n_jobs=-1,
        refit=True,
        return_train_score=False,
        verbose=1,
    )

    print("\nTuning Random Forest using training data only...")
    search.fit(X_train, y_train)
    best_model = search.best_estimator_

    # The test split is used only after model selection is complete.
    print("\nEvaluating the selected model on the untouched testing split...")
    predictions = best_model.predict(X_test)
    probabilities = best_model.predict_proba(X_test)
    positive_index = list(best_model.classes_).index("parkinsons")

    metrics = {
        "task": task,
        "training_images": int(len(y_train)),
        "testing_images": int(len(y_test)),
        "training_class_counts": dict(Counter(y_train)),
        "testing_class_counts": dict(Counter(y_test)),
        "image_size": list(IMAGE_SIZE),
        "feature_method": "HOG",
        "hog": {
            "orientations": HOG_ORIENTATIONS,
            "pixels_per_cell": list(HOG_PIXELS_PER_CELL),
            "cells_per_block": list(HOG_CELLS_PER_BLOCK),
            "block_norm": "L2-Hys",
            "transform_sqrt": True,
        },
        "best_parameters": search.best_params_,
        "best_training_cv_macro_f1": float(search.best_score_),
        "test_accuracy": float(accuracy_score(y_test, predictions)),
        "test_balanced_accuracy": float(balanced_accuracy_score(y_test, predictions)),
        "test_precision_macro": float(precision_score(
            y_test, predictions, average="macro", zero_division=0)),
        "test_recall_macro": float(recall_score(
            y_test, predictions, average="macro", zero_division=0)),
        "test_f1_macro": float(f1_score(
            y_test, predictions, average="macro", zero_division=0)),
        "confusion_matrix_labels": list(best_model.classes_),
        "confusion_matrix": confusion_matrix(
            y_test, predictions, labels=list(best_model.classes_)
        ).tolist(),
        "classification_report": classification_report(
            y_test, predictions, labels=list(best_model.classes_),
            output_dict=True, zero_division=0
        ),
        "test_files": test_paths,
    }

    try:
        metrics["test_roc_auc"] = float(
            roc_auc_score((y_test == "parkinsons").astype(int),
                          probabilities[:, positive_index])
        )
    except ValueError:
        metrics["test_roc_auc"] = None

    bundle = {
        "model": best_model,
        "task": task,
        "image_size": IMAGE_SIZE,
        "hog": {
            "orientations": HOG_ORIENTATIONS,
            "pixels_per_cell": HOG_PIXELS_PER_CELL,
            "cells_per_block": HOG_CELLS_PER_BLOCK,
            "block_norm": "L2-Hys",
            "transform_sqrt": True,
        },
        "class_names": list(best_model.classes_),
        "positive_class": "parkinsons",
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    model_path = MODEL_DIR / f"{task}_random_forest.joblib"
    report_path = REPORT_DIR / f"{task}_evaluation.json"

    joblib.dump(bundle, model_path)
    report_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print("\nRESULTS")
    print(f"Best parameters: {search.best_params_}")
    print(f"Training CV macro-F1: {search.best_score_:.3f}")
    print(f"Testing accuracy: {metrics['test_accuracy']:.3f}")
    print(f"Testing balanced accuracy: {metrics['test_balanced_accuracy']:.3f}")
    print(f"Testing macro-F1: {metrics['test_f1_macro']:.3f}")
    print("Confusion matrix (rows=true, columns=predicted):")
    print(confusion_matrix(y_test, predictions, labels=list(best_model.classes_)))
    print("\nClassification report:")
    print(classification_report(y_test, predictions, zero_division=0))
    print(f"Saved model: {model_path}")
    print(f"Saved report: {report_path}")

    return metrics


def main():
    print("PARKINSON'S SCREENING — RANDOM FOREST TRAINING")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Dataset root: {DATASET_ROOT}")

    if not DATASET_ROOT.is_dir():
        raise FileNotFoundError(
            f"Dataset folder not found: {DATASET_ROOT}\n"
            "Save this script inside the project's training folder."
        )

    all_metrics = []
    for task in TASKS:
        all_metrics.append(train_one_task(task))

    summary_path = REPORT_DIR / "training_summary.json"
    summary_path.write_text(json.dumps(all_metrics, indent=2), encoding="utf-8")

    print("\n" + "=" * 68)
    print("TRAINING COMPLETE")
    print(f"Models saved in: {MODEL_DIR}")
    print(f"Evaluation reports saved in: {REPORT_DIR}")
    print(f"Summary saved in: {summary_path}")
    print("=" * 68)
    print(
        "\nInterpret results cautiously: each test class contains only 15 images. "
        "A few changed predictions can noticeably change the reported metrics."
    )


if __name__ == "__main__":
    main()
