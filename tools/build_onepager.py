#!/usr/bin/env python3
"""One-page landscape comparison - S Northgate Ave development options."""
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle)

FOREST = colors.HexColor("#1F3D2B"); MOSS = colors.HexColor("#4A6B52")
SAND = colors.HexColor("#EFE9DD"); SANDLT = colors.HexColor("#F7F4EC")
INKY = colors.HexColor("#2B2B28"); GRAY = colors.HexColor("#6B6B64")
RULE = colors.HexColor("#C9C2B2"); ACCENT = colors.HexColor("#B0713A")
HILITE = colors.HexColor("#FBF3E4")

PAGE = landscape(letter); PW, PH = PAGE
ML, MR, MT, MB = 0.42*inch, 0.42*inch, 0.40*inch, 0.36*inch

ss = getSampleStyleSheet()
def st(name, **kw):
    return ParagraphStyle(name, parent=ss["Normal"], **kw)

S_CELL  = st("c",  fontName="Helvetica", fontSize=7.6, leading=9.6, textColor=INKY)
S_LAB   = st("l",  fontName="Helvetica-Bold", fontSize=7.6, leading=9.6, textColor=FOREST)
S_HEAD  = st("h",  fontName="Helvetica-Bold", fontSize=8.6, leading=10.4, textColor=colors.white)
S_HEADS = st("hs", fontName="Helvetica", fontSize=6.6, leading=8.2, textColor=colors.HexColor("#DCE5DC"))
S_FACT  = st("f",  fontName="Helvetica", fontSize=7.4, leading=9.4, textColor=INKY)
S_FOOT  = st("ft", fontName="Helvetica", fontSize=6.9, leading=8.8, textColor=GRAY)
S_FOOTB = st("fb", fontName="Helvetica-Bold", fontSize=7.2, leading=9.0, textColor=FOREST)

def P(t, s=S_CELL): return Paragraph(t, s)

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(FOREST)
    canvas.rect(0, PH-0.62*inch, PW, 0.62*inch, stroke=0, fill=1)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, PH-0.62*inch-3.5, PW, 3.5, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 15.5)
    canvas.drawString(ML, PH-0.40*inch, "S Northgate Ave \u2014 Development Options at a Glance")
    canvas.setFont("Helvetica", 8.3)
    canvas.setFillColor(colors.HexColor("#DCE5DC"))
    canvas.drawString(ML, PH-0.545*inch,
        "Vacant 0.58-acre flag lot (25,281 sq ft) adjoining the owners' residence  \u00b7  Portland, OR 97219  \u00b7  Tax account R547474")
    canvas.setFillColor(colors.HexColor("#F0C89A"))
    canvas.setFont("Helvetica-Bold", 8.3)
    canvas.drawRightString(PW-MR, PH-0.40*inch, "DRAFT v1 \u2014 July 20, 2026")
    canvas.setFont("Helvetica", 7.4)
    canvas.drawRightString(PW-MR, PH-0.545*inch, "Pending: preliminary title report (disclosed non-utility easement unidentified)")
    canvas.restoreState()

doc = BaseDocTemplate("/home/claude/northgate/S_Northgate_Options_One_Pager.pdf",
                      pagesize=PAGE, leftMargin=ML, rightMargin=MR,
                      topMargin=0.62*inch+0.12*inch, bottomMargin=MB,
                      title="S Northgate Ave Options One-Pager")
fr = Frame(ML, MB, PW-ML-MR, PH-(0.62*inch+0.12*inch)-MB, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[fr], onPage=on_page)])

story = []

# ---- facts strip ----
facts = ("<b>Jurisdiction:</b> City of Portland (annexed) \u00b7 Council District 4   |   "
 "<b>Zoning:</b> R20 \u2014 no c/p/z overlays observed   |   <b>Schools:</b> Riverdale SD 51J   |   "
 "<b>Access:</b> pole meets S Northgate Ave right of way   |   "
 "<b>Utilities at boundary (seller disclosure 6/2026):</b> public water access (hook-up charge unknown), public sewer available, "
 "electric, gas, phone, internet   |   <b>Survey:</b> ROS 68582 (2023)   |   No soil tests; no known contamination")
tfacts = Table([[P(facts, S_FACT)]], colWidths=[PW-ML-MR])
tfacts.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), SAND),
    ("BOX", (0,0), (-1,-1), 0.5, RULE),
    ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(tfacts)
story.append(Spacer(1, 6))

# ---- main comparison ----
def hd(title, tag):
    return Paragraph(f"{title}<br/><font size=6.6 color=#DCE5DC>{tag}</font>", S_HEAD)

head = [P("", S_HEAD),
        hd("A \u2014 Rental house + detached ADU", "RECOMMENDED BASELINE"),
        hd("B \u2014 Duplex, hold both units", "BEST PURE YIELD"),
        hd("C \u2014 Single rental house", "SIMPLEST BUILD"),
        hd("D \u2014 Consolidate lots: compound", "LIFESTYLE + ONLY LAWFUL STR")]

