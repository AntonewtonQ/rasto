# -*- coding: utf-8 -*-
"""Constrói o relatório do TCC a partir do tcc_exemplo.docx (estilos) e dos ficheiros content_*.py.
Uso: python3 build.py TEMPLATE OUT.docx [pages.json]"""
import sys, re, copy, json
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import content_pre as PRE
from content_intro import INTRO
from content_cap1 import CAP1
from content_cap2 import CAP2
from content_cap3 import CAP3
from content_cap4 import CAP4
from content_cap5 import CAP5
from content_cap6 import CAP6
from content_concl import CONCL
from content_apendices import APPX
from content_refs import REFS

TEMPLATE, OUT = sys.argv[1], sys.argv[2]
PAGES = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}
LOGO = "modelo/logo_isptec.png"

doc = Document(TEMPLATE)
body = doc.element.body
final_sect = body.find(qn("w:sectPr"))
for el in list(body):
    if el is not final_sect:
        body.remove(el)
for tag in ("w:headerReference", "w:footerReference", "w:pgNumType", "w:titlePg"):
    for e in final_sect.findall(qn(tag)):
        final_sect.remove(e)
pgMar = final_sect.find(qn("w:pgMar"))
pgMar.set(qn("w:header"), "1134"); pgMar.set(qn("w:footer"), "709")

# ---------- ajustes de estilos ----------
st = doc.styles
def style_el(name):
    return st[name].element
for name in ("Heading 1", "Heading 2", "Heading 3"):
    pPr = style_el(name).find(qn("w:pPr"))
    n = pPr.find(qn("w:numPr"))
    if n is not None:
        pPr.remove(n)
    st[name].paragraph_format.space_before = Pt(12)
    st[name].paragraph_format.space_after = Pt(12)
    st[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
st["Heading 2"].font.bold = True
st["Heading 3"].font.bold = True; st["Heading 3"].font.italic = True
for lvl in (1, 2, 3):
    nm = f"toc {lvl}"
    try:
        s = st[nm]
    except KeyError:
        s = st.add_style(nm, WD_STYLE_TYPE.PARAGRAPH); s.base_style = st["Normal"]
    s.font.size = Pt(12); s.font.bold = (lvl == 1)
    pf = s.paragraph_format
    pf.left_indent = Cm(0.6 * (lvl - 1)); pf.space_after = Pt(2); pf.line_spacing = 1.15
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
tof = st["table of figures"]; tof.font.size = Pt(12)
tof.paragraph_format.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
tof.paragraph_format.space_after = Pt(2); tof.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
cap = st["Caption"]; cap.font.size = Pt(10); cap.font.bold = False
cap.paragraph_format.space_before = Pt(6); cap.paragraph_format.space_after = Pt(4)
cap.paragraph_format.keep_with_next = True

# ---------- utilitários ----------
TOKEN = re.compile(r"(`[^`]+`|\*\*.+?\*\*|\{\{.+?\}\}|\*.+?\*)")
def add_runs(par, text, size=None, bold=None, italic=None):
    for part in TOKEN.split(text):
        if not part:
            continue
        b, i, hl = bold, italic, False
        if part.startswith("`") and part.endswith("`") and len(part) > 2:
            # código, comandos e caminhos: letra de largura fixa, sem outra marcação
            r = par.add_run(part[1:-1]); r.font.name = "Courier New"
            r._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:hAnsi"), "Courier New")
            r.font.size = Pt((size or 12) - 2)
            if b: r.bold = True
            continue
        if part.startswith("**"):
            part, b = part[2:-2], True
        elif part.startswith("{{"):
            part, hl = part[2:-2], True
        elif part.startswith("*"):
            part, i = part[1:-1], True
        # itálico dentro de negrito ou realce
        for sub in TOKEN.split(part):
            if not sub:
                continue
            ii = i
            if sub.startswith("*") and sub.endswith("*") and len(sub) > 2:
                sub, ii = sub[1:-1], True
            r = par.add_run(sub)
            if b: r.bold = True
            if ii: r.italic = True
            if size: r.font.size = Pt(size)
            if hl: r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return par

def P(text="", style="Normal", align=None, size=None, bold=None, italic=None, space_before=None,
      space_after=None, line=None, left=None, first=None, keep_next=False, page_break_before=False):
    par = doc.add_paragraph(style=style)
    if text:
        add_runs(par, text, size, bold, italic)
    pf = par.paragraph_format
    if align is not None: pf.alignment = align
    if space_before is not None: pf.space_before = Pt(space_before)
    if space_after is not None: pf.space_after = Pt(space_after)
    if line is not None: pf.line_spacing = line
    if left is not None: pf.left_indent = Cm(left)
    if first is not None: pf.first_line_indent = Cm(first)
    if keep_next: pf.keep_with_next = True
    if page_break_before: pf.page_break_before = True
    return par

def page_break():
    par = doc.add_paragraph(); par.add_run().add_break(WD_BREAK.PAGE)

def section_break(start_page=None):
    par = doc.add_paragraph()
    sp = copy.deepcopy(final_sect)
    if start_page is not None:
        pg = OxmlElement("w:pgNumType"); pg.set(qn("w:start"), str(start_page))
        cols = sp.find(qn("w:cols"))
        if cols is not None:
            cols.addprevious(pg)
        else:
            sp.find(qn("w:pgMar")).addnext(pg)
    par._p.get_or_add_pPr().append(sp)

def fld_simple(par, instr, text):
    f = OxmlElement("w:fldSimple"); f.set(qn("w:instr"), instr)
    r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
    t = OxmlElement("w:t"); t.text = text; r.append(rpr); r.append(t); f.append(r)
    par._p.append(f)

def fld_char(par, kind):
    r = par.add_run(); fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), kind); r._r.append(fc)

