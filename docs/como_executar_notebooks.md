# Executar os notebooks

## Colab

1. Use os links **Colab** no [índice de notebooks](../notebooks/README.md), seguindo a ordem dos 11 notebooks.
2. Mantenha em Meu Drive a pasta `co2-cems-thermal-modeling`, com `notebooks/`, `scripts/`, `pipeline/` e os insumos de `data/`. Os arquivos estão no [Drive do projeto](https://drive.google.com/drive/folders/1ONZBhbSfVpuN9TNTstsAmCQSZBZKv0l9).
3. Execute a primeira célula e permita a conexão ao Drive. A raiz é localizada automaticamente; para outra pasta, defina `CO2_PROJECT_ROOT` antes dessa célula.
4. Nas etapas de aquisição, configure `EPA_API_KEY` em **Segredos** no Colab e permita seu uso pelo notebook. A chave também pode ser fornecida como variável de ambiente.
5. Execute as células na ordem. Uma sessão CPU é suficiente. As versões estão fixadas em `constraints.txt`, aplicado por `requirements.txt`. Para instalar as dependências após localizar a raiz, use uma célula com:

```python
%cd "{project_root()}"
%pip install -r requirements.txt
```

## Insumos

Os Parquets volumosos ficam no Drive e não integram o download do GitHub. Preserve a estrutura de pastas:

- `pipeline/selected_unit.json` e os arquivos de seleção/tratamento produzidos pelas primeiras etapas;
- `data/interim/03A04_multiyear/iatan_unit2_YYYY.parquet`, arquivos anuais utilizados na análise histórica;
- `data/interim/03A05_trajectory_history/`, com as amostras comuns, partições e previsões de 03A.05.

O 5A utiliza os insumos do 5. O 5B utiliza as previsões pareadas do 5 e do 5A. O 5C utiliza as partições comuns do 5. Verifique os caminhos indicados nas primeiras células de cada complemento antes de iniciar.

As saídas científicas existentes estão em `outputs/tables/`, `outputs/figures/` e `outputs/03A05A/`, `outputs/03A05B/`, `outputs/03A05C/`. Os notebooks também exibem os resultados salvos. Abrir um notebook não executa suas células.

## Execução local

Instale as dependências com `python -m pip install -r requirements.txt` e abra os notebooks dentro da pasta do projeto, mantendo os mesmos insumos relativos. A primeira célula localiza a raiz sem montar o Drive. `CO2_PROJECT_ROOT` permite indicar outra localização; `EPA_API_KEY` fornece a chave para consultas à EPA.
