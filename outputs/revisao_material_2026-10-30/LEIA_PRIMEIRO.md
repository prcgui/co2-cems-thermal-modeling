# Verificação e apresentação dos experimentos concluídos

As figuras reapresentam os CSVs já preservados dos complementos 5B e 5C. Não houve treino, busca de parâmetros ou nova reamostragem. Os registros JSON distinguem as 38 verificações de integridade/apresentação da repetição das 376 verificações da auditoria existente.

- `03A05C_validacao_teste_sementes`: famílias e cenários em validação/teste; pontos representam sementes e losangos representam médias.
- `03A05B_sensibilidade_blocos_global_rampas`: diferenças de perda absoluta A menos B; percentis exploratórios, sem cobertura nominal demonstrada.
- `validacao_integridade_e_figuras.json`: engenharia de atributos executada em isolamento e verificações de dados/apresentação.
- `verificacao_final_drive.json`: repetição da auditoria de modelos e previsões, com o nome histórico da rotina preservado.
- `sincronizacao_revisao.json`: confirmação da publicação e do upload, quando concluídos.

As figuras podem ser refeitas com `python scripts/gerar_figuras_complementos.py`, a partir da raiz do repositório e de suas dependências usuais. A numeração das células na matriz inclui células Markdown e começa em 1.
