import os
from typing import Dict, Any, List
from collections import Counter
from PIL import Image

class DatasetInspector:
    """
    DatasetInspector analyzes a dataset directory containing images and optional
    folder-based class structure.

    It computes:
        - total image count
        - class distribution (if directories represent classes)
        - file type distribution
        - corrupt image files
        - class imbalance ratio
        - missing labels (images in root folder, empty directories)
    """

    SUPPORTED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

    def _is_image_corrupt(self, path: str) -> bool:
        try:
            with Image.open(path) as img:
                img.verify()  # verify does not decode fully, but detects corruption
            return False
        except Exception:
            return True

    def inspect(self, dataset_path: str) -> Dict[str, Any]:
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset path not found: {dataset_path}")

        file_types = Counter()
        class_counts = Counter()
        corrupt_files: List[str] = []
        image_files: List[str] = []
        missing_label_files: List[str] = []

        _, class_dirs, _ = next(os.walk(dataset_path))

        # Classes are first-level folders
        valid_classes = set(class_dirs)

        for root, _, files in os.walk(dataset_path):
            class_label = os.path.basename(root)
            is_root = (root == dataset_path)

            for f in files:
                ext = os.path.splitext(f)[1].lower()
                file_types[ext] += 1

                full_path = os.path.join(root, f)

                if ext in self.SUPPORTED_IMAGE_EXT:
                    image_files.append(full_path)

                    # Missing label = image placed directly in dataset root
                    if is_root:
                        missing_label_files.append(full_path)

                    # Otherwise count class
                    elif class_label in valid_classes:
                        class_counts[class_label] += 1

                    # Check corruption
                    if self._is_image_corrupt(full_path):
                        corrupt_files.append(full_path)

        # Compute class imbalance
        imbalance = {}
        if class_counts:
            max_count = max(class_counts.values())
            for cls, count in class_counts.items():
                imbalance[cls] = round(count / max_count, 3)

        # Detect empty class folders
        empty_classes = [cls for cls in valid_classes if class_counts.get(cls, 0) == 0]

        return {
            "dataset_path": dataset_path,
            "total_images": len(image_files),
            "file_types": dict(file_types),
            "class_distribution": dict(class_counts),
            "class_imbalance_ratio": imbalance,
            "corrupt_files": corrupt_files,
            "missing_label_images": missing_label_files,
            "empty_class_folders": empty_classes,
        }
