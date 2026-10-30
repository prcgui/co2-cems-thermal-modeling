# Mapa dos experimentos concluídos de Modelagem Matemática com IA

O estudo está encerrado nos notebooks 03A.05, 03A.05A, 03A.05B e 03A.05C. Este mapa organiza evidências existentes, sem novo treinamento, reamostragem ou cálculo de métricas. O histórico anterior está preservado nos demais notebooks.

## Perguntas e evidências

| Etapa | Pergunta | Condições que definem a comparação | Evidência preservada | Alcance |
|---|---|---|---|---|
| [03A.05](../notebooks/03A.05_trajetoria_operacional_historico_ampliado.ipynb) | A trajetória acrescenta informação à carga atual? | Elegibilidade comum A/B; treino de seleção e outubro para seleção de complexidade; reajuste com outubro; teste de novembro-dezembro de 2025 | [Resultado global](../outputs/tables/03A05_resultado_final_A_B.csv) e [contextos](../outputs/tables/03A05_comparacao_contextos_operacionais.csv) | B não melhora o MAE global; ganho específico de 22,90% nas 258 horas de rampas intensas |
| [03A.05A](../notebooks/03A_05A_ablacao_controlada_features_Colab.ipynb) | Qual o efeito de retiradas específicas de atributos de B? | Mesmos dados e configuração de B; semente 42; 721 árvores; 88.686 horas no reajuste e 1.144 no teste | [Pacote executado 5A](../outputs/auditoria_consolidada_2026-10-29/5A/) e artigo, Tabela D1 | Isolamento parcial dentro de B; A é controle externo com outra complexidade |
| [03A.05B](../notebooks/03A_05B_incerteza_pareada_calendario.ipynb) | A descrição das diferenças de perda depende do comprimento dos blocos? | Modelos salvos; blocos de 1, 3 e 7 dias de calendário; 10.000 sorteios por comprimento; semente 42 | [Pacote executado 5B](../outputs/auditoria_consolidada_2026-10-29/5B/) e artigo, Tabelas D2-D3 | Sensibilidade exploratória das perdas; sem novos ajustes e sem cobertura nominal demonstrada |
| [03A.05C](../notebooks/03A_05C_MLP_XGBoost_sementes_protocolo_comum_Colab.ipynb) | Como famílias e cenários se comportam nas cinco sementes? | Duas famílias × dois cenários × cinco sementes; 20 ajustes; treino 88.475, validação 211 e teste 1.144; sem reajuste com outubro | [Resumo](../outputs/auditoria_consolidada_2026-10-29/5C/resumo_sementes.csv), [protocolo](../outputs/auditoria_consolidada_2026-10-29/5C/protocolo_antes_do_treino.json) e artigo, Tabela D4 | Menor MAE do XGBoost nos dez pares de teste; ordenação inversa na validação; efeito de B sem estabilidade global |

O ganho de 13,28% com ampliação do histórico pertence à comparação do [03A.04](../notebooks/03A.04_volume_dados_generalizacao_temporal_iatan.ipynb), anterior aos complementos. Não resulta desta revisão documental.

## Fontes de variação e interpretação

| Dimensão | Onde foi examinada | O que não deve ser confundido |
|---|---|---|
| Representação dos atributos | A/B no 5 e 5C; retiradas específicas no 5A | Correlação e identidade algébrica não demonstram dispensabilidade preditiva |
| Dependência temporal das perdas | Blocos de calendário do 5B | Réplicas de perdas não são novos treinamentos ou períodos independentes |
| Variação entre treinamentos | Sementes do 5C | Cinco sementes não medem generalização para cinco períodos novos |
| Seleção e reutilização do teste | Limitações do artigo e protocolos | Nenhum complemento elimina a influência de consultas anteriores ao teste |
| Procedimento de ajuste | Reajuste no 5 e ausência de reajuste no 5C | As métricas desses protocolos não devem ser fundidas em uma única comparação |

## Proveniência dos resultados

Os protocolos registram configurações e insumos; as saídas guardam previsões e métricas; a auditoria documenta a conferência posterior. As [376 verificações](../outputs/auditoria_consolidada_2026-10-29/Relatorio_final_auditoria.txt) permanecem como evidência de conferência, sem serem descritas como repetição independente de todos os treinamentos.

A adaptação documental de perguntas, contrastes e evidências é motivada por Fayyad, Piatetsky-Shapiro e Smyth (1996), Shcherbakov et al. (2014), Liu e Yoon (2024) e pelas aulas de e-Science/DoE. Os princípios FAIR de Wilkinson et al. (2016) orientam a organização dos metadados, sem declaração de conformidade integral. Fontes e cópias estão descritas no [parecer](parecer_material_disciplina_modmat_2026-10-30.md) e no [índice de materiais](../references/metadata/material_disciplina_modmat_2026-10-30.csv).