def instr(par, text):
    r = par.add_run(); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = text
    r._r.append(it)

def strip(text):
    return re.sub(r"\*\*|\*|\{\{|\}\}|`", "", text)

# registos para o índice e as listas
HEADINGS, CAPTIONS = [], {"Figura": [], "Tabela": [], "Quadro": []}
counter = {"Figura": 0, "Tabela": 0, "Quadro": 0}

def caption(kind, text, align):
    counter[kind] += 1; n = counter[kind]
    par = doc.add_paragraph(style="Caption"); par.paragraph_format.alignment = align
    par.add_run(kind + " ")
    fld_simple(par, f" SEQ {kind} \\* ARABIC ", str(n))
    add_runs(par, " — " + text)
    CAPTIONS[kind].append((n, strip(text)))
    return par

def fonte(text, align):
    return P("Fonte: " + text, align=align, size=10, line=1.0, space_after=12, space_before=4)

def figure(fname, cap_text, src, width):
    caption("Figura", cap_text, WD_ALIGN_PARAGRAPH.CENTER)
    par = doc.add_paragraph(); par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.keep_with_next = True; par.paragraph_format.first_line_indent = Cm(0)
    par.add_run().add_picture("figuras/" + fname, width=Cm(width))
    fonte(src, WD_ALIGN_PARAGRAPH.CENTER)

def set_cell_border(cell, **edges):
    tcPr = cell._tc.get_or_add_tcPr()
    b = tcPr.find(qn("w:tcBorders"))
    if b is None:
        b = OxmlElement("w:tcBorders"); tcPr.append(b)
    for edge in ("top", "left", "bottom", "right"):
        if edge not in edges: continue
        val = edges[edge]
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), val); e.set(qn("w:sz"), "6" if val != "nil" else "0"); e.set(qn("w:space"), "0")
        e.set(qn("w:color"), "000000"); b.append(e)

def table(kind, cap_text, header, rows, src, widths, opts=None):
    opts = opts or {}
    size = 9 if opts.get("small") else 10
    num_cols = set(opts.get("num_cols", []))
    caption(kind, cap_text, WD_ALIGN_PARAGRAPH.LEFT)
    t = doc.add_table(rows=1 + len(rows), cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    tblPr = t._tbl.tblPr
    tw = tblPr.find(qn("w:tblW"))
    tw.set(qn("w:w"), str(int(sum(widths) * 567))); tw.set(qn("w:type"), "dxa")

    grid = t._tbl.tblGrid
    for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(widths[i] * 567)))
    all_rows = [header] + rows
    last = len(all_rows) - 1
    for ri, row in enumerate(all_rows):
        tr = t.rows[ri]
        trPr = tr._tr.get_or_add_trPr()
        cs = OxmlElement("w:cantSplit"); trPr.append(cs)
        if ri == 0:
            h = OxmlElement("w:tblHeader"); trPr.append(h)
        for ci, val in enumerate(row):
            cell = tr.cells[ci]; cell.width = Cm(widths[ci])
            par = cell.paragraphs[0]
            pf = par.paragraph_format; pf.line_spacing = 1.0; pf.first_line_indent = Cm(0)
            pf.space_before = Pt(2); pf.space_after = Pt(2)
            pf.alignment = WD_ALIGN_PARAGRAPH.CENTER if (ci in num_cols or ri == 0 and ci > 0 and num_cols) else WD_ALIGN_PARAGRAPH.LEFT
            is_total = opts.get("total_row") and ri == last
            add_runs(par, val, size=size, bold=True if (ri == 0 or is_total) else None)
            if kind == "Quadro":
                set_cell_border(cell, top="single", left="single", bottom="single", right="single")
            else:
                edges = {"left": "nil", "right": "nil"}
                edges["top"] = "single" if ri == 0 else "nil"
                edges["bottom"] = "single" if (ri == 0 or ri == last) else "nil"
                if is_total: edges["top"] = "single"
                set_cell_border(cell, **edges)
    fonte(src, WD_ALIGN_PARAGRAPH.LEFT)

