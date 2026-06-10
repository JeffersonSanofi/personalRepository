import pandas as pd
from pathlib import Path

_WRITERS = {
    'csv':     lambda df, p: df.to_csv(p, index=False),
    'json':    lambda df, p: df.to_json(p, orient='records', force_ascii=False, indent=2),
    'parquet': lambda df, p: df.to_parquet(p, index=False),
    'xlsx':    lambda df, p: df.to_excel(p, index=False),
}


def write_file(df: pd.DataFrame, path: Path, fmt: str):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    writer = _WRITERS.get(fmt.lower())
    if not writer:
        raise ValueError(f"Formato de saída '{fmt}' não suportado. Suportados: {list(_WRITERS)}")

    writer(df, path)
