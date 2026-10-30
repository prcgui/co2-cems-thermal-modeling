"""Reapresenta resultados existentes de 5B/5C. Não treina modelos nem reamostra perdas."""
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
REPO=Path(__file__).resolve().parents[1]
FIG=REPO/'outputs/revisao_material_2026-10-30'
FIG.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,ok,**evidence):
    checks.append({'verificacao':name,'aprovada':bool(ok),**evidence})
    assert ok,name
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
metrics_path=REPO/'outputs/auditoria_consolidada_2026-10-29/5C/metricas_e_tempos.csv'
summary_path=metrics_path.with_name('resumo_sementes.csv')
m=pd.read_csv(metrics_path);s=pd.read_csv(summary_path)
check('40 combinações únicas de métricas',len(m)==40 and not m.duplicated(['familia','cenario','semente','particao']).any())
for _,r in s.iterrows():
    a=m[(m.familia==r.familia)&(m.cenario==r.cenario)&(m.particao==r.particao)]
    check('Média e DP para figura '+r.familia+'/'+r.cenario+'/'+r.particao,len(a)==5 and np.isclose(a.MAE.mean(),r.MAE_media,atol=1e-10,rtol=0) and np.isclose(a.MAE.std(ddof=1),r.MAE_dp_sementes,atol=1e-10,rtol=0))
p=m.pivot(index=['particao','cenario','semente'],columns='familia',values='MAE').reset_index()
check('Ordenação inversa confirmada em dez pares por partição',((p[p.particao=='teste'].MLP-p[p.particao=='teste'].XGBoost)>0).all() and ((p[p.particao=='validacao'].MLP-p[p.particao=='validacao'].XGBoost)<0).all())

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titlesize':12,'svg.fonttype':'none'})
fig,axes=plt.subplots(1,2,figsize=(11.6,5.1),sharey=True)
palette={'MLP':'#2166AC','XGBoost':'#B55A00'}
positions={('MLP','A'):0,('MLP','B'):1,('XGBoost','A'):2.3,('XGBoost','B'):3.3}
for ax,(split,title) in zip(axes,[('validacao','Validação | outubro de 2025 | 211 horas'),('teste','Teste | nov-dez de 2025 | 1.144 horas')]):
    for family in ['MLP','XGBoost']:
        x0=positions[(family,'A')];x1=positions[(family,'B')]
        for j,seed in enumerate([42,43,44,45,46]):
            rows=m[(m.particao==split)&(m.familia==family)&(m.semente==seed)].set_index('cenario')
            off=(j-2)*.045
            ax.plot([x0+off,x1+off],[rows.loc['A','MAE'],rows.loc['B','MAE']],color=palette[family],alpha=.32,lw=1,zorder=2)
            ax.scatter([x0+off,x1+off],[rows.loc['A','MAE'],rows.loc['B','MAE']],color=palette[family],s=25,alpha=.78,zorder=3)
        means=[]
        for scenario in ['A','B']:
            a=m[(m.particao==split)&(m.familia==family)&(m.cenario==scenario)]
            means.append(a.MAE.mean())
            ax.scatter(positions[(family,scenario)],a.MAE.mean(),s=72,marker='D',facecolor='white',edgecolor=palette[family],linewidth=1.8,zorder=4)
            ax.annotate(f'{a.MAE.mean():.2f}'.replace('.',','),(positions[(family,scenario)],a.MAE.mean()),xytext=(0,11),textcoords='offset points',ha='center',fontsize=10,color=palette[family],fontweight='bold')
        ax.plot([x0,x1],means,color=palette[family],lw=2.2,zorder=3)
    ax.set_title(title,pad=15);ax.set_xticks(list(positions.values()),['MLP A','MLP B','XGBoost A','XGBoost B']);ax.set_ylim(0,69);ax.yaxis.set_major_locator(MultipleLocator(10));ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
axes[0].set_ylabel('MAE (short tons de CO₂ por registro horário)')
fig.suptitle('03A.05C | A ordenação entre famílias muda entre validação e teste',fontweight='bold',fontsize=14,x=.06,ha='left',y=.99)
fig.text(.06,.075,'Pontos: sementes 42 a 46. Losangos e linhas fortes: médias entre sementes. Menor MAE indica menor erro.',fontsize=9)
fig.text(.06,.035,'Mesmas horas por partição; configuração fixa por família/cenário; sem reajuste com outubro. Comparação descritiva.',fontsize=9,color='#4B5563')
fig.subplots_adjust(top=.83,bottom=.2,wspace=.12,left=.075,right=.98)
for ext in ['png','svg']:fig.savefig(FIG/f'03A05C_validacao_teste_sementes.{ext}',dpi=180,facecolor='white')
plt.close(fig)

bs_path=REPO/'outputs/auditoria_consolidada_2026-10-29/5B/sensibilidade_blocos_calendario.csv'
bs=pd.read_csv(bs_path);bs=bs[(bs.referencia=='A')&(bs.candidata=='B_completo')&(bs.contexto.isin(['global','rampas']))]
fig,axes=plt.subplots(1,2,figsize=(10.8,4.3),sharex=True)
for ax,(ctx,title,count) in zip(axes,[('global','Global',1144),('rampas','Rampas intensas',258)]):
    sub=bs[bs.contexto==ctx].sort_values('bloco_dias')
    check('Figura 5B usa três comprimentos '+ctx,len(sub)==3 and (sub.n==count).all())
    for j,(_,r) in enumerate(sub.iterrows()):
        ax.plot([r.percentil_2_5,r.percentil_97_5],[j,j],color='#2166AC',lw=3,solid_capstyle='round')
        ax.scatter(r.d_medio,j,color='#173A59',s=45,zorder=4)
    ax.axvline(0,color='#646464',lw=1,ls='--');ax.set_yticks([0,1,2],['1 dia','3 dias','7 dias']);ax.set_ylim(2.5,-.5);ax.set_title(f'{title} | {count:,} horas'.replace(',','.'));ax.set_xlabel('Diferença média de perda absoluta: A menos B');ax.grid(axis='x',alpha=.18);ax.set_xlim(-5,10)
fig.suptitle('03A.05B | Sensibilidade ao comprimento dos blocos',fontweight='bold',fontsize=14,x=.07,ha='left',y=.99)
fig.text(.07,.09,'Valores positivos favorecem B. Pontos: diferenças médias. Barras: percentis exploratórios 2,5 e 97,5.',fontsize=9)
fig.text(.07,.045,'Unidade: short tons de CO₂ por registro horário. Cobertura nominal não demonstrada; não são intervalos de previsão.',fontsize=9,color='#4B5563')
fig.subplots_adjust(top=.8,bottom=.25,wspace=.25,left=.075,right=.98)
for ext in ['png','svg']:fig.savefig(FIG/f'03A05B_sensibilidade_blocos_global_rampas.{ext}',dpi=180,facecolor='white')
plt.close(fig)


record={'rotina':'apresentação de CSVs existentes; sem treino ou nova reamostragem','verificacoes':checks,'fontes':{p.relative_to(REPO).as_posix():sha(p) for p in [metrics_path,summary_path,bs_path]}}
(FIG/'validacao_figuras_reproducao.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print('Figuras geradas a partir dos resultados existentes; verificações:',len(checks))