def heading(level, text):
    style = {1: "Heading 1", 2: "Heading 2", 3: "Heading 3"}[level]
    par = doc.add_paragraph(style=style)
    add_runs(par, text)
    if level == 1:
        par.paragraph_format.page_break_before = True
        par.paragraph_format.space_before = Pt(0); par.paragraph_format.space_after = Pt(18)
    HEADINGS.append((level, strip(text)))
    return par

def render(blocks):
    for b in blocks:
        k = b[0]
        if k == "h1": heading(1, b[1])
        elif k == "h2": heading(2, b[1])
        elif k == "h3": heading(3, b[1])
        elif k == "p": P(b[1], style="Corpo do Texto")
        elif k == "al":
            P(b[1], style="List Paragraph", line=1.5, left=1.25, first=0)
        elif k == "fig": figure(*b[1:])
        elif k == "tab": table(*b[1:])
        else: raise ValueError(k)

# ---------- índices com resultados em cache ----------
def page_of(key):
    return str(PAGES.get(key, "0"))

def static_field(instr_text, entries, style):
    """entries: list of (text, key, style_override). Field with cached result."""
    if not entries:
        par = P("{{[Sem entradas]}}"); return
    for i, (text, key, sty) in enumerate(entries):
        par = doc.add_paragraph(style=sty or style)
        if i == 0:
            fld_char(par, "begin"); instr(par, instr_text); fld_char(par, "separate")
        par.add_run(text)
        par.add_run("\t" + page_of(key))
        if i == len(entries) - 1:
            fld_char(par, "end")

def title_pre(text):
    P(f"**{text}**", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)

# =====================================================================
# 1. CAPA (secção 1, não contada)
C = WD_ALIGN_PARAGRAPH.CENTER
par = doc.add_paragraph(); par.alignment = C; par.add_run().add_picture(LOGO, width=Cm(4.0))
for line in ("INSTITUTO SUPERIOR POLITÉCNICO DE TECNOLOGIAS E CIÊNCIAS", PRE.DEPARTAMENTO, "CURSO DE ENGENHARIA INFORMÁTICA"):
    P(line, align=C, bold=True, line=1.5)
P("", space_after=60)
P(PRE.ESTUDANTE, align=C, bold=True)
P("", space_after=90)
P(PRE.TITULO, align=C, bold=True, line=1.5)
P("", space_after=170)
P("Luanda", align=C, bold=True); P(PRE.ANO, align=C, bold=True)
section_break()

# 2. FOLHA DE ROSTO (página 1)
P(PRE.ESTUDANTE, align=C, bold=True)
P("", space_after=120)
P(PRE.TITULO, align=C, bold=True, line=1.5)
P("", space_after=40)
P(PRE.NATUREZA, align=WD_ALIGN_PARAGRAPH.JUSTIFY, left=8, line=1.0, space_after=12)
P("Orientador: " + PRE.ORIENTADOR, left=8, line=1.0)
P("", space_after=150)
P("Luanda", align=C, bold=True); P(PRE.ANO, align=C, bold=True)
page_break()

# 3. FOLHA DE APROVAÇÃO
P(PRE.ESTUDANTE, align=C, bold=True)
P("", space_after=30)
P(PRE.TITULO, align=C, bold=True, line=1.5)
P("", space_after=20)
P(PRE.APROVACAO, align=WD_ALIGN_PARAGRAPH.JUSTIFY, left=8, line=1.0, space_after=30)
P("**BANCA EXAMINADORA**", align=C, space_after=30)
for who in ("Presidente da Banca", "Primeiro Oponente", "Segundo Oponente"):
    P("___________________________________________________", align=C, space_before=24)
    P(f"Prof. {{{{[Nome]}}}} – {who}", align=C)
    P("DET/ISPTEC", align=C)
P("", space_after=24)
P("Luanda, aos {{[dia]}} de {{[mês]}} de {{[ano]}}", align=C)
page_break()

