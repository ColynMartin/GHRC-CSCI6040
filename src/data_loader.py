from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd


@dataclass
class DatasetRecord:
    dataset: str
    row_id: int
    prompt: str
    metadata: Dict[str, str]


class DatasetLoader:
    def __init__(self, prompt_column_candidates: Iterable[str]) -> None:
        self.prompt_column_candidates = list(prompt_column_candidates)

    def _detect_prompt_column(self, df: pd.DataFrame) -> str:
        lower_map = {c.lower(): c for c in df.columns}
        for candidate in self.prompt_column_candidates:
            if candidate.lower() in lower_map:
                return lower_map[candidate.lower()]
        # fallback: first string-like column
        for col in df.columns:
            if pd.api.types.is_string_dtype(df[col]):
                return col
        raise ValueError(
            f"Could not detect prompt column. Available columns: {list(df.columns)}"
        )

    def load(self, dataset_name: str, path: str | Path, max_samples: int | None = None, shuffle: bool = True) -> List[DatasetRecord]:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")

        df = pd.read_csv(path)
        prompt_col = self._detect_prompt_column(df)
        df = df[df[prompt_col].notna()].copy()
        df[prompt_col] = df[prompt_col].astype(str).str.strip()
        df = df[df[prompt_col] != ""]

        if shuffle:
            df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        if max_samples is not None:
            df = df.head(max_samples)

        records: List[DatasetRecord] = []
        for idx, row in df.iterrows():
            metadata = {k: str(v) for k, v in row.to_dict().items() if k != prompt_col}
            records.append(
                DatasetRecord(
                    dataset=dataset_name,
                    row_id=int(idx),
                    prompt=str(row[prompt_col]),
                    metadata=metadata,
                )
            )
        return records
