# CO₂ CEMS Thermal Modeling

Projeto desenvolvido na disciplina **EQM2118: Modelagem Matemática com Aplicação de Inteligência Artificial**, utilizando dados horários públicos da **U.S. Environmental Protection Agency (EPA)**, provenientes do ecossistema **CEMS/CAMPD**, para analisar e modelar emissões de CO₂ de uma unidade termelétrica a carvão.

A unidade piloto é a **Iatan Unit 2**, Facility ID 6065, Missouri, com série horária inicial de 2025.

## Apresentação do Trabalho

A apresentação em vídeo do Trabalho 1 está disponível no YouTube:

https://youtu.be/EUEqmm9nRHQ

## Notebooks, procedimentos metodológicos e relatórios

| Etapa | Notebook | Objetivo | Procedimentos metodológicos | Relatório | Google Colab |
|---|---|---|---|---|---|
| 01 | [`01_selecao_unidade_estudo.ipynb`](notebooks/01_selecao_unidade_estudo.ipynb) | Seleção da unidade | Triagem sucessiva de elegibilidade; cobertura CEMS; caracterização operacional | [Abrir relatório](outputs/reports/relatorio_selecao_unidade.md) | [Abrir no Colab](https://colab.research.google.com/drive/11KpbBLZD8xo9CS2H6HKUW2Bd32spE-_S) |
| 02 | [`02_tratamento_dados.ipynb`](notebooks/02_tratamento_dados.ipynb) | Auditoria e preparação | Auditoria temporal; faltantes estruturais; IQR; *feature engineering*; PCA exploratória; *temporal split*; Min–Max | [Abrir relatório](outputs/reports/relatorio_tratamento_dados.md) | [Abrir no Colab](https://colab.research.google.com/drive/1PtW8T_oWDK9-e9OHMkgngsNpGTJ87PyN) |
| 03A | [`03A_modelagem_preditiva_co2.ipynb`](notebooks/03A_modelagem_preditiva_co2.ipynb) | MLP: carga versus trajetória | *Supervised regression*; MLP *feedforward*; Adam; MSE; *EarlyStopping*; *temporal holdout*; comparação A/B | [Abrir relatório](outputs/reports/relatorio_modelagem_preditiva_3A.md) | [Abrir no Colab](https://colab.research.google.com/drive/18alc2xYDM511l5pSXpIXXxkDFrSWAC8M) |
| 03A.01 | [`03A.01_modelagem_preditiva_co2.ipynb`](notebooks/03A.01_modelagem_preditiva_co2.ipynb) | Enriquecimento temporal | *Lagged* e *rolling-window features*; prevenção de *look-ahead bias*; comparação controlada B/C; diagnóstico descritivo de *distribution shift* | [Abrir relatório](outputs/reports/relatorio_modelagem_preditiva_03A01.md) | [Abrir no Colab](https://colab.research.google.com/drive/1DVjl1v-wgQgWWtIyfE_bkCAdiVVjqJuW) |
| 03A.02 | [`03A.02_comparacao_modelos_gradient_boosting.ipynb`](notebooks/03A.02_comparacao_modelos_gradient_boosting.ipynb) | MLP versus XGBoost | GBRT/XGBoost; *walk-forward* com janela expansiva (5 folds); *early stopping*; *sanity checks*; importância por *gain* | [Abrir relatório](outputs/reports/relatorio_modelagem_preditiva_03A02.md) | [Abrir no Colab](https://colab.research.google.com/drive/1BRbZkilK4omkxV7QjMbx3uPYkI7acsNY) |
| 03A.03 | [`03A.03_otimizacao_pareada_xgboost.ipynb`](notebooks/03A.03_otimizacao_pareada_xgboost.ipynb) | Otimização pareada de XGBoost | *Random Search* (`ParameterSampler`); 30 configurações A/B × 5 folds; desenho pareado; *final refit*; sem *early stopping* na busca | [Abrir relatório](outputs/reports/relatorio_modelagem_preditiva_03A03.md) | [Abrir no Colab](https://colab.research.google.com/drive/1wbDqQxBoOi4qURULPh9EFTnNXpFUhgYj) |
| 03A.04 | [`03A.04_volume_dados_generalizacao_temporal_iatan.ipynb`](notebooks/03A.04_volume_dados_generalizacao_temporal_iatan.ipynb) | Histórico e generalização temporal | *Backtesting* com janelas de 1, 2, 3, 5 e 10 anos; validação entre anos; análise de *drift*; comparação pareada de histórico | [Abrir relatório](outputs/reports/03A04_relatorio_valor_preditivo_historico.md) | [Abrir no Colab](https://colab.research.google.com/drive/1AvnuJ-wPYravlkuZ1C0_-TWD80VWrz4m) |
| 03A.05 | [`03A.05_trajetoria_operacional_historico_ampliado.ipynb`](notebooks/03A.05_trajetoria_operacional_historico_ampliado.ipynb) | Trajetória com histórico ampliado | *Temporal feature engineering*; comparação pareada A/B em amostra comum; *early stopping*; *final refit*; análise estratificada de erros | [Abrir relatório](outputs/reports/03A05_relatorio_trajetoria_operacional_historico_ampliado.md) | [Abrir no Colab](https://colab.research.google.com/drive/1e3QA1-eq5hdaynapAQqBNFdqBlW4grJY) |

## Reprodução e auditoria concluídas em 24/10/2026

Os notebooks 03A.04 e 03A.05 foram executados integralmente após as correções de leitura e sintaxe. Os sete CSVs centrais coincidiram byte a byte com as referências históricas. O ambiente, os hashes e a auditoria de monitoramento de 2011 a 2025 estão em [Reprodução dos experimentos](reproducibility/README.md). Essa verificação abrange as duas etapas finais e preserva as limitações do delineamento descritas no artigo.

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

A sequência experimental do **Trabalho 2** está concluída no **Notebook 03A.05**. Ela compreende MLP, XGBoost, validação temporal, busca pareada de hiperparâmetros, avaliação do volume histórico e análise do ganho das informações de trajetória operacional por regime. Não se declara um modelo universalmente ótimo.

## Fundamentação dos métodos e referências

Os oito notebooks, da seleção da unidade até 03A.05, incluem notas metodológicas, comentários junto das etapas principais e referências completas. O [guia de fundamentação metodológica](docs/fundamentacao_metodologica.md) relaciona os procedimentos às publicações científicas ou documentações oficiais que os sustentam e identifica as escolhas próprias do estudo.

A revisão documental de 24 de outubro de 2026 explicita as fontes de retropropagação, ReLU, Adam, gradient boosting, XGBoost, busca aleatória, PCA, IQR, normalização e avaliação temporal. As arquiteturas, os hiperparâmetros, os períodos, as regras operacionais e os limiares pertencem ao protocolo do projeto. As referências não são apresentadas como origem de decisões que não prescrevem.

Essa atualização preserva as instruções executáveis e as saídas dos notebooks. Ela não representa nova execução dos oito experimentos. A reprodução integral já documentada permanece restrita a 03A.04 e 03A.05, conforme o [guia de reprodução](reproducibility/README.md).

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

**Procedimentos metodológicos empregados.** Aprendizado supervisionado para regressão (*supervised regression*) com uma rede neural artificial *feedforward* do tipo **Multilayer Perceptron (MLP)**, composta por duas camadas ocultas densas (64 e 32 neurônios, ReLU) e saída linear. O treinamento utilizou **Mean Squared Error (MSE)**, retropropagação executada pelo TensorFlow/Keras e otimizador **Adam**, com **EarlyStopping** monitorando a validação e recuperação dos melhores pesos. A comparação A versus B seguiu um **desenho controlado de conjuntos de atributos** (*controlled feature-set comparison*), com normalização **Min–Max ajustada somente no treino** e **temporal holdout** cronológico (treino, validação e teste). A avaliação fora da amostra empregou **MAE, RMSE e R²**, complementados por erros estratificados em startups e rampas intensas (P90 calculado no treino). Essa etapa **não** empregou validação *walk-forward* nem busca de hiperparâmetros.

**Documentação:** [Notebook 03A](notebooks/03A_modelagem_preditiva_co2.ipynb) · [Relatório metodológico e resultados 03A](outputs/reports/relatorio_modelagem_preditiva_3A.md).


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

**Procedimentos metodológicos empregados.** **Engenharia de atributos temporais** (*temporal feature engineering*), com **variáveis defasadas** (*lagged features*, implementadas com `shift(n)`), **estatísticas de janelas móveis** (*rolling-window features*) e representação de direção, aceleração, startups e estados operacionais. O uso de `shift(1)` antes das janelas retrospectivas foi adotado para **prevenir *look-ahead bias***. Realizou-se **comparação controlada de atributos** (*controlled feature-set comparison*) entre B e C, mantendo a arquitetura MLP, Adam, MSE, *EarlyStopping* e a partição de **temporal holdout**; a equivalência completa das amostras entre notebooks não é presumida. A comparação incluiu **MAE, RMSE, R², viés e diagnósticos por contexto**, além de um diagnóstico **descritivo** de *distribution shift* e risco de extrapolação. Não se realizou teste formal de *concept drift* ou *covariate shift*.

**Documentação:** [Notebook 03A.01](notebooks/03A.01_modelagem_preditiva_co2.ipynb) · [Relatório metodológico e resultados 03A.01](outputs/reports/relatorio_modelagem_preditiva_03A01.md).


O Cenário C ampliou a representação temporal mantendo a mesma família MLP.

Resultados principais:

- MAE B: **61,61**;
- MAE C: **62,65**;
- melhora de C em startups: **22,67%** em relação a B;
- melhora de C em rampas intensas: **1,33%**.

O aumento do número de variáveis temporais não produziu melhora global consistente.

## Notebook 03A.02: comparação com XGBoost

**Procedimentos metodológicos empregados.** Substituição da família MLP por **Extreme Gradient Boosting (XGBoost)**, um conjunto sequencial de **árvores de regressão por *gradient boosting*** (*GBRT*), com comparação dos conjuntos de atributos A (1), B (7) e C (24). Aplicou-se **validação cruzada temporal *walk-forward* com janela de treinamento expansiva** (*expanding-window time-series cross-validation*) em **cinco folds cronológicos**, além de avaliação em *holdout* histórico de 2025. O **early stopping** selecionou a complexidade efetiva das árvores por validação; **não houve *Random Search* nesta etapa**. A comparação controlada **MLP versus XGBoost** separou o efeito da família de algoritmo do efeito dos atributos. Os **sanity checks** avaliaram a integridade das variáveis, o alinhamento das observações e a ausência de sobreposição temporal; calculou-se importância das variáveis por ***gain*** (não SHAP nem efeito causal).

**Documentação:** [Notebook 03A.02](notebooks/03A.02_comparacao_modelos_gradient_boosting.ipynb) · [Relatório metodológico e resultados 03A.02](outputs/reports/relatorio_modelagem_preditiva_03A02.md).


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

**Procedimentos metodológicos empregados.** **Busca aleatória de hiperparâmetros** (*Random Search*) com `ParameterSampler` e semente 42: **30 configurações candidatas**, aplicadas tanto ao Cenário A quanto ao B nos **mesmos cinco folds *walk-forward* com janela expansiva**, totalizando **300 ajustes**. O **desenho experimental pareado** (*paired experimental design*) manteve observações, configurações candidatas, folds e métrica primária de seleção (**MAE médio**) comparáveis, embora cada cenário pudesse selecionar uma configuração final diferente. Nesta busca, **`n_estimators` foi hiperparâmetro explícito, sem *early stopping***. Após a seleção, realizou-se **reajuste final** (*final refit*) no período de desenvolvimento e avaliação no *holdout* histórico de novembro e dezembro de 2025, com diagnóstico estratificado por startups e rampas intensas. O desenho não constitui teste formal de significância nem demonstra superioridade causal.

**Documentação:** [Notebook 03A.03](notebooks/03A.03_otimizacao_pareada_xgboost.ipynb) · [Relatório metodológico e resultados 03A.03](outputs/reports/relatorio_modelagem_preditiva_03A03.md).


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

## Notebook 03A.04: histórico ampliado e generalização temporal

**Procedimentos metodológicos empregados.** O Cenário A utiliza **aprendizado supervisionado para regressão** com **Extreme Gradient Boosting (XGBoost)**, da família *gradient-boosted regression trees (GBRT)*, tendo a carga elétrica instantânea como única variável preditora. A etapa começa pela **auditoria e delimitação da amostra histórica por indicadores operacionais**, com 2011–2022 como período principal e 2023–2024 identificados como **regimes operacionais distintos** a partir de horas em operação, distribuição da carga e startups. Trata-se de **caracterização descritiva de *process drift*** e de diagnóstico de **possível *concept drift***, não de detecção estatística formal de mudança na relação carga–emissão.

A avaliação do volume histórico emprega ***rolling-origin temporal backtesting with multiple training-window lengths***: anos-alvo de **2021 a 2025**, com **janelas retrospectivas de 1, 2, 3, 5 e 10 anos**, comparação de erros entre anos e seleção de complexidade por ***early stopping*** em validação cronológica. As janelas possuem extensões alternativas predefinidas; **não** correspondem todas a uma única janela de treinamento expansiva. O protocolo também inclui **teste de generalização *out-of-time*** (treino em 2011–2022, avaliação em 2025), **reajuste final (*final refit*)** após a seleção do número de árvores e **experimento controlado e pareado de disponibilidade do histórico** (*paired controlled experiment on training-history availability*), comparando janeiro–outubro de 2025 com 2011–2022 acrescido do mesmo período recente. São calculados **MAE, RMSE, R², NMAE, bias e diferenças horárias de erro**. Novembro e dezembro de 2025 são *holdout* temporal da comparação, mas não avaliação inteiramente cega do conjunto da pesquisa.

**Documentação:** [Notebook 03A.04](notebooks/03A.04_volume_dados_generalizacao_temporal_iatan.ipynb) · [Relatório de delimitação da amostra histórica](outputs/reports/03A04_delimitacao_amostra_historica.md) · [Relatório metodológico e resultados 03A.04](outputs/reports/03A04_relatorio_valor_preditivo_historico.md).


O Notebook 03A.04 ampliou a série da Iatan Unit 2 e avaliou o valor preditivo do histórico para o **Cenário A**, definido por:

`CO₂(t) = f(P(t))`

A delimitação temporal adotada foi:

- **2010:** período parcial de commissioning, excluído da amostra principal;
- **2011–2022:** histórico operacional de referência;
- **2023–2024:** regime operacional distinto, preservado para análises específicas, mas excluído da amostra principal;
- **2025:** período futuro de avaliação.

A delimitação de 2011 a 2022 foi exploratória e consolidada após os backtests, que incluíram avaliação em 2025. Os indicadores operacionais sustentam sua justificativa, sem caracterizar uma escolha independente dos resultados. O detalhamento está em [03A04_delimitacao_amostra_historica.md](outputs/reports/03A04_delimitacao_amostra_historica.md).

### Generalização 2011–2022 para 2025

Treinado exclusivamente com **83.832 observações de 2011 a 2022**, o XGBoost do Cenário A foi avaliado nas **6.249 horas operacionais válidas de 2025**.

| Métrica | Resultado |
|---|---:|
| MAE | 50,2740 |
| RMSE | 68,4650 |
| R² | 0,8894 |
| NMAE | 8,65% |
| Bias | -33,9686 |

O resultado mostra capacidade relevante de transferência temporal, embora com superestimação média e degradação localizada em determinados meses e faixas de carga.

### Valor incremental do histórico

Para verificar se o processamento do histórico acrescenta informação mesmo quando dados recentes de 2025 já estão disponíveis, foi realizado um teste pareado em novembro e dezembro de 2025.

| Modelo | MAE | RMSE | R² | NMAE |
|---|---:|---:|---:|---:|
| Jan–Out/2025 | 23,3470 | 28,5786 | 0,9802 | 3,97% |
| 2011–2022 + Jan–Out/2025 | **20,2454** | **25,1240** | **0,9847** | **3,44%** |

A inclusão do histórico reduziu o MAE em **13,28%** e o RMSE em **12,09%**. O modelo com histórico apresentou menor erro absoluto em **65,30%** das horas do teste.

Assim, o Notebook 03A.04 responde positivamente à questão:

> **O processamento do histórico de 2011 a 2022 acrescenta valor preditivo ao Cenário A?**

**Sim.**

O relatório consolidado está em [03A04_relatorio_valor_preditivo_historico.md](outputs/reports/03A04_relatorio_valor_preditivo_historico.md).

## Arquivos-chave do Notebook 03A.04

Para facilitar a navegação pelos resultados desta etapa:

- [Notebook 03A.04](notebooks/03A.04_volume_dados_generalizacao_temporal_iatan.ipynb)
- [Relatório de delimitação da amostra histórica](outputs/reports/03A04_delimitacao_amostra_historica.md)
- [Relatório do valor preditivo do histórico](outputs/reports/03A04_relatorio_valor_preditivo_historico.md)
- [Tabela de generalização 2011–2022 para 2025](outputs/tables/03A04_generalizacao_2011_2022_para_2025.csv)
- [Comparação pareada: 2025 versus histórico + 2025](outputs/tables/03A04_comparacao_2025_vs_historico_2025.csv)
- [Síntese das evidências do histórico](outputs/tables/03A04_sintese_evidencias_historico.csv)
- [Figura de comparação dos erros](outputs/figures/03A04_comparacao_2025_vs_historico_2025_erros.png)
- [Séries observada e previstas](outputs/figures/03A04_comparacao_2025_vs_historico_2025_series.png)

## Notebook 03A.05: trajetória operacional com histórico ampliado

**Procedimentos metodológicos empregados.** Regressão supervisionada com **XGBoost/GBRT** nos Cenários A (carga instantânea) e B (carga, memória e trajetória operacional), mantendo os **mesmos hiperparâmetros estruturais**. No Cenário B, a ***temporal feature engineering*** utiliza ***lagged features*** (`shift(1)`), ***rolling-window features*** e indicadores de transições operacionais. O agrupamento em ***temporal blocks*** impede que o final de 2022 seja interpretado como imediatamente anterior ao início de 2025, reduzindo o risco de ***look-ahead bias*** e de continuidade temporal artificial. A auditoria de qualidade identificou uma carga ausente em 2019, **preservada sem imputação**, e o tempo desde startup semanticamente desconhecido no início do histórico; as observações não elegíveis foram retiradas igualmente dos dois cenários.

A avaliação segue um ***paired experimental design on a common eligible sample*** (*desenho experimental pareado em amostra comum*): A e B utilizam as mesmas observações, o mesmo alvo e a mesma partição cronológica. O número de árvores é selecionado separadamente por ***early stopping*** em **outubro de 2025** (RMSE de validação; paciência de 50 rodadas), seguido de ***final refit*** com 2011–2022 e janeiro–outubro de 2025. A comparação em **novembro–dezembro de 2025** utiliza ***temporal holdout*** histórico e **análise pareada de erros hora a hora**, incluindo MAE, RMSE, R², NMAE e bias. A ***context-stratified error analysis*** examina startups, **rampas intensas definidas pelo P90 calculado no treino**, demais horas e casos extremos. Esta etapa **não** executa *Random Search*, *walk-forward cross-validation*, teste formal de significância, modelo híbrido ou análise causal; tampouco demonstra previsão antecipada sem conhecimento da carga da própria hora.

**Documentação:** [Notebook 03A.05](notebooks/03A.05_trajetoria_operacional_historico_ampliado.ipynb) · [Relatório metodológico e resultados 03A.05](outputs/reports/03A05_relatorio_trajetoria_operacional_historico_ampliado.md).


O experimento final do Trabalho 2 retomou a comparação entre os modelos XGBoost com **carga instantânea (A)** e com **carga e trajetória operacional (B)**, sob as mesmas observações e o histórico de **2011–2022 + janeiro a outubro de 2025**. A avaliação temporal utilizou novembro e dezembro de 2025 como período de comparação histórica, previamente examinado em outros experimentos do projeto.

| Indicador | Cenário A | Cenário B |
|---|---:|---:|
| MAE (short tons de CO₂ por registro horário) | **20,1514** | 21,1720 |
| NMAE | **3,4240%** | 3,5974% |
| Variação global do MAE de B em relação a A | Referência | **−5,06%** |

Embora B tenha apresentado MAE global maior, houve **redução de 22,90% do MAE nas rampas intensas** e melhora agregada nas primeiras seis horas após startup. Nas demais horas, que predominam no teste, o MAE de B foi aproximadamente **16,03% maior**.

O resultado deve ser interpretado como evidência de **valor preditivo localizado da trajetória operacional**, e não como superioridade global ou prova causal de qualquer variável.

**Artefatos do experimento:** [notebook 03A.05](notebooks/03A.05_trajetoria_operacional_historico_ampliado.ipynb), [relatório completo](outputs/reports/03A05_relatorio_trajetoria_operacional_historico_ampliado.md), [métricas finais](outputs/tables/03A05_resultado_final_A_B.csv), [comparação por contexto](outputs/tables/03A05_comparacao_contextos_operacionais.csv), [síntese das evidências](outputs/tables/03A05_sintese_evidencias_trajetoria_historico.csv), [ganhos por regime](outputs/figures/03A05_ganho_trajetoria_por_contexto.png) e [distribuição dos ganhos horários](outputs/figures/03A05_distribuicao_ganho_horario_B_vs_A.png).

## Trabalho 2: resposta à pergunta de pesquisa

**Pergunta investigada:**

> Em que medida a inclusão de informações sobre estados, memória e trajetória operacional melhora a estimação das emissões horárias de CO₂ em relação ao uso apenas da carga instantânea?

**Resposta a partir dos experimentos 03A a 03A.05:** a inclusão indiscriminada de informações de trajetória **não produziu melhoria global consistente** quando comparada ao uso apenas da carga elétrica, especialmente nos modelos XGBoost e após a ampliação do histórico. Entretanto, essas informações **podem melhorar expressivamente as estimativas em condições dinâmicas específicas**, sobretudo em rampas intensas.

Os resultados também demonstram que a **família de modelo** e a **composição temporal dos dados de treinamento** influenciam o desempenho: no 03A.04, a inclusão do histórico de 2011–2022 ao período recente reduziu o MAE do Cenário A em **13,28%** no teste comparativo de 2025. O desempenho varia entre períodos e regimes, e não foi estabelecida uma quantidade universal de histórico suficiente.

**Conclusão do escopo da disciplina:** a pergunta de pesquisa do Trabalho 2 está respondida com as ressalvas acima. O experimento acadêmico se encerra no **Notebook 03A.05**. Não se assume a otimização adicional, nem a seleção definitiva de uma arquitetura como requisito deste trabalho.

## Limitações e hipóteses para estudos futuros

As evidências foram obtidas para a **Iatan Unit 2**, em condições operacionais e períodos determinados. O uso da carga da própria hora caracteriza uma **estimativa de emissões condicionada à carga conhecida**, não necessariamente uma previsão antecipada quando a carga futura é desconhecida. O período de novembro e dezembro de 2025 foi utilizado como comparação histórica, e não como teste completamente cego em relação ao conjunto da pesquisa.

Como **possibilidades de investigação futura, sem constituírem compromissos de execução neste trabalho**, destacam-se: a suficiência e a recência do histórico para diferentes regimes; estratégias de predição específicas para condições transitórias; a estabilidade temporal em períodos com comportamento operacional distinto; e a aplicabilidade a outras unidades físicas.

Essas hipóteses não alteram nem ampliam o escopo experimental já concluído.

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
│   ├── 03A.03_otimizacao_pareada_xgboost.ipynb
│   ├── 03A.04_volume_dados_generalizacao_temporal_iatan.ipynb
│   └── 03A.05_trajetoria_operacional_historico_ampliado.ipynb
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

## Verificação da aplicação dos métodos

As técnicas citadas foram conferidas por confronto com as fontes, extração das funções dos notebooks, cálculos independentes e consulta aos modelos e resultados preservados. O [relatório técnico e os scripts](reproducibility/methods/README.md) registram cada verificação e suas condições. Também foram corrigidas as alegações de suficiência de 30 configurações, de isolamento exclusivo dos efeitos e de independência global do teste.
