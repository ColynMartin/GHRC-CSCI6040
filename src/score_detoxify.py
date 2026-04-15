from __future__ import annotations

from typing import Dict, List

try:
    from detoxify import Detoxify
except Exception:  # pragma: no cover
    Detoxify = None


class DetoxifyScorer:
    def __init__(self, model_name: str = "original") -> None:
        self.model_name = model_name
        self.model = None
        if Detoxify is None:
            raise ImportError(
                "Detoxify is not installed. Install requirements.txt before running this project."
            )
        self.model = Detoxify(model_name)

    def score_texts(self, texts: List[str]) -> List[Dict[str, float]]:
        if not texts:
            return []
        raw = self.model.predict(texts)
        keys = list(raw.keys())
        results: List[Dict[str, float]] = []
        for i in range(len(texts)):
            row = {k: float(raw[k][i]) for k in keys}
            row["toxicity"] = float(row.get("toxicity", 0.0))
            results.append(row)
        return results
