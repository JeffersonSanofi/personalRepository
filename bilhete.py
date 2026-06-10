#!/usr/bin/env python3
"""
bilhete.py — Orquestrador de pipeline medallion (bronze → prata → ouro).

Uso:
    python bilhete.py                        # usa config.yaml
    python bilhete.py meu_config.yaml        # usa outro arquivo
    python bilhete.py config.yaml -p vendas  # roda só o pipeline "vendas"
"""
import argparse
import sys
from pathlib import Path
import yaml
from pipeline.runner import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description='Executa pipelines de dados a partir de um arquivo YAML.'
    )
    parser.add_argument('config', nargs='?', default='config.yaml',
                        help='Caminho para o arquivo YAML de configuração (padrão: config.yaml)')
    parser.add_argument('--pipeline', '-p',
                        help='Executa apenas o pipeline com este nome')
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Erro: arquivo de configuração '{config_path}' não encontrado.")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Suporta tanto `pipelines: [...]` (lista) quanto um único `pipeline:` na raiz
    pipelines = config.get('pipelines') or [config.get('pipeline', config)]

    executed = 0
    for pipeline_config in pipelines:
        name = pipeline_config.get('name', 'sem-nome')
        if args.pipeline and name != args.pipeline:
            continue

        print(f"\n{'='*55}")
        print(f"  Pipeline: {name}")
        print(f"{'='*55}")

        try:
            run_pipeline(pipeline_config)
            executed += 1
        except Exception as e:
            print(f"\n  ERRO no pipeline '{name}': {e}")
            sys.exit(1)

    if executed == 0:
        print(f"Nenhum pipeline encontrado com nome '{args.pipeline}'.")
        sys.exit(1)

    print(f"\n{'='*55}")
    print(f"  {executed} pipeline(s) concluído(s) com sucesso.")
    print(f"{'='*55}\n")


if __name__ == '__main__':
    main()
