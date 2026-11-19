# Metodologia

## Problema e dados

O estudo estima a massa de CO₂ por registro horário da Iatan Unit 2, unidade termelétrica a carvão identificada pela EPA como Facility ID 6065, Missouri. Os dados públicos provêm de CEMS/CAMPD. O alvo é `CO2 Mass (short tons)`, sem divisão pelo tempo de operação na hora.

As entradas incluem a carga da própria hora: trata-se de estimação contemporânea, não de previsão antecipada com carga futura desconhecida. A análise inicial utiliza 2025; os experimentos históricos examinam arquivos anuais de 2010 a 2025 e adotam 2011–2022 como histórico principal nas comparações finais.

## Seleção e preparação

A seleção considera elegibilidade da unidade, cobertura temporal, qualidade dos dados e variabilidade operacional. A preparação preserva a ordem cronológica e distingue horas ON (`Operating Time > 0`) e OFF (`Operating Time = 0`). Horas de operação parcial integram a análise.

Ausências estruturais em horas OFF são preservadas nas variáveis originais; representações tratadas são criadas separadamente. A análise por intervalo interquartil sinaliza valores extremos sem exclusão automática. A PCA é exploratória; suas componentes não substituem os atributos dos modelos.

As transformações de escala são ajustadas somente no treino. Os atributos temporais usam a carga e o histórico operacional, sem variáveis derivadas do CO₂ como entradas.

## Representações e modelos

- **Cenário A:** carga instantânea (`load_current_mw`).
- **Cenário B:** carga, defasagem de uma hora, variação horária, variação absoluta, média das três horas anteriores, tempo de operação anterior e horas desde a partida.
- **Cenário C:** representação ampliada com 24 atributos nas etapas exploratórias.

São utilizados MLP e XGBoost. A MLP emprega camadas ocultas 64/32, ReLU, saída linear e Adam. Os notebooks especificam as transformações, os critérios de parada e os hiperparâmetros de cada etapa.

A otimização pareada do XGBoost em 03A.03 usa 30 configurações comuns aos cenários A/B e cinco partições temporais. A avaliação histórica em 03A.04 compara janelas de 1, 2, 3, 5 e 10 anos e examina a transferência entre períodos da mesma unidade.

## Partições e comparação final

A separação inicial de 2025 usa janeiro–setembro para treino, outubro para validação e novembro–dezembro para avaliação. Na amostra inicial, são 4.894, 211 e 1.144 horas operacionais, respectivamente.

No **03A.05**, os cenários A/B são comparados nas mesmas observações elegíveis. A complexidade é selecionada com treino de 88.475 horas e validação de 211 horas em outubro; o ajuste final incorpora outubro, totalizando 88.686 horas. A avaliação usa as mesmas 1.144 horas de novembro–dezembro de 2025.

No **03A.05A**, a ablação retira blocos específicos de atributos de B, mantendo dados, semente e configuração de B fixos. O cenário A funciona como controle externo e tem outra complexidade; os resultados não isolam um efeito universal de cada variável.

No **03A.05B**, diferenças pareadas de perda absoluta são reamostradas em blocos de calendário de 1, 3 e 7 dias, com 10.000 sorteios por comprimento e semente 42. São utilizadas previsões salvas, sem novos ajustes. Os percentis são exploratórios, sem cobertura nominal demonstrada.

No **03A.05C**, MLP e XGBoost são comparados nos cenários A/B e nas sementes 42–46, totalizando 20 ajustes. As partições têm 88.475 horas de treino, 211 de validação e 1.144 de teste. **Não há reajuste com outubro**; suas métricas devem ser interpretadas separadamente das de 03A.05.

## Métricas e interpretação

MAE, RMSE, mediana do erro absoluto, R², NMAE e viés descrevem o desempenho global. NMAE é `100 × MAE / média observada`; o resíduo é observado menos previsto. Ganho de B é `100 × (MAE A − MAE B) / MAE A`.

A análise por contexto distingue as primeiras seis horas após partidas e as rampas intensas, definidas pelo percentil 90 da variação absoluta de carga no treino. Os contextos podem se sobrepor. Comparações de modelos exigem as mesmas horas e a explicitação do protocolo de ajuste.

A ampliação do histórico reduz o MAE na comparação específica de 03A.04. Em 03A.05, a trajetória não reduz o MAE global, mas apresenta ganho nas rampas intensas. Ablação, sensibilidade em blocos e variação entre sementes examinam dimensões distintas desses resultados.

## Limitações

A seleção da unidade e do histórico é retrospectiva. O período de teste foi consultado ao longo do desenvolvimento e não constitui avaliação final completamente cega. A separação cronológica não elimina esse risco de seleção.

O estudo envolve uma unidade e períodos específicos; não demonstra generalização para outras usinas, efeito causal dos atributos ou estabilidade instrumental ao longo dos anos. Cinco sementes descrevem variação de treinamento nas mesmas horas, não cinco períodos independentes. A sensibilidade em blocos não produz intervalos de previsão calibrados.

Os procedimentos, as equações e as referências completas estão no [artigo](../artigo/Artigo_CO2_Modelagem_Matematica_IA.docx) e nos [notebooks](../notebooks/). As métricas e figuras estão em [resultados](../outputs/README.md); as fontes são identificadas no [catálogo bibliográfico](../references/source_registry.csv).
