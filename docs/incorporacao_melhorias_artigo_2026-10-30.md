# Incorporação das melhorias ao artigo em 30 de outubro de 2026

A versão incorpora as melhorias documentais validadas no parecer da mesma data. Os experimentos permanecem encerrados no complemento 03A.05C.

## Alterações incorporadas

1. Metodologia: explicitação do encadeamento entre seleção, preparação, representação, ajuste e interpretação, com citação de Fayyad, Piatetsky-Shapiro e Smyth (1996), figura 1 e páginas 41-42 da revista. Não se introduz um novo método experimental.
2. Representação operacional: esclarecimento de que o conhecimento da operação orienta os atributos e de que os estimadores não impõem equações físicas na função de perda.
3. Discussão: síntese das funções distintas de 03A.05A, 03A.05B e 03A.05C, preservando o caráter retrospectivo e a ausência de novos períodos independentes.
4. Figura D1: comparação visual dos limites exploratórios de reamostragem para os contextos global e de rampas nos blocos de 1, 3 e 7 dias. A inclusão de zero no resultado global e os limites positivos nas rampas ficam visíveis na mesma escala.
5. Figura D2: MAE de validação e teste por família, cenário e semente, com escala comum, pontos individuais e médias. A figura evidencia a inversão entre períodos sem tratar sementes como novas amostras temporais.
6. Disponibilidade e rastreabilidade: inclusão das verificações documentais adicionais, atualização dos dois registros bibliográficos e do índice dos PDFs usados. O artigo passa de 40 para 41 referências; o registro mestre contém ainda uma fonte específica dos notebooks.

As figuras são chamadas nos resultados principais e foram inseridas no Apêndice D junto às análises correspondentes. Foram utilizadas as imagens já validadas, geradas exclusivamente de resultados preservados pelo script `scripts/gerar_figuras_complementos.py`.

## Validação e preservação

O documento final tem 31 páginas, 29 tabelas, sete equações e três figuras. Todas as páginas foram renderizadas e inspecionadas visualmente. As tabelas e equações foram comparadas integralmente com a versão anterior. Os 236 arquivos científicos da linha de base, excluído somente o artigo intencionalmente alterado, e os 360 arquivos do projeto de Ciência de Dados foram conferidos por SHA-256 e permaneceram idênticos.

Não houve novo treinamento, nova reamostragem, seleção pelo teste ou alteração de notebooks, previsões, modelos, métricas e dados. Os percentis de 03A.05B continuam exploratórios; a dispersão de 03A.05C permanece condicional às configurações e às mesmas partições.

O [registro de validação](../outputs/incorporacao_artigo_2026-10-30/validacao_artigo.json) identifica as versões do artigo por SHA-256 e documenta a conferência. O parecer anterior é mantido como registro da etapa de levantamento, anterior à presente incorporação.

O PDF de Fayyad está preservado no acervo privado `references/material_disciplina_modmat_2026-10-30/Fayyad_1996_KDD.pdf`, já enviado ao [Drive de materiais selecionados](https://drive.google.com/drive/folders/1uRmBmdakWIsggK61ddGq6fCnd4gA_pMa). As cópias integrais privadas não foram acrescentadas ao GitHub público.
