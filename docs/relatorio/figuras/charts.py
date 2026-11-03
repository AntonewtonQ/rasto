import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
plt.rcParams.update({"font.family":"Liberation Serif","font.size":11,"axes.edgecolor":"#8A8494",
  "axes.linewidth":0.8,"xtick.color":"#55515F","ytick.color":"#1B1A22","savefig.dpi":300})
INK="#1B1A22"; MUTED="#55515F"; BAR="#3A2D8F"; GRID="#E3DFD7"
N=24
def hbar(fname, labels, counts, denom=N, xlabel="Percentagem das respostas (n = 24)", w=6.3, pctonly=False):
    # sorted descending, largest at top
    pairs=sorted(zip(labels,counts), key=lambda p:p[1])
    labs=[p[0] for p in pairs]; vals=[p[1] for p in pairs]
    pcts=[v/denom*100 for v in vals]
    h=0.42*len(labs)+0.9
    fig,ax=plt.subplots(figsize=(w,h))
    bars=ax.barh(range(len(labs)),pcts,height=0.6,color=BAR,edgecolor="white",linewidth=0)
    ax.set_yticks(range(len(labs))); ax.set_yticklabels(labs)
    for i,(p,v) in enumerate(zip(pcts,vals)):
        txt=f"{p:.1f}%".replace(".",",") if pctonly else f"{v} ({p:.1f}%)".replace(".",",")
        ax.text(p+1.2,i,txt,va="center",ha="left",color=INK,fontsize=10)
    top=max(pcts); ax.set_xlim(0,top*1.38)
    step=20 if top<=70 else 25
    ax.set_xticks([t for t in range(0,101,step) if t<=top+step*0.6])
    ax.xaxis.grid(True,color=GRID,linewidth=0.6); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#8A8494")
    ax.set_xlabel(xlabel,color=MUTED)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,_: f"{x:.0f}%"))
    fig.tight_layout(); fig.savefig(f"figuras/{fname}.png"); plt.close(fig)

# Figura 3 — ameaças (INAPEM/Unitel 2023 apud Manuel 2023); percentages only, n of study = 115
labs=["Falta de financiamento","Regulação","Tributação","Concorrência","Falta de talentos ou equipa","Outras"]
vals=[62,47,40,38,31,22]
hbar("fig03_ameacas",labs,vals,denom=100,xlabel="Percentagem das startups inquiridas (n = 115)",pctonly=True)
# Figura 5 — perfil
hbar("fig05_perfil",["Fundador(a) ou membro de startup acelerada","Investidor(a)","Representante de aceleradora ou incubadora","Outro perfil"],[17,3,2,2])
# Figura 6 — problemas frequentes (frequentemente + quase sempre)
hbar("fig06_problemas",["Informação dispersa em vários canais","Dificuldade em saber a etapa de cada investidor",
  "Falta de registo de reuniões, decisões ou soft commits","Dificuldade em partilhar dados e documentos de forma segura",
  "Falta de indicadores claros sobre a captação"],[10,13,13,12,14],
  xlabel="«Frequentemente» ou «quase sempre» (n = 24)")
# Figura 7 — funcionalidades
hbar("fig07_funcionalidades",["Gestão de perfil de startup","Gestão de rondas de investimento","Data room com controlo de acessos",
  "Registo de contactos e reuniões","Registo de soft commits e estado das negociações","Painéis de indicadores",
  "Integração com assinatura electrónica"],[23,13,11,14,13,17,13],xlabel="Escolha múltipla (n = 24)")
# Figura 8 — interesse (ordinal, keep order)
fig,ax=plt.subplots(figsize=(6.3,3.1))
labs=["Sem\ninteresse","Pouco\ninteresse","Algum\ninteresse","Muito\ninteresse","Interesse\nmáximo"]; vals=[1,0,3,10,10]
pc=[v/24*100 for v in vals]
ax.bar(range(5),pc,width=0.6,color=BAR)
for i,(p,v) in enumerate(zip(pc,vals)):
    ax.text(i,p+1.5,f"{v} ({p:.1f}%)".replace(".",","),ha="center",color=INK,fontsize=10)
ax.set_xticks(range(5)); ax.set_xticklabels(labs)
ax.set_ylim(0,55); ax.yaxis.grid(True,color=GRID,linewidth=0.6); ax.set_axisbelow(True)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,_: f"{x:.0f}%"))
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.set_ylabel("Percentagem (n = 24)",color=MUTED)
fig.tight_layout(); fig.savefig("figuras/fig08_interesse.png"); plt.close(fig)
print("ok")
