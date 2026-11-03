import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"font.family":"Liberation Serif","savefig.dpi":300})
INK="#1B1A22"; MUTED="#55515F"; T="#3A2D8F"; FILL="#EEEBFA"; G="#8A8494"
fig,ax=plt.subplots(figsize=(6.5,3.6)); ax.set_xlim(0,10); ax.set_ylim(0,5.6); ax.axis("off")
def box(x,y,w,h,text,fill,edge):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.25",fc=fill,ec=edge,lw=1.2))
    ax.text(x,y,text,ha="center",va="center",fontsize=11,color=INK,linespacing=1.3)
box(5,4.75,4.0,1.0,"Terceiro verificado\n(aceleradora ou universidade)","white",G)
box(1.75,1.6,3.2,1.25,"Startup\n(conhece a sua qualidade,\ntracção e equipa)",FILL,T)
box(8.25,1.6,3.2,1.25,"Investidor\n(conhece o seu mandato,\ncapacidade e intenção)",FILL,T)
def arr(p,q,color=MUTED,ls="-",rad=0.0):
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle="-|>",mutation_scale=12,color=color,lw=1.2,linestyle=ls,connectionstyle=f"arc3,rad={rad}"))
arr((3.45,1.95),(6.55,1.95),ls="--"); ax.text(5,2.12,"informação declarada,\npouco fiável para o investidor",ha="center",va="bottom",fontsize=9.5,color=MUTED)
arr((6.55,1.25),(3.45,1.25),ls="--"); ax.text(5,1.08,"mandato pouco explícito: a startup\nnão sabe a quem se dirigir",ha="center",va="top",fontsize=9.5,color=MUTED)
arr((3.6,4.3),(2.2,2.3)); ax.text(1.55,3.35,"confirma participação\ne marcos, com data",ha="center",va="center",fontsize=9.5,color=MUTED)
arr((6.4,4.3),(7.8,2.3),color=T); ax.text(8.5,3.35,"sinal verificável\n(quem confirmou e quando)",ha="center",va="center",fontsize=9.5,color=T)
fig.tight_layout(pad=0.2); fig.savefig("figuras/fig02.png")
