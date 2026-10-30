# Biblioteca de referências da versão revisada em 29/10/2026

Este diretório acompanha a versão atual do artigo e contém o registro das **40 referências do artigo**, complementado pelas fontes específicas dos notebooks.

As referências fornecidas pelo usuário foram conferidas no texto original. Quando uma fonte nova cobria de forma mais direta a mesma afirmação de uma referência temática anterior, a nova fonte foi priorizada. Por esse motivo, F. Liu e Li (2025), Tu et al. (2024) e Zhou et al. (2023) deixaram de integrar a bibliografia final do artigo.

O PDF `10_artigos_emissoes_co2_termeletricas.pdf` é um resumo secundário e não é usado como evidência científica no artigo ou nos notebooks.

## Organização

- `source_registry.csv`: DOI/URL, função da citação, status de auditoria e nome da cópia privada quando fornecida.
- `private_library/`: PDFs fornecidos pelo usuário, preservados no Google Drive privado.
- GitHub público: mantém o registro e somente PDFs cuja redistribuição pública seja apropriada.

## Melhorias metodológicas incorporadas

Potts et al. (2026) motivou um diagnóstico de cobertura operacional baseado em atributos do teste fora das faixas observadas no treinamento. A busca expandida acrescentou uma segunda melhoria executável no Notebook 03A.05: uma auditoria diagnóstica de redundância das sete features de B, motivada por Zhang et al. (2026), com correlação de Pearson e verificação das identidades algébricas entre carga, defasagem e variação.

Essas rotinas são diagnósticas. Não removem atributos, não reabrem a seleção de hiperparâmetros e não alteram retrospectivamente os resultados do teste.

## Busca expandida de 29/10/2026

A nova triagem avaliou 65 PDFs, correspondentes a 58 documentos únicos após deduplicação. Cinco fontes acrescentaram contribuição direta ao estudo e foram incorporadas ao registro mestre e ao Notebook 03A.05:

1. Zhang et al. (2026): redundância/multicolinearidade e seleção híbrida XGBoost + Pearson. Aplicação no projeto: auditoria diagnóstica das sete features de B, sem poda retrospectiva ou novo ajuste.
2. Jin et al. (2026): transferência explicável entre usinas. Aplicação: delimitação da generalização externa como problema distinto da generalização temporal intraplanta.
3. Huang et al. (2027): previsão sob histórico reduzido, mudança de regime e calibração de incerteza. Aplicação: interpretação não monotônica do valor do histórico e extensão futura para incerteza.
4. Liu et al. (2025): regulação profunda de carga e intensidade de carbono. Aplicação: suporte físico à leitura estratificada por regime.
5. Lu, Tang e Duan (2024): soft measurement de vazão de gases sob operação dinâmica. Aplicação: explicitação de limitação metrológica possível em sistemas CEMS.

Os PDFs recebidos permanecem no acervo privado do projeto quando sua licença de redistribuição pública não está confirmada. O GitHub registra metadados, DOI/URL e finalidade de uso; apenas arquivos com redistribuição permitida devem ser copiados para `public_pdfs/`.

## Consolidação dos experimentos executados

A ablação 03A.05A, a sensibilidade temporal 03A.05B e a comparação de cinco sementes 03A.05C estão executadas e conferidas. Diebold e Mariano (1994), Grinsztajn et al. (2022), Si et al. (2019) e Künsch (1989) integram a fundamentação complementar, com as adaptações descritas no artigo e nos notebooks. Os resultados não demonstram ganho global consistente da remoção de atributos.

O [catálogo atualizado](metadata/source_registry.csv) e o [índice dos PDFs](metadata/pdfs_referencias_utilizadas.csv) identificam fontes, versões e SHA-256. As cópias integrais destinadas ao Drive usam títulos nos nomes dos arquivos. A biblioteca pública conserva sua política de redistribuição.
