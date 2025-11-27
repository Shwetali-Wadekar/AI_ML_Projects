import re
from typing import Dict, Any, List

class MetricsParser:
    """
    Generic metrics parser: extracts numerical metrics from text.
    Useful when scraping Google Search results or parsing LLM output.

    Recognizes:
    - accuracy, precision, recall, f1-score
    - mAP@50, mAP@50-95
    - IoU, Dice, pixel accuracy
    - top-1, top-5 accuracy
    """

    METRIC_PATTERNS = {
        "accuracy": r"(accuracy|acc)\s*[:=\s]\s*([0-9.]+)",
        "precision": r"(precision)\s*[:=\s]\s*([0-9.]+)",
        "recall": r"(recall)\s*[:=\s]\s*([0-9.]+)",
        "f1": r"(f1|f1-score)\s*[:=\s]\s*([0-9.]+)",
        "iou": r"(iou|intersection over union)\s*[:=\s]\s*([0-9.]+)",
        "dice": r"(dice)\s*[:=\s]\s*([0-9.]+)",
        "pixel_accuracy": r"(pixel\s*accuracy)\s*[:=\s]\s*([0-9.]+)",
        "top1": r"(top[-\s]?1)\s*[:=\s]\s*([0-9.]+)",
        "top5": r"(top[-\s]?5)\s*[:=\s]\s*([0-9.]+)",
        "map50": r"(map[@\s]?50)\s*[:=\s]\s*([0-9.]+)",
        "map50_95": r"(map[@\s]?50-95|map50-95)\s*[:=\s]\s*([0-9.]+)",
    }

    def parse(self, text: str) -> Dict[str, Any]:
        metrics = {}
        for metric, pattern in self.METRIC_PATTERNS.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    metrics[metric] = float(match.group(2))
                except ValueError:
                    pass
        return metrics

    def extract_all(self, texts: List[str]) -> Dict[str, Any]:
        collected = {}
        for t in texts:
            parsed = self.parse(t)
            collected.update(parsed)
        return collected