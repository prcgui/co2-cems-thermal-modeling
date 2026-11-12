# Execução dos notebooks

## Abrir pelo GitHub no Colab

Abra o notebook da etapa desejada pelo link abaixo. A primeira célula conecta o Drive e localiza a pasta `co2-cems-thermal-modeling` em Meu Drive. A pasta precisa conter `scripts/publication.py`, `pipeline/`, os notebooks e os insumos preservados. Se o Drive já estiver montado, a conexão é reutilizada.

Para uma pasta diferente, defina `CO2_PROJECT_ROOT` antes de executar a primeira célula. Essa configuração é usada apenas durante a sessão; os registros públicos usam caminhos relativos.

Nas etapas que consultam a EPA, configure o segredo `EPA_API_KEY` no painel de chaves do Colab e permita seu uso pelo notebook. A mesma chave pode ser fornecida como variável de ambiente em uma execução local. O código não grava a chave nos resultados.

## Ordem dos arquivos

1. [01_selecao_unidade_estudo.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/01_selecao_unidade_estudo.ipynb)
2. [02_tratamento_dados.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/02_tratamento_dados.ipynb)
3. [03A_modelagem_preditiva_co2.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/03A_modelagem_preditiva_co2.ipynb)
4. [03A.01_modelagem_preditiva_co2.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/03A.01_modelagem_preditiva_co2.ipynb)
5. [03A.02_comparacao_modelos_gradient_boosting.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/03A.02_comparacao_modelos_gradient_boosting.ipynb)
6. [03A.03_otimizacao_pareada_xgboost.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/03A.03_otimizacao_pareada_xgboost.ipynb)
7. [03A.04_volume_dados_generalizacao_temporal_iatan.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/03A.04_volume_dados_generalizacao_temporal_iatan.ipynb)
8. [03A.05_trajetoria_operacional_historico_ampliado.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/03A.05_trajetoria_operacional_historico_ampliado.ipynb)
9. [03A_05A_ablacao_controlada_features.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/03A_05A_ablacao_controlada_features.ipynb)
10. [03A_05B_incerteza_pareada_calendario.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/03A_05B_incerteza_pareada_calendario.ipynb)
11. [03A_05C_MLP_XGBoost_sementes_protocolo_comum.ipynb](https://colab.research.google.com/github/prcgui/co2-cems-thermal-modeling/blob/main/notebooks/03A_05C_MLP_XGBoost_sementes_protocolo_comum.ipynb)

Os arquivos 03A.05A, 03A.05B e 03A.05C são complementos. O 5A lê os insumos do 5; o 5B usa as previsões preservadas do 5 e do 5A; o 5C compara as famílias nas mesmas partições. Os insumos volumosos estão no Drive e não são baixados automaticamente do GitHub. Confirme a presença dos arquivos antes de iniciar um ajuste.

## Instalação e resultados

Use uma sessão nova com CPU e execute as células na ordem. O requisito de XGBoost 3.4.1 é verificado pelos complementos. A lista de dependências está em `requirements.txt`; o arquivo de restrições registra as versões da reprodução documentada.

Os notebooks conservam as saídas científicas já verificadas. Abrir um arquivo não refaz o experimento. Ao optar por uma nova execução, salve o notebook com suas saídas no Drive. Os complementos gravam novas subpastas datadas e verificam a identidade dos insumos; não substituem automaticamente os resultados preservados.

## Execução local

Instale as dependências e abra os notebooks a partir da pasta do projeto. A primeira célula localiza a raiz sem montar serviços externos. `CO2_PROJECT_ROOT` também é aceito nesse modo.
