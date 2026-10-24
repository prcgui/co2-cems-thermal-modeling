# Reprodução dos experimentos históricos e auditoria do monitoramento

Em 24 de outubro de 2026, os notebooks 03A.04 e 03A.05 foram executados integralmente, em sequência, com um kernel novo para cada notebook e os arquivos anuais originais preservados. As dez células de código de cada notebook terminaram sem erro. Esta reprodução abrange essas duas etapas. A seleção inicial, o tratamento e as etapas com MLP e busca de hiperparâmetros anteriores não foram novamente executados.

## Correções e resultados

A leitura de 03A.04 passou a selecionar explicitamente os 16 arquivos anuais de 2010 a 2025. O consolidado existente deixa de ser lido como se fosse outro ano. Cada arquivo é validado quanto a unidade, ano, identidade do timestamp, calendário completo e duplicatas. O programa interrompe a execução se houver inconsistência, sem remover silenciosamente linhas. A série consolidada corrigida contém **133.704 registros únicos**, entre 1º de outubro de 2010 e 31 de dezembro de 2025. O consolidado posterior que motivou a correção continha 267.408 linhas, das quais 133.704 duplicadas.

No 03A.05, foi removido o prefixo inválido `3a#`. Também foram fortalecidas as verificações dos arquivos anuais. A célula redundante de relatório no 03A.04 foi removida e a geração do relatório foi mantida após suas dependências. O texto do relatório foi corrigido para reconhecer que a delimitação de 2011 a 2022 foi exploratória, após backtests que incluíram 2025. Os atributos, períodos, hiperparâmetros, sementes e procedimentos de ajuste dos modelos foram preservados.

| Evidência | Resultado da reprodução |
|---|---|
| Sete CSVs de referência | Mesmo SHA-256, portanto identidade byte a byte |
| Três tabelas de previsões de 03A.05 | Valores e tipos exatamente iguais após alinhamento por timestamp; 211, 1.144 e 1.144 registros |
| Seis bases e amostras de 03A.05 | Valores, tipos e ordem exatamente iguais aos originais |
| Dezesseis arquivos anuais de entrada | SHA-256 inalterados |
| MAE com acréscimo do histórico | 23,3469868140 para 20,2453520822; redução de 13,2849466% |
| MAE final em amostra comum | A: 20,1514190054; B: 21,1719865784 |
| MAE nas 258 horas de rampas intensas | A: 24,0577; B: 18,5491; redução de 22,90% |

Os nove Parquets de 03A.05 têm bytes diferentes dos originais preservados, embora seus valores, tipos, colunas e ordenação sejam exatamente iguais. A igualdade binária declarada nesta documentação refere-se aos sete CSVs e aos arquivos anuais de entrada. Os arquivos derivados de 03A.04 foram reconstruídos a partir dos anuais, corrigindo as duplicações anteriores.

## Ambiente e execução

O ambiente verificado usa Linux x86_64 e Python 3.12.14, com XGBoost 3.4.1, pandas 2.2.3, NumPy 2.3.5 e scikit-learn 1.8.0. O arquivo `requirements-reproduction.lock` fixa todas as distribuições instaladas nesta reprodução. Ele documenta o ambiente efetivamente utilizado agora, sem afirmar reconstrução integral do ambiente original do Colab. O comando `pip check` terminou sem dependências incompatíveis. TensorFlow está incluído para as dependências do projeto, mas os experimentos com MLP não foram repetidos nesta verificação.