rows = [
 ("Concept & program",
  "~2,400 sq ft long-term rental house + 800 sq ft detached ADU for visiting family (leasable when idle). One lot, by-right path.",
  "One ~3,000 sq ft structure, two ~1,500 sq ft units, both leased long-term. Allowed on every buildable R20 lot.",
  "One ~2,400 sq ft house, leased long-term. Cleanest permit path; add an ADU later if desired.",
  "Merge with owners' lot; build accessory to the existing home: detached ADU (the \u201ctiny home\u201d), workshop w/ studio above, sport court in the screened flag body. Phase-able."),
 ("Cost, excl. land*",
  "$1.35M \u2013 $1.70M (house $1.0\u20131.2M; ADU $250\u2013330K SDC-exempt w/ covenant; site + SDCs + sprinklers)",
  "$1.30M \u2013 $1.50M (hard cost $1.15\u20131.3M; two-unit SDCs; site; sprinklers)",
  "$1.10M \u2013 $1.35M (hard cost $1.0\u20131.2M; SDCs; site; sprinklers)",
  "$0.8M \u2013 $1.1M full scope \u2014 ADU $250\u2013350K; workshop + studio $450\u2013600K; court $60\u2013120K; elements stand alone"),
 ("Gross income / mo",
  "$4,800\u2013$5,800 house; + $2,000\u2013$2,400 ADU when leased = up to $6,800\u2013$8,200",
  "$3,000\u2013$3,600 per unit = $6,000\u2013$7,200",
  "$4,800\u2013$5,800",
  "$2,000\u2013$2,400 (ADU long-term) \u2014 or STR upside in family-visit gaps"),
 ("Approx. gross yield**",
  "4\u20135% (both units leased)",
  "4\u20134.5%+ \u2014 strongest cash-on-cost",
  "3\u20134% \u2014 appreciation / wealth-storage play",
  "~2% \u2014 lifestyle-weighted"),
 ("Short-term rental",
  "No \u2014 no operator resides on site",
  "No \u2014 no operator resides on site",
  "No \u2014 no operator resides on site",
  "Yes \u2014 Type A permit (owners live on consolidated site); STR of ADU repays waived SDCs"),
 ("Family guest space",
  "Yes \u2014 the ADU",
  "Possible \u2014 hold one unit open (forgoes its rent)",
  "Not until an ADU is added",
  "Yes \u2014 the ADU / studio"),
 ("Key watch-outs",
  "ADU on site blocks future middle-housing unit division; most site work of A\u2013C; FAR caps total size",
  "Design so it reads as one house in an estate-scale pocket; unit division for separate sale = clunky shared-pole easements (fallback only); thinner duplex comps",
  "Weakest income per dollar; same flag premium spread over less rent",
  "Hard to reverse \u2014 re-division must meet R20 standards; forfeits separate-lot value & independent sale; court abuts rear yards (noise / lighting siting)"),
 ("Best for",
  "Income and dedicated family space at the same time",
  "Maximum cash flow from the land",
  "Simplicity, low management, long-hold appreciation",
  "Family lifestyle, phased budget, and the only lawful STR route"),
]

lab_w = 1.02*inch
col_w = (PW-ML-MR-lab_w)/4.0
data = [head] + [[P(r[0], S_LAB)] + [P(x) for x in r[1:]] for r in rows]
t = Table(data, colWidths=[lab_w, col_w, col_w, col_w, col_w])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), FOREST),
    ("BACKGROUND", (0,1), (0,-1), SAND),
    ("BACKGROUND", (1,1), (1,-1), HILITE),
    ("ROWBACKGROUNDS", (2,1), (-1,-1), [colors.white, SANDLT]),
    ("GRID", (0,0), (-1,-1), 0.5, RULE),
    ("BOX", (1,0), (1,-1), 1.1, ACCENT),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 4.5), ("RIGHTPADDING", (0,0), (-1,-1), 4.5),
    ("TOPPADDING", (0,0), (-1,-1), 2.6), ("BOTTOMPADDING", (0,0), (-1,-1), 2.6),
]))
story.append(t)
story.append(Spacer(1, 6))

# ---- footer: diligence + notes ----
dil = ("<b>Open diligence before the ranking hardens:</b>  (1) preliminary title report + the disclosed non-utility easement instrument "
 "(and any Palatine Hill / West Palatine Ridge CC&Rs \u2014 private restrictions can trump zoning)   (2) legal-lot confirmation \u2014 parcel was "
 "assembled from multiple plat pieces + a 1947 street vacation; more than one legal lot upgrades everything   (3) city-maintained street check at the "
 "frontage (precondition for the duplex + detached-ADU combo)   (4) official overlay / infill-options confirmation with a City planner   "
 "(5) geotechnical recon (West Hills slope drives foundations & retaining)   (6) utility quotes \u2014 sewer lateral down the pole; water hook-up "
 "charge unknown   (7) stormwater infiltration test \u00b7 tree survey \u00b7 boundary pins")
notes = ("*Planning ranges, roughly \u00b125%, July 2026; include $40\u201380K flag-lot site premium and 13D fire sprinklers where noted.   "
 "**Gross yield adds a $500K land-basis placeholder (replace with contract price) and excludes vacancy, operating costs, and property tax.   "
 "Not legal, tax, investment, or engineering advice \u2014 verify all items with the City of Portland and licensed professionals.")
tfoot = Table([[P(dil, S_FOOT)],[P(notes, S_FOOT)]], colWidths=[PW-ML-MR])
tfoot.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,0), SANDLT),
    ("BOX", (0,0), (0,0), 0.5, RULE),
    ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 3.5), ("BOTTOMPADDING", (0,0), (-1,-1), 3.5),
]))
story.append(tfoot)

doc.build(story)
print("one-pager built")
