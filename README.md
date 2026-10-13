# CO₂ CEMS Thermal Modeling

Projeto desenvolvido na disciplina **EQM2118: Modelagem Matemática com Aplicação de Inteligência Artificial**, utilizando dados horários públicos da **U.S. Environmental Protection Agency (EPA)**, provenientes do ecossistema **CEMS/CAMPD**, para analisar e modelar emissões de CO₂ de uma unidade termelétrica a carvão.

A unidade piloto é a **Iatan Unit 2**, Facility ID 6065, Missouri, com série horária inicial de 2025.

## Apresentação do Trabalho

A apresentação em vídeo do Trabalho 1 está disponível no YouTube:

https://youtu.be/EUEqmm9nRHQ

## Notebooks e Google Colab

| Etapa | Notebook | Objetivo | Google Colab |
|---|---|---|---|
| 01 | [01_selecao_unidade_estudo.ipynb](notebooks/01_selecao_unidade_estudo.ipynb) | Seleção da unidade de estudo | [Abrir no Colab](https://colab.research.google.com/drive/11KpbBLZD8xo9CS2H6HKUW2Bd32spE-_S) |
| 02 | [02_tratamento_dados.ipynb](notebooks/02_tratamento_dados.ipynb) | Auditoria, tratamento e preparação da base | [Abrir no Colab](https://colab.research.google.com/drive/1PtW8T_oWDK9-e9OHMkgngsNpGTJ87PyN) |
| 03A | [03A_modelagem_preditiva_co2.ipynb](notebooks/03A_modelagem_preditiva_co2.ipynb) | Modelagem preditiva inicial | [Abrir no Colab](https://colab.research.google.com/drive/18alc2xYDM511l5pSXpIXXxkDFrSWAC8M) |
| 03A.01 | [03A.01_modelagem_preditiva_co2.ipynb](notebooks/03A.01_modelagem_preditiva_co2.ipynb) | Enriquecimento temporal da trajetória | [Abrir no Colab](https://colab.research.google.com/drive/1DVjl1v-wgQgWWtIyfE_bkCAdiVVjqJuW) |
| 03A.02 | [03A.02_comparacao_modelos_gradient_boosting.ipynb](notebooks/03A.02_comparacao_modelos_gradient_boosting.ipynb) | Comparação MLP x XGBoost e validação temporal | [Abrir no Colab](https://colab.research.google.com/drive/1BRbZkilK4omkxV7QjMbx3uPYkI7acsNY) |
| 03A.03 | [03A.03_otimizacao_pareada_xgboost.ipynb](notebooks/03A.03_otimizacao_pareada_xgboost.ipynb) | Busca pareada A x B e valor incremental da trajetória | [Abrir no Colab](https://colab.research.google.com/drive/1wbDqQxBoOi4qURULPh9EFTnNXpFUhgYj) |

## Executar o projeto

Os arquivos `.ipynb` são notebooks executáveis. No GitHub eles são exibidos de forma estática. Para executar as células, utilize os links do Google Colab acima.

A execução deve seguir a ordem indicada na tabela.

O Notebook 1 utiliza uma chave da API da EPA armazenada como segredo do Google Colab com o nome `EPA_API_KEY`. A chave não é armazenada no repositório.

A pasta persistente utilizada no Google Drive é:

```text
/content/drive/MyDrive/co2-cems-thermal-modeling
```

Os arquivos horários brutos e intermediários podem ser volumosos e, por isso, não são versionados no GitHub.

Para execução local:

```bash
pip install -r requirements.txt
```

## Contexto do projeto

O projeto investiga a previsão de emissões horárias de CO₂ a partir do comportamento operacional de uma unidade termelétrica.

A questão que orientou a primeira sequência de experimentos foi:

> **Em que medida a inclusão de informações sobre estados, memória e trajetória operacional melhora a estimação das emissões horárias de CO₂ em relação ao uso apenas da carga instantânea?**

A etapa atual avançou além da preparação da base e já inclui modelagem por MLP e XGBoost, validação temporal, busca de hiperparâmetros e diagnóstico por contexto operacional.

Nenhum modelo obtido até o Notebook 03A.03 é tratado como modelo final da Iatan.

## Fonte dos dados

Os dados são provenientes da **U.S. EPA**, com resolução horária.

O recorte inicial utilizado nos experimentos é o ano de **2025**.

Os arquivos brutos e intermediários de grande volume não são versionados. O código necessário para seleção, tratamento e análise permanece documentado nos notebooks.

## Seleção da unidade de estudo

> Caracterização técnica detalhada da unidade: [relatorio_caracterizacao_tecnica_iatan_unit2.md](outputs/reports/relatorio_caracterizacao_tecnica_iatan_unit2.md)

A seleção partiu de uma população ampla de unidades termelétricas a carvão e aplicou critérios sucessivos de elegibilidade estrutural, disponibilidade de dados, cobertura de monitoramento, qualidade da série horária e comportamento operacional.

A unidade selecionada foi:

- **Facility:** Iatan
- **Facility ID:** 6065
- **Unit:** 2
- **Estado:** Missouri (MO)
- **Ano inicial de análise:** 2025
- **Registros horários:** 8.760

A Iatan Unit 2 foi escolhida por apresentar boa qualidade dos dados, número relevante de transições operacionais, ampla faixa de carga e variabilidade suficiente para investigar efeitos de estados e trajetórias operacionais.

O processo completo está documentado em:

- [Notebook 1](notebooks/01_selecao_unidade_estudo.ipynb)
- [Relatório de seleção](outputs/reports/relatorio_selecao_unidade.md)

## Tratamento e preparação dos dados

O Notebook 2 realiza a preparação da série da unidade selecionada.

As principais etapas foram:

1. auditoria estrutural e temporal da base;
2. análise e tratamento de dados faltantes;
3. representação básica dos estados operacionais;
4. detecção exploratória de outliers;
5. engenharia de atributos orientada ao processo;
6. análise de componentes principais (PCA);
7. definição da base experimental;
8. divisão temporal em treino, validação e teste;
9. normalização Min-Max.

O processo completo está documentado em:

- [Notebook 2](notebooks/02_tratamento_dados.ipynb)
- [Relatório de tratamento](outputs/reports/relatorio_tratamento_dados.md)

## Qualidade dos dados

A série selecionada contém **8.760 registros horários** e cobre integralmente o ano de 2025.

Na auditoria foram observados:

- ausência de timestamps duplicados;
- ausência de lacunas na sequência horária;
- ausência de dados faltantes de carga ou CO₂ durante a operação;
- **6.249 horas operacionais**;
- **2.511 horas com a unidade desligada**;
- **77 horas de operação parcial**.

Os valores ausentes de carga e CO₂ nas horas OFF foram preservados nas variáveis originais e representados como zero apenas em novas variáveis tratadas destinadas às etapas posteriores de análise e modelagem.

## Engenharia de atributos

Foram criadas variáveis capazes de representar não apenas a condição instantânea, mas também a trajetória recente da unidade, incluindo:

- carga atual;
- carga da hora anterior;
- variação horária da carga;
- intensidade absoluta da variação;
- média de carga nas três horas anteriores;
- Operating Time da hora anterior;
- eventos de startup e shutdown;
- direção da mudança de carga;
- tempo desde o último startup;
- hora do dia;
- mês.

No período analisado foram identificados:

- **38 startups**;
- **37 shutdowns**.

Nenhuma variável derivada de CO₂ foi utilizada como atributo preditivo, evitando vazamento da variável-alvo.

## Análise de outliers

A detecção exploratória de outliers foi realizada pelo método do **intervalo interquartil (IQR)** somente durante as horas operacionais.

Foram encontrados:

- **0 outliers de carga**;
- **3 outliers de CO₂**, aproximadamente 0,05% das horas operacionais.

Os registros não foram removidos automaticamente. Em processos industriais, valores estatisticamente extremos podem corresponder a regimes operacionais reais.

## PCA exploratória

A **Análise de Componentes Principais (PCA)** foi aplicada a sete variáveis operacionais com o objetivo de investigar redundância e potencial de redução de dimensionalidade.

| Componente | Variância explicada | Variância acumulada |
|---|---:|---:|
| PC1 | 44,07% | 44,07% |
| PC2 | 16,51% | 60,57% |
| PC3 | 14,15% | 74,72% |
| PC4 | 13,27% | 87,99% |
| PC5 | 11,66% | 99,65% |

Foram necessárias **cinco componentes para superar 90% da variância**. Como a redução de 7 para 5 dimensões foi pequena frente à perda de interpretabilidade física, as variáveis originais foram preservadas.

Os loadings apresentaram interpretação operacional consistente:

- **PC1:** predominantemente associada ao nível de carga;
- **PC2:** predominantemente associada à dinâmica e às rampas de carga.

A PCA foi mantida como ferramenta exploratória e não como substituta das features originais.

## Decisões metodológicas do tratamento

Nem todas as técnicas foram aplicadas automaticamente. A escolha foi condicionada à natureza do problema e dos dados.

| Técnica | Decisão | Justificativa |
|---|---|---|
| Tratamento de faltantes | Aplicado | Ausências estruturais associadas ao estado OFF |
| Interpolação por spline | Não aplicada | Não existem lacunas durante a operação |
| Detecção de outliers por IQR | Aplicada | Diagnóstico sem remoção automática |
| Feature engineering | Aplicada | Representação de estados e trajetórias operacionais |
| PCA | Aplicada de forma exploratória | Avaliação de redundância |
| SMOTE | Não aplicado | O problema é de regressão |
| Divisão aleatória treino/teste | Não aplicada | A ordem temporal deve ser preservada |
| Normalização Min-Max | Aplicada | Preparação para modelos sensíveis à escala |

## Preparação experimental inicial

A base destinada à modelagem considera apenas as horas em que a unidade está operando.

A separação temporal inicial foi:

- **Treino:** janeiro a setembro de 2025, 4.894 observações;
- **Validação:** outubro de 2025, 211 observações;
- **Teste:** novembro e dezembro de 2025, 1.144 observações.

O `MinMaxScaler` foi ajustado somente sobre o conjunto de treino e aplicado posteriormente aos períodos de validação e teste.

Nos experimentos posteriores, novembro e dezembro passaram a ser tratados como **holdout histórico de comparação**, pois já haviam sido observados ao longo do desenvolvimento e não constituem mais teste final completamente cego.

# Modelagem preditiva

## Notebook 03A: experimento inicial com MLP

Foram comparados:

- **Cenário A:** carga instantânea;
- **Cenário B:** carga + memória e trajetória operacional.

Resultados no conjunto de teste histórico:

| Cenário | MAE | RMSE | R² |
|---|---:|---:|---:|
| A | 67,25 | 70,90 | 0,8779 |
| B | 61,61 | 67,04 | 0,8908 |

O Cenário B reduziu o MAE em aproximadamente **8,39%**.

Nas primeiras seis horas após startup, a redução foi de aproximadamente **26,15%**. Em rampas intensas, entretanto, B apresentou pior desempenho que A.

## Notebook 03A.01: trajetória temporal enriquecida

O Cenário C ampliou a representação temporal mantendo a mesma família MLP.

Resultados principais:

- MAE B: **61,61**;
- MAE C: **62,65**;
- melhora de C em startups: **22,67%** em relação a B;
- melhora de C em rampas intensas: **1,33%**.

O aumento do número de variáveis temporais não produziu melhora global consistente.

## Notebook 03A.02: comparação com XGBoost

A família de modelo foi alterada para XGBoost e os Cenários A, B e C foram avaliados em cinco folds temporais progressivos.

| Cenário | Features | MAE médio |
|---|---:|---:|
| A | 1 | 56,61 |
| B | 7 | 56,23 |
| C | 24 | 55,69 |

No holdout histórico:

| Cenário | MAE | RMSE | R² |
|---|---:|---:|---:|
| A-XGBoost | 22,96 | 28,06 | 0,9809 |
| B-XGBoost | 23,27 | 28,81 | 0,9798 |
| C-XGBoost | 25,02 | 30,63 | 0,9772 |

A mudança de MLP para XGBoost foi o principal fator de redução do erro.

Os sanity checks verificaram:

- ausência de features derivadas de CO₂;
- reconstrução consistente das features;
- threshold de rampa calculado no conjunto de desenvolvimento;
- ordem temporal correta;
- ausência de sobreposição entre treino, validação e holdout;
- alinhamento das 1.144 observações usadas nas comparações.

## Notebook 03A.03: busca pareada A x B

Foram avaliadas **30 configurações** para cada cenário nos mesmos cinco folds, totalizando **300 ajustes**.

Resultados principais:

- B venceu **4 de 5 folds**;
- ganho médio de B na validação temporal: **+0,89%**;
- ganho de B no holdout histórico: **-1,18%**;
- ganho de B nas primeiras 6 h após startup: **-4,34%**;
- ganho de B em rampas intensas: **+4,88%**.

A conclusão atual é:

> Para a Iatan Unit 2, considerando os dados de 2025 e as variáveis de trajetória avaliadas, não foi observada evidência robusta de ganho preditivo global e consistente da trajetória operacional além daquele obtido com a carga instantânea.

O comportamento em rampas intensas permanece como hipótese exploratória.

## Decisão metodológica atual

O A-XGBoost do Notebook 03A.02 permanece como **modelo de referência**, por apresentar o melhor desempenho absoluto observado até aqui com apenas uma feature.

Ele **não é considerado modelo final da Iatan**.

Antes de qualquer generalização entre termelétricas, será investigada a generalização temporal intraplanta.

As questões seguintes são:

1. mais anos de dados reduzem o erro?;
2. qual volume histórico é suficiente para estabilizar o desempenho?;
3. o modelo consegue prever um período futuro completamente não observado?;
4. o desempenho é estável entre diferentes anos?;
5. existe drift na relação carga e CO₂?;
6. a trajetória continua apresentando pequeno ganho incremental com maior histórico?;
7. em quais regimes o modelo apresenta maiores erros?;
8. é necessário retreinamento periódico?

## Próximo experimento

Notebook planejado:

`03A.04_volume_dados_generalizacao_temporal_iatan.ipynb`

Pergunta central:

> **A ampliação do histórico de treinamento melhora de forma consistente a capacidade de prever emissões futuras de CO₂ da Iatan Unit 2?**

A estratégia prevista inclui:

- incorporação de anos adicionais;
- janelas crescentes de treinamento;
- curva de aprendizado temporal;
- validação entre anos;
- teste futuro completamente fora da amostra;
- comparação entre modelo estático e atualização periódica;
- análise de drift;
- reavaliação de startups e rampas;
- métricas absolutas e normalizadas de erro.

## Artefatos gerados

Os resultados estão organizados em:

- [outputs/reports](outputs/reports): relatórios de seleção, tratamento, modelagem e diagnósticos;
- [outputs/tables](outputs/tables): métricas, previsões, folds, sanity checks e resultados da busca pareada;
- [outputs/figures](outputs/figures): figuras exploratórias e diagnósticos dos modelos.

## Estrutura atual do repositório

```text
co2-cems-thermal-modeling/
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   ├── 01_selecao_unidade_estudo.ipynb
│   ├── 02_tratamento_dados.ipynb
│   ├── 03A_modelagem_preditiva_co2.ipynb
│   ├── 03A.01_modelagem_preditiva_co2.ipynb
│   ├── 03A.02_comparacao_modelos_gradient_boosting.ipynb
│   └── 03A.03_otimizacao_pareada_xgboost.ipynb
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── pipeline/
└── outputs/
    ├── reports/
    ├── figures/
    ├── tables/
    └── presentations/
```

## Autores

- Guilherme Pereira Rodrigues da Costa
- Felipe Calmon
- Thiago Menezes

## Disciplina

**EQM2118: Modelagem Matemática com Aplicação de Inteligência Artificial**  
Professor: **Brunno Ferreira dos Santos**  
PUC-Rio