Na raiz do projeto, crie um ambiente com a versão de Python indicada:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-reproduction.lock
python -m pip check
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python scripts/reproduce_history.py
```

Antes da execução, restaure `pipeline/selected_unit.json` e os 16 arquivos `data/interim/03A04_multiyear/iatan_unit2_YYYY.parquet` do pacote preservado do projeto. Os hashes esperados estão em [input_manifest.json](../outputs/reproducibility/input_manifest.json). Esses dados permanecem fora do versionamento Git. Uma nova consulta à EPA pode fornecer uma versão posterior dos dados e deve ser registrada como nova aquisição.

O runner usa a raiz do próprio repositório e configura `CO2_PROJECT_ROOT` para os notebooks. Em execução manual local, defina essa variável com o caminho da raiz antes de abrir o notebook. Quando ela não está definida, mantém-se o fluxo de montagem do Google Drive no Colab. Com os anuais válidos já presentes, a leitura ocorre sem acesso à API da EPA. Se faltar um ano, a aquisição do notebook exige uma chave fornecida legitimamente como `EPA_API_KEY` ou segredo do Colab; nenhuma chave integra os artefatos.

As quatro variáveis de threads do comando limitam a concorrência das bibliotecas nesta execução e estão registradas em environment.json. Elas evitam contenção em máquinas compartilhadas; os hiperparâmetros dos notebooks permanecem inalterados.

Cada notebook inicia com saídas limpas em memória e um kernel independente. O arquivo executado somente substitui a cópia de trabalho após a conclusão de todas as suas células. O runner verifica os hashes dos insumos antes e depois e registra ambiente, duração, hash do código, outputs e comparação dos resultados. Os tempos registrados descrevem esta máquina e não constituem um benchmark de desempenho.

## Evidências verificáveis

- [execution_summary.json](../outputs/reproducibility/execution_summary.json): conclusão e escopo de cada execução.
- [environment.json](../outputs/reproducibility/environment.json): versões observadas do interpretador e dos pacotes.
- [input_manifest.json](../outputs/reproducibility/input_manifest.json): integridade dos 17 insumos necessários.
- [output_manifest.json](../outputs/reproducibility/output_manifest.json): hashes dos resultados gerados.
- [reference_comparison.json](../outputs/reproducibility/reference_comparison.json): comparações dos sete CSVs.
- [independent_validation.json](../outputs/reproducibility/independent_validation.json): conferência independente das previsões, amostras, calendário e preservação dos parâmetros científicos.
- [baselines](baselines): cópias imutáveis dos sete CSVs usados como referência.
- [monitoring](monitoring): auditoria histórica dos indicadores e da configuração de monitoramento.

As três referências de 03A.04 provêm do commit [029a68ef63aa7aee0d15db504b25c9f1da85d5be](https://github.com/prcgui/co2-cems-thermal-modeling/tree/029a68ef63aa7aee0d15db504b25c9f1da85d5be). As quatro referências de 03A.05 provêm de [ed9d409fbf7805e0bbc9fe1fa1ac944cc1e4c8f4](https://github.com/prcgui/co2-cems-thermal-modeling/tree/ed9d409fbf7805e0bbc9fe1fa1ac944cc1e4c8f4). A comparação admite tolerância absoluta de 10⁻⁶ e relativa de 10⁻⁸, mas todas as diferenças observadas foram zero e os hashes dos sete CSVs coincidiram.

## Monitoramento e interpretação

A auditoria dos 15 anos completos, de 2011 a 2025, cobre 131.496 registros de calendário e 98.799 horas ON. São 98.261 horas `Measured`, 425 `Measured and Substitute` e 113 `Substitute`. Em 2025, as 6.249 horas ON incluem 6.209 `Measured` e 40 `Measured and Substitute`. O filtro original de seleção utilizou `contains("measured")`, incluindo as duas primeiras categorias. A proporção estritamente `Measured` é 99,359898% em 2025, enquanto a proporção com participação de medição é 100%. Essa distinção esclarece o critério aplicado, sem refazer a seleção de unidades.

O método CO2/CEM está documentado desde 1º de outubro de 2010, com cobertura declarada de todo o período auditado. Os planos registram mudanças no registrador em 2017, no DAHS em 2018 e no analisador e na sonda de CO2 em 2024. As fontes são dois snapshots posteriores que contêm vigências históricas, e não quinze versões preservadas ano a ano. A continuidade declarada do método não implica ausência de incerteza ou homogeneidade instrumental. O relatório de auditoria separa esses achados de qualquer hipótese sobre seu efeito nos modelos.

## Limites preservados

A reprodução resolve as falhas de execução e a rastreabilidade dos resultados históricos e finais. Permanecem características do delineamento: estudo de uma unidade, seleção retrospectiva, delimitação histórica exploratória, reutilização do teste durante o desenvolvimento, uma semente por configuração e ausência de intervalos de confiança que considerem dependência temporal. A conferência não transforma a análise descritiva em evidência causal nem demonstra generalização para outras plantas.

## Primeira atualização documental de 24 de outubro de 2026

Na primeira atualização, as oito versões dos notebooks receberam referências e comentários metodológicos. A [matriz de fundamentação](../docs/fundamentacao_metodologica.md) explicita o alcance das fontes e as decisões do protocolo. Foram comparadas as árvores sintáticas das células Python antes e depois da atualização e as saídas armazenadas; ambas permaneceram iguais em cada repositório.

Os hashes de código e de notebook presentes nos registros de execução anteriores identificam as versões efetivamente executadas naquela reprodução. Naquela etapa, a inclusão de comentários e células Markdown modificou o hash integral dos arquivos, sem modificar as instruções computacionais. A [verificação desta atualização documental](../outputs/reproducibility/documentation_update_2026-10-24.json) registra essa correspondência. Os registros anteriores de execução e os dados e resultados científicos foram preservados.

## Verificação da aplicação dos métodos

As técnicas citadas foram conferidas por confronto com as fontes, extração das funções dos notebooks, cálculos independentes e consulta aos modelos e resultados preservados. O [relatório técnico e os scripts](methods/README.md) registram cada verificação e suas condições. Também foram corrigidas as alegações de suficiência de 30 configurações, de isolamento exclusivo dos efeitos e de independência global do teste.

A verificação posterior corrigiu também a borda final de faixas de carga no diagnóstico de 03A.04. Esta é a única alteração de cálculo nesta revisão e não muda os resultados do recorte observado. O registro anterior de atualização documental descreve sua própria versão; o [registro das correções posteriores](../outputs/reproducibility/methods/corrections_manifest.json) identifica a nova mudança.
