# Monitoramento de CO₂

Tabelas descritivas dos indicadores horários e das vigências dos planos da Iatan Unit 2, de 2011 a 2025. Os resumos somam 131.496 registros e 98.799 horas ON (`Operating Time > 0`).

- `annual_measurement_summary.csv`, `monthly_measurement_summary.csv` e `cohort_measurement_summary.csv`: cobertura, indicadores e massas por período.
- `indicator_raw_counts.csv` e `substitution_episodes.csv`: categorias reportadas e episódios com participação de substituição.
- `monitoring_plan_coverage.csv`, `component_coverage.csv` e `plan_*_history.csv`: método, fórmulas, sistemas, componentes e vigências.
- `co2_flow_component_changes.csv` e `snapshot_comparison.csv`: alterações de configuração e comparação dos planos.

Os percentuais usam todas as horas ON como denominador. A categoria mista não identifica a fração de massa substituída. Datas finais incluem a última hora declarada; continuidade documental não demonstra estabilidade instrumental ou de calibração.

Para recalcular, disponibilize os arquivos anuais em `data/interim/03A04_multiyear/` e execute, na raiz, `python scripts/caracterizar_monitoramento.py`. As fontes estão em [referências de monitoramento](../../../references/monitoramento/).