# 4. DEDICATÓRIA
P("", space_after=400)
for t in PRE.DEDICATORIA:
    P(t, align=WD_ALIGN_PARAGRAPH.JUSTIFY, left=8, line=1.5, italic=True)
page_break()

# 5. AGRADECIMENTOS
title_pre("AGRADECIMENTOS")
for t in PRE.AGRADECIMENTOS:
    P(t, style="Corpo do Texto")
page_break()

# 6. RESUMO / ABSTRACT
title_pre("RESUMO")
P(PRE.RESUMO, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line=1.5, space_after=18)
P("**Palavras-chave:** " + PRE.PALAVRAS_CHAVE, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line=1.5)
page_break()
title_pre("ABSTRACT")
P(PRE.ABSTRACT, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line=1.5, space_after=18)
P("**Keywords:** " + PRE.KEYWORDS, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line=1.5)

# conteúdo textual é renderizado num documento auxiliar? Não: precisamos das entradas antes.
# Recolhe entradas fazendo uma passagem "a seco" sobre os blocos.
def dry(blocks, H, CAPS):
    cnt = {"Figura": 0, "Tabela": 0, "Quadro": 0}
    for b in blocks:
        if b[0] in ("h1", "h2", "h3"):
            H.append((int(b[0][1]), strip(b[1])))
        elif b[0] == "fig":
            cnt["Figura"] += 1; CAPS["Figura"].append((cnt["Figura"], strip(b[2])))
        elif b[0] == "tab":
            k = b[1]; cnt[k] += 1; CAPS[k].append((cnt[k], strip(b[2])))
        # contagem acumulada entre blocos
    return cnt

ALL = INTRO + CAP1 + CAP2 + CAP3 + CAP4 + CAP5 + CAP6 + CONCL
ALL_TAIL = [("h1", "REFERÊNCIAS")]
DH, DC = [], {"Figura": [], "Tabela": [], "Quadro": []}
dry(ALL + ALL_TAIL + APPX, DH, DC)

for kind, title in (("Figura", "LISTA DE FIGURAS"), ("Quadro", "LISTA DE QUADROS"), ("Tabela", "LISTA DE TABELAS")):
    page_break(); title_pre(title)
    static_field(f' TOC \\h \\z \\c "{kind}" ',
                 [(f"{kind} {n} — {t}", f"{kind}{n}", None) for n, t in DC[kind]], "table of figures")

page_break(); title_pre("LISTA DE ABREVIATURAS E SIGLAS")
for s, d in PRE.SIGLAS:
    par = P(f"{s}\t{d}", line=1.5, left=3.0, first=-3.0, align=WD_ALIGN_PARAGRAPH.LEFT)
    par.paragraph_format.tab_stops.add_tab_stop(Cm(3.0))

page_break(); title_pre("ÍNDICE")
static_field(' TOC \\o "1-3" \\h \\z \\u ', [(t, f"H{i}", f"toc {lvl}") for i, (lvl, t) in enumerate(DH)], "toc 1")

# 3.ª secção: parte textual, páginas numeradas
section_break(start_page=1)  # fecha a secção pré-textual (folha de rosto = 1)
render(ALL)
heading(1, "REFERÊNCIAS")
for r in REFS:
    P(r, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.0, space_after=12)
render(APPX)

# ---------- cabeçalhos ----------
secs = doc.sections
for i, s in enumerate(secs):
    s.different_first_page_header_footer = False
    s.header.is_linked_to_previous = False
    s.footer.is_linked_to_previous = False
    hp = s.header.paragraphs[0]
    for r in list(hp.runs): r._r.getparent().remove(r._r)
    if i == len(secs) - 1:
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        fld_char(hp, "begin"); instr(hp, " PAGE "); fld_char(hp, "separate")
        rr = hp.add_run("1"); fld_char(hp, "end")
        for r in hp.runs: r.font.size = Pt(10)

# actualizar campos ao abrir no Word
settings = doc.settings.element
uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"), "true")
for anchor in ("w:hdrShapeDefaults", "w:footnotePr", "w:endnotePr", "w:compat", "w:docVars", "w:rsids"):
    a = settings.find(qn(anchor))
    if a is not None:
        a.addprevious(uf); break
else:
    settings.append(uf)

doc.core_properties.title = strip(PRE.TITULO)
doc.core_properties.author = "[Autor]"
doc.save(OUT)
json.dump({"headings": HEADINGS, "captions": CAPTIONS}, open("build/structure.json", "w"), ensure_ascii=False)
print("ok", len(HEADINGS), {k: len(v) for k, v in CAPTIONS.items()})
