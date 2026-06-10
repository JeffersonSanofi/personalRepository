import pandas as pd
from typing import List, Dict, Any

_TYPE_MAP = {
    'int':      'int64',
    'float':    'float64',
    'str':      'str',
    'string':   'str',
    'bool':     'bool',
    'date':     'datetime64[ns]',
    'datetime': 'datetime64[ns]',
}


def apply_transformations(df: pd.DataFrame, transformations: List[Dict[str, Any]]) -> pd.DataFrame:
    for step in transformations:
        t_type = step.get('type')
        handler = _HANDLERS.get(t_type)
        if not handler:
            raise ValueError(
                f"Transformação '{t_type}' desconhecida. Disponíveis: {list(_HANDLERS)}"
            )
        df = handler(df, step)
        print(f"    → {t_type}: {len(df)} linhas × {len(df.columns)} colunas")
    return df


def _rename_columns(df, cfg):
    return df.rename(columns=cfg['mapping'])


def _drop_columns(df, cfg):
    cols = [c for c in cfg['columns'] if c in df.columns]
    return df.drop(columns=cols)


def _select_columns(df, cfg):
    return df[cfg['columns']]


def _filter_rows(df, cfg):
    return df.query(cfg['condition'])


def _cast_types(df, cfg):
    for col, dtype in cfg['columns'].items():
        if col not in df.columns:
            continue
        mapped = _TYPE_MAP.get(dtype, dtype)
        if mapped == 'datetime64[ns]':
            df[col] = pd.to_datetime(df[col])
        else:
            df[col] = df[col].astype(mapped)
    return df


def _drop_duplicates(df, cfg):
    return df.drop_duplicates(subset=cfg.get('subset'))


def _drop_nulls(df, cfg):
    return df.dropna(subset=cfg.get('columns'))


def _fill_nulls(df, cfg):
    # Accepts either `values: {col: val}` (per column) or `value: x` (all columns)
    if 'values' in cfg:
        return df.fillna(cfg['values'])
    return df.fillna(cfg['value'])


def _add_column(df, cfg):
    df = df.copy()
    df[cfg['name']] = df.eval(cfg['expression'])
    return df


def _sort(df, cfg):
    return df.sort_values(by=cfg['columns'], ascending=cfg.get('ascending', True))


def _aggregate(df, cfg):
    agg_kwargs = {
        out_col: pd.NamedAgg(column=agg['column'], aggfunc=agg['func'])
        for out_col, agg in cfg['aggregations'].items()
    }
    return df.groupby(cfg['group_by']).agg(**agg_kwargs).reset_index()


_HANDLERS = {
    'rename_columns':  _rename_columns,
    'drop_columns':    _drop_columns,
    'select_columns':  _select_columns,
    'filter_rows':     _filter_rows,
    'cast_types':      _cast_types,
    'drop_duplicates': _drop_duplicates,
    'drop_nulls':      _drop_nulls,
    'fill_nulls':      _fill_nulls,
    'add_column':      _add_column,
    'sort':            _sort,
    'aggregate':       _aggregate,
}
