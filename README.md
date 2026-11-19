# Estimação de emissões horárias de CO₂

Projeto da disciplina **EQM2118 — Modelagem Matemática com Aplicação de Inteligência Artificial**. Estudo da **Iatan Unit 2** (EPA Facility ID 6065, Missouri), com dados horários públicos CEMS/CAMPD da U.S. EPA e modelos MLP e XGBoost.

[Ler o artigo](artigo/README.md)

## Apresentação

[Assistir à apresentação do Trabalho 1 no YouTube](https://youtu.be/EUEqmm9nRHQ)

## Conteúdo

- [Notebooks](notebooks/README.md): sequência das 11 etapas e links para executar no Colab.
- [Metodologia](docs/metodologia.md): dados, representações, protocolos e limites do estudo.
- [Resultados](outputs/README.md): síntese das comparações, tabelas, figuras e modelos.
- [Referências](references/README.md): fontes científicas e documentação dos dados.

## Execução

Siga a ordem dos notebooks. No Colab, conecte o Drive com a pasta do projeto e os insumos; para consultas à EPA, configure o segredo `EPA_API_KEY`. Os arquivos volumosos de entrada permanecem no [Drive do projeto](https://drive.google.com/drive/folders/1ONZBhbSfVpuN9TNTstsAmCQSZBZKv0l9).

Para executar localmente: `python -m pip install -r requirements.txt`. Consulte o [guia de execução](docs/como_executar_notebooks.md) para organizar os insumos.
