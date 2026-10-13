# CO₂ CEMS Thermal Modeling

Projeto desenvolvido na disciplina **EQM2118: Modelagem Matemática com Aplicação de Inteligência Artificial**, com dados horários U.S. EPA CEMS/CAMPD e foco na previsão de emissões de CO₂ de uma unidade termelétrica a carvão.

A unidade piloto é a **Iatan Unit 2**, Facility ID 6065, Missouri. A série inicial cobre 2025 com resolução horária.

## Objetivo atual

A linha experimental investiga:

- capacidade de prever a massa horária de CO₂;
- efeito da família de modelo sobre o desempenho;
- valor incremental de informações de trajetória operacional;
- robustez temporal intraplanta;
- efeito do aumento do histórico de treinamento;
- capacidade de prever períodos futuros completamente fora da amostra.

Nenhum modelo obtido até o Notebook 03A.03 é tratado como modelo final da Iatan.

## Notebooks

| Etapa | Notebook | Objetivo | Google Colab |
|---|---|---|---|
| 01 | [01_selecao_unidade_estudo.ipynb](notebooks/01_selecao_unidade_estudo.ipynb) | Seleção da unidade piloto | [Abrir no Colab](https://colab.research.google.com/drive/11KpbBLZD8xo9CS2H6HKUW2Bd32spE-_S) |
| 02 | [02_tratamento_dados.ipynb](notebooks/02_tratamento_dados.ipynb) | Auditoria, tratamento e engenharia de atributos | [Abrir no Colab](https://colab.research.google.com/drive/1PtW8T_oWDK9-e9OHMkgngsNpGTJ87PyN) |
| 03A | [03A_modelagem_preditiva_co2.ipynb](notebooks/03A_modelagem_preditiva_co2.ipynb) | Modelagem preditiva inicial | [Abrir no Colab](https://colab.research.google.com/drive/18alc2xYDM511l5pSXpIXXxkDFrSWAC8M) |
| 03A.01 | [03A.01_modelagem_preditiva_co2.ipynb](notebooks/03A.01_modelagem_preditiva_co2.ipynb) | Trajetória temporal enriquecida | [Abrir no Colab](https://colab.research.google.com/drive/1DVjl1v-wgQgWWtIyfE_bkCAdiVVjqJuW) |
| 03A.02 | [03A.02_comparacao_modelos_gradient_boosting.ipynb](notebooks/03A.02_comparacao_modelos_gradient_boosting.ipynb) | MLP x XGBoost e validação temporal progressiva | [Abrir no Colab](https://colab.research.google.com/drive/1BRbZkilK4omkxV7QjMbx3uPYkI7acsNY) |
| 03A.03 | [03A.03_otimizacao_pareada_xgboost.ipynb](notebooks/03A.03_otimizacao_pareada_xgboost.ipynb) | Busca pareada A x B e valor incremental da trajetória | [Abrir no Colab](https://colab.research.google.com/drive/1wbDqQxBoOi4qURULPh9EFTnNXpFUhgYj) |

## Resultados até o Notebook 03A.03

### 03A.01: enriquecimento temporal com MLP

O Cenário C, com trajetória temporal enriquecida, não apresentou melhora global consistente sobre o Cenário B.

Principais resultados:

- MAE B: **61,61**;
- MAE C: **62,65**;
- melhora de C em startups: **22,67%**;
- melhora de C em rampas intensas: **1,33%**.

O resultado indicou que simplesmente ampliar o número de variáveis temporais não solucionava as limitações da MLP.

### 03A.02: comparação com XGBoost

A substituição da MLP por XGBoost produziu a principal melhora observada na sequência experimental.

Validação temporal progressiva:

| Cenário | Features | MAE médio |
|---|---:|---:|
| A | 1 | 56,61 |
| B | 7 | 56,23 |
| C | 24 | 55,69 |

Holdout histórico de novembro e dezembro de 2025:

| Cenário | MAE | RMSE | R² |
|---|---:|---:|---:|
| A-XGBoost | 22,96 | 28,06 | 0,9809 |
| B-XGBoost | 23,27 | 28,81 | 0,9798 |
| C-XGBoost | 25,02 | 30,63 | 0,9772 |

Os sanity checks não indicaram target leakage, vazamento temporal ou desalinhamento das bases.

O holdout de novembro e dezembro é mantido como **referência histórica de comparação**, não como teste final completamente cego, pois já foi observado durante o desenvolvimento.

### 03A.03: busca pareada A x B

Foram avaliadas 30 configurações de hiperparâmetros para A e B nos mesmos cinco folds temporais, totalizando 300 ajustes.

Resultados:

- B venceu **4 de 5 folds**;
- ganho médio de B na validação temporal: **+0,89%**;
- ganho de B no holdout histórico: **-1,18%**;
- ganho de B nas primeiras 6 h após startup: **-4,34%**;
- ganho de B em rampas intensas: **+4,88%**.

Conclusão atual:

> Para a Iatan Unit 2, considerando os dados de 2025 e as variáveis de trajetória avaliadas, não foi observada evidência robusta de ganho preditivo global e consistente da trajetória operacional além daquele obtido com a carga instantânea.

O efeito positivo observado em rampas intensas permanece como hipótese a ser reavaliada com maior histórico.

## Decisão metodológica

O A-XGBoost do Notebook 03A.02 é o **modelo de referência atual**, por apresentar o melhor desempenho absoluto observado até aqui com apenas uma feature.

Ele ainda não é considerado modelo final.

Antes de qualquer generalização entre termelétricas, será investigada a **generalização temporal intraplanta** da Iatan.

As questões seguintes são:

1. mais anos de dados reduzem o erro?;
2. qual volume histórico é suficiente para estabilizar o desempenho?;
3. o modelo consegue prever um período futuro completamente não observado?;
4. o desempenho permanece estável entre diferentes anos?;
5. existe drift na relação entre carga e CO₂?;
6. a trajetória continua apresentando pequeno ganho incremental com maior histórico?;
7. em quais condições operacionais ocorrem os maiores erros?;
8. é necessário retreinamento periódico?

## Próximo experimento

Notebook planejado:

**03A.04_volume_dados_generalizacao_temporal_iatan.ipynb**

Pergunta central:

> A ampliação do histórico de treinamento melhora de forma consistente a capacidade de prever emissões futuras de CO₂ da Iatan Unit 2?

A estratégia incluirá curvas de aprendizado temporal, múltiplos anos, teste verdadeiramente fora da amostra, comparação entre modelo estático e atualização periódica, análise de drift e métricas de erro normalizadas.

## Artefatos

Os produtos gerados estão versionados em:

- [outputs/reports](outputs/reports): relatórios dos experimentos e diagnósticos;
- [outputs/tables](outputs/tables): métricas, previsões, folds, sanity checks e resultados da busca pareada;
- [outputs/figures](outputs/figures): figuras de validação, previsões, importância de variáveis e diagnósticos operacionais.

Arquivos brutos e intermediários volumosos, credenciais e modelos binários não são versionados.

## Estrutura

```text
co2-cems-thermal-modeling/
├── README.md
├── requirements.txt
├── notebooks/
│   ├── 01_selecao_unidade_estudo.ipynb
│   ├── 02_tratamento_dados.ipynb
│   ├── 03A_modelagem_preditiva_co2.ipynb
│   ├── 03A.01_modelagem_preditiva_co2.ipynb
│   ├── 03A.02_comparacao_modelos_gradient_boosting.ipynb
│   └── 03A.03_otimizacao_pareada_xgboost.ipynb
├── data/
├── pipeline/
└── outputs/
    ├── reports/
    ├── tables/
    ├── figures/
    └── presentations/
```

## Apresentação

Vídeo do Trabalho 1: https://youtu.be/EUEqmm9nRHQ

## Autores

- Guilherme Pereira Rodrigues da Costa
- Felipe Calmon
- Thiago Menezes

## Disciplina

**EQM2118: Modelagem Matemática com Aplicação de Inteligência Artificial**  
Professor: **Brunno Ferreira dos Santos**  
PUC-Rio
