# Fontes do monitoramento

Extratos técnicos das fontes oficiais da U.S. EPA para a Iatan Unit 2 (Facility ID 6065). Os planos são consultas posteriores com vigências históricas; não representam quinze versões anuais independentes.

- `original_plan_unit2.xml`: extrato da unidade no [arquivo XML da instalação](https://api.epa.gov/easey/bulk-files/xml/mp/006065_MP.zip).
- `current_plan_unit2.json`: extrato da [exportação do plano ECMPS](https://api.epa.gov/easey/monitor-plan-mgmt/plans/export?planId=DWH3021DNT-5A975BAEEA3B4DE698FA731B4AE3347A), atualizado em janeiro de 2026.
- `mdm_*-codes.json`: seis tabelas de códigos de métodos, substituição, parâmetros, componentes, sistemas e aquisição, disponíveis nos [dados mestres da EPA](https://api.epa.gov/easey/master-data-mgmt/list).
- `emissions_fields.json`: definições de massa de CO₂, indicador e tempo de operação, extraídas da [documentação de emissões](https://api.epa.gov/easey/emissions-mgmt/swagger-json).

O [manual ECMPS](../public_pdfs/EPA_2024_ECMPS_Monitoring_Plan.pdf) fundamenta a leitura dos campos e das vigências. O cálculo está em [`caracterizar_monitoramento.py`](../../scripts/caracterizar_monitoramento.py); execute `python scripts/caracterizar_monitoramento.py` na raiz, com os insumos anuais presentes. Os [resultados](../../outputs/tables/monitoramento/) acompanham a entrega.
