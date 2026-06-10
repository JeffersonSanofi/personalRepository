import pandas as pd
from pathlib import Path
from .loader import load_file
from .writer import write_file
from .transformations import apply_transformations


def run_pipeline(config: dict):
    source = config['source']

    print(f"  Carregando: {source['path']}")
    df = load_file(
        source['path'],
        fmt=source.get('format'),
        options=source.get('options'),
    )
    print(f"  Carregado: {len(df)} linhas × {len(df.columns)} colunas")

    # Bronze — cópia bruta sem modificações
    if 'bronze' in config:
        _save_layer(df, config['bronze'], 'bronze')

    # Silver — limpeza e padronização
    silver_df = df.copy()
    if 'silver' in config:
        silver_df = _transform_and_save(silver_df, config['silver'], 'silver')

    # Gold — agregações e lógica de negócio
    if 'gold' in config:
        _transform_and_save(silver_df.copy(), config['gold'], 'gold')


def _transform_and_save(df: pd.DataFrame, layer_config: dict, layer_name: str) -> pd.DataFrame:
    transformations = layer_config.get('transformations', [])
    if transformations:
        print(f"  [{layer_name.upper()}] Aplicando {len(transformations)} transformação(ões):")
        df = apply_transformations(df, transformations)
    _save_layer(df, layer_config, layer_name)
    return df


def _save_layer(df: pd.DataFrame, layer_config: dict, layer_name: str):
    save_as = layer_config.get('save_as', f'{layer_name}_output')
    fmt = layer_config.get('format', 'parquet')
    output_path = Path('data') / layer_name / f"{save_as}.{fmt}"
    write_file(df, output_path, fmt)
    print(f"  [{layer_name.upper()}] Salvo: {len(df)} linhas → {output_path}")
