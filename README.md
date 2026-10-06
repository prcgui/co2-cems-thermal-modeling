# CO₂ CEMS Thermal Modeling

[![Open Notebook 1 in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/01_selecao_unidade_estudo.ipynb)
[![Open Notebook 2 in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/02_tratamento_dados.ipynb)

Preparação e análise de dados operacionais para futura modelagem de emissões horárias de CO₂ em unidade termelétrica a carvão, utilizando dados públicos da U.S. EPA e técnicas de pré-processamento e redução de dimensionalidade trabalhadas na disciplina **EQM2118 – Modelagem Matemática com Aplicação de Inteligência Artificial**.

## Apresentação do Trabalho

A apresentação em vídeo do **Trabalho 1** está disponível no YouTube.

[![Assistir à apresentação no YouTube](https://img.youtube.com/vi/EUEqmm9nRHQ/hqdefault.jpg)](https://youtu.be/EUEqmm9nRHQ)

▶ **[Assistir à apresentação no YouTube](https://youtu.be/EUEqmm9nRHQ)**

## Executar o projeto

Os arquivos `.ipynb` são notebooks executáveis. No GitHub eles são exibidos de forma estática; para executar as células, utilize os botões **Open in Colab** acima.

A execução deve seguir a ordem:

1. **Notebook 1 — seleção da unidade de estudo**: consulta os dados da EPA, executa o processo de seleção e gera os artefatos necessários para a etapa seguinte;
2. **Notebook 2 — tratamento e preparação dos dados**: carrega automaticamente a unidade selecionada e os dados horários produzidos pelo Notebook 1.

O Notebook 1 utiliza uma chave da API da EPA armazenada como segredo do Google Colab com o nome `EPA_API_KEY`. A chave não é armazenada no repositório.

Os notebooks utilizam o Google Drive como área persistente de trabalho, na pasta:

```text
/content/drive/MyDrive/co2-cems-thermal-modeling
```

Como os arquivos horários e intermediários podem ser volumosos, eles não são versionados no GitHub. Por isso, para reproduzir integralmente o fluxo em uma nova conta do Google Drive, recomenda-se executar primeiro o Notebook 1 e, em seguida, o Notebook 2.

Para execução local, as principais dependências estão registradas em [`requirements.txt`](requirements.txt):

```bash
pip install -r requirements.txt
```

## Contexto do projeto

O projeto investiga se a inclusão de informações sobre **estado e trajetória operacional** de uma unidade termelétrica pode melhorar, em etapas futuras, a estimação de suas emissões horárias de CO₂ em comparação com uma abordagem baseada apenas na carga elétrica instantânea.

A questão de pesquisa adotada é:

> **Em que medida a inclusão de informações sobre estados e transições operacionais melhora a estimação das emissões horárias de CO₂ de uma unidade termelétrica a carvão em relação ao uso apenas da carga atual?**

Nesta fase, correspondente ao **Trabalho 1**, o foco está na análise crítica da base de dados, seleção da unidade de estudo, tratamento dos dados, engenharia de atributos, análise exploratória por PCA e preparação do conjunto experimental. O treinamento dos modelos de inteligência artificial será realizado em etapa posterior.

## Fonte dos dados

Os dados são provenientes da **U.S. Environmental Protection Agency (EPA)**, a partir de dados horários de monitoramento contínuo de emissões (CEMS/CAMPD).

O período considerado é o ano de **2025**, com resolução horária.

Os arquivos brutos e intermediários de grande volume não são versionados neste repositório. O código necessário para seleção, tratamento e análise permanece documentado nos notebooks.

## Seleção da unidade de estudo

A seleção partiu de uma população ampla de unidades termelétricas a carvão e aplicou critérios sucessivos de elegibilidade estrutural, disponibilidade de dados, cobertura de monitoramento, qualidade da série horária e comportamento operacional.

A unidade selecionada foi:

- **Facility:** Iatan
- **Facility ID:** 6065
- **Unit:** 2
- **Estado:** Missouri (MO)
- **Ano:** 2025
- **Registros horários:** 8.760

A Iatan Unit 2 foi escolhida por apresentar boa qualidade dos dados, número relevante de transições operacionais, ampla faixa de carga e variabilidade suficiente para investigar efeitos de estados e trajetórias operacionais.

O processo completo está documentado em:

- [`notebooks/01_selecao_unidade_estudo.ipynb`](notebooks/01_selecao_unidade_estudo.ipynb)
- [`outputs/reports/relatorio_selecao_unidade.md`](outputs/reports/relatorio_selecao_unidade.md)

## Tratamento e preparação dos dados

O segundo notebook realiza a preparação da série da unidade selecionada.

As principais etapas foram:

1. auditoria estrutural e temporal da base;
2. análise e tratamento de dados faltantes;
3. detecção exploratória de outliers;
4. engenharia de atributos orientada ao processo;
5. análise de componentes principais (PCA);
6. definição da base experimental;
7. divisão temporal em treino, validação e teste;
8. normalização Min–Max.

O processo completo está documentado em:

- [`notebooks/02_tratamento_dados.ipynb`](notebooks/02_tratamento_dados.ipynb)
- [`outputs/reports/relatorio_tratamento_dados.md`](outputs/reports/relatorio_tratamento_dados.md)

## Qualidade dos dados

A série selecionada contém 8.760 registros horários e cobre integralmente o ano de 2025.

Na auditoria foram observados:

- ausência de timestamps duplicados;
- ausência de lacunas na sequência horária;
- ausência de dados faltantes de carga ou CO₂ durante a operação;
- 6.249 horas operacionais;
- 2.511 horas com a unidade desligada;
- 77 horas de operação parcial.

Os valores ausentes de carga e CO₂ nas horas OFF foram preservados nas variáveis originais e representados como zero apenas em novas variáveis tratadas, destinadas às etapas posteriores de análise e modelagem.

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

No período analisado foram identificados **38 startups** e **37 shutdowns**.

Nenhuma variável derivada de CO₂ foi utilizada como atributo preditivo, evitando vazamento da variável-alvo.

## Análise de outliers

A detecção exploratória de outliers foi realizada pelo método do **intervalo interquartil (IQR)** somente durante as horas operacionais.

Foram encontrados:

- **0 outliers de carga**;
- **3 outliers de CO₂**, equivalentes a aproximadamente 0,05% das horas operacionais.

Os registros não foram removidos automaticamente. Em processos industriais, valores estatisticamente extremos podem corresponder a regimes operacionais reais e, portanto, devem ser avaliados em conjunto com o contexto físico do processo.

## PCA exploratória

A **Análise de Componentes Principais (PCA)** foi aplicada a sete variáveis operacionais com o objetivo de investigar redundância e potencial de redução de dimensionalidade.

A variância explicada foi aproximadamente:

| Componente | Variância explicada | Variância acumulada |
|---|---:|---:|
| PC1 | 44,07% | 44,07% |
| PC2 | 16,51% | 60,57% |
| PC3 | 14,15% | 74,72% |
| PC4 | 13,27% | 87,99% |
| PC5 | 11,66% | 99,65% |

Foram necessárias **cinco componentes para superar 90% da variância**, de modo que a redução dimensional foi considerada relativamente pequena frente à perda de interpretabilidade física das variáveis originais.

Os loadings mostraram ainda uma interpretação operacional consistente:

- **PC1:** predominantemente associada ao nível de carga;
- **PC2:** predominantemente associada à dinâmica e às rampas de carga.

A PCA foi, portanto, mantida como ferramenta exploratória e não como substituta das features originais.

## Decisões metodológicas

Nem todas as técnicas estudadas foram aplicadas automaticamente. A escolha foi condicionada à natureza do problema e dos dados.

| Técnica | Decisão | Justificativa |
|---|---|---|
| Tratamento de faltantes | Aplicado | Ausências estruturais associadas ao estado OFF |
| Interpolação por spline | Não aplicada | Não existem lacunas durante a operação |
| Detecção de outliers por IQR | Aplicada | Diagnóstico de valores extremos sem remoção automática |
| Feature engineering | Aplicada | Necessária para representar estados e trajetórias operacionais |
| PCA | Aplicada de forma exploratória | Avaliação de redundância e redução de dimensionalidade |
| SMOTE | Não aplicado | O problema futuro é de regressão, não de classificação |
| Divisão aleatória treino/teste | Não aplicada | A ordem temporal deve ser preservada |
| Normalização Min–Max | Aplicada | Preparação para modelos sensíveis à escala |

## Preparação experimental

A base destinada à futura modelagem considera apenas as horas em que a unidade está operando.

A separação temporal foi definida como:

- **Treino:** janeiro a setembro de 2025 — 4.894 observações;
- **Validação:** outubro de 2025 — 211 observações;
- **Teste:** novembro e dezembro de 2025 — 1.144 observações.

O `MinMaxScaler` é ajustado somente sobre o conjunto de treino e posteriormente aplicado aos períodos de validação e teste, evitando data leakage.

## Estrutura do repositório

```text
co2-cems-thermal-modeling/
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   ├── 01_selecao_unidade_estudo.ipynb
│   └── 02_tratamento_dados.ipynb
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── pipeline/
│   └── selected_unit.json
└── outputs/
    ├── reports/
    │   ├── relatorio_selecao_unidade.md
    │   └── relatorio_tratamento_dados.md
    ├── figures/
    ├── tables/
    └── presentations/
        └── README.md
```

Os diretórios de dados permanecem sem arquivos pesados no GitHub por opção de versionamento. O arquivo `.gitignore` impede o envio acidental de dados brutos, arquivos intermediários e credenciais.

## Próximas etapas

A fase seguinte do projeto deverá desenvolver e avaliar modelos de regressão para estimar as emissões horárias de CO₂.

A comparação experimental será estruturada de modo a investigar o ganho obtido ao passar de uma representação baseada apenas na carga instantânea para outra que incorpore informações sobre trajetória e estado operacional.

As métricas previstas para avaliação incluem **MAE, RMSE e R²**, sempre respeitando a separação temporal dos dados.

## Autores

- Guilherme Pereira Rodrigues da Costa
- Felipe Calmon
- Thiago Menezes

## Disciplina

**EQM2118 – Modelagem Matemática com Aplicação de Inteligência Artificial**  
Professor: **Brunno Ferreira dos Santos**  
PUC-Rio
