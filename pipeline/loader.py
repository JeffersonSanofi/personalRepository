import pandas as pd
from pathlib import Path

_READERS = {
    'csv':     lambda p, opts: pd.read_csv(p, **opts),
    'json':    lambda p, opts: pd.read_json(p, **opts),
    'parquet': lambda p, opts: pd.read_parquet(p, **opts),
    'xlsx':    lambda p, opts: pd.read_excel(p, **opts),
    'xls':     lambda p, opts: pd.read_excel(p, **opts),
}


def load_file(path: str, fmt: str = None, options: dict = None) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {path}")

    ext = fmt or p.suffix.lstrip('.').lower()
    reader = _READERS.get(ext)
    if not reader:
        raise ValueError(f"Formato '{ext}' não suportado. Suportados: {list(_READERS)}")

    return reader(p, options or {})
