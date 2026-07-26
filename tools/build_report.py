#!/usr/bin/env python3
"""Detailed development options report - S Northgate Ave, Portland OR."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether, HRFlowable,
                                NextPageTemplate)

# ---------- palette ----------
FOREST   = colors.HexColor("#1F3D2B")
MOSS     = colors.HexColor("#4A6B52")
SAND     = colors.HexColor("#EFE9DD")
SANDLT   = colors.HexColor("#F7F4EC")
INKY     = colors.HexColor("#2B2B28")
GRAY     = colors.HexColor("#6B6B64")
RULE     = colors.HexColor("#C9C2B2")
ACCENT   = colors.HexColor("#B0713A")

PAGE_W, PAGE_H = letter
M = 0.8 * inch

styles = getSampleStyleSheet()

def st(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    s = ParagraphStyle(name, parent=base, **kw)
    return s

S_TITLE   = st("t",  fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=colors.white)
S_SUB     = st("sub", fontName="Helvetica", fontSize=11, leading=15, textColor=colors.HexColor("#DCE5DC"))
S_H1      = st("h1", fontName="Helvetica-Bold", fontSize=14.5, leading=18, textColor=FOREST,
               spaceBefore=16, spaceAfter=6)
S_H2      = st("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=MOSS,
               spaceBefore=10, spaceAfter=4)
S_BODY    = st("b",  fontName="Helvetica", fontSize=9.6, leading=13.6, textColor=INKY, spaceAfter=6)
S_BULL    = st("bu", parent=S_BODY, leftIndent=14, bulletIndent=4, spaceAfter=3)
S_SMALL   = st("sm", fontName="Helvetica", fontSize=8.2, leading=11, textColor=GRAY)
S_CELL    = st("c",  fontName="Helvetica", fontSize=8.8, leading=11.6, textColor=INKY)
S_CELL_B  = st("cb", parent=S_CELL, fontName="Helvetica-Bold")
S_CELL_W  = st("cw", parent=S_CELL_B, textColor=colors.white)
S_KICKER  = st("k",  fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT,
               spaceBefore=2, spaceAfter=2)

def P(txt, s=S_BODY): return Paragraph(txt, s)
def B(txt): return Paragraph(txt, S_BULL, bulletText="\u2022")

# ---------- page furniture ----------
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE); canvas.setLineWidth(0.6)
    canvas.line(M, 0.62*inch, PAGE_W - M, 0.62*inch)
    canvas.setFont("Helvetica", 7.6); canvas.setFillColor(GRAY)
    canvas.drawString(M, 0.46*inch,
        "S Northgate Ave, Portland OR 97219  \u00b7  Development Options Study  \u00b7  Draft v1 \u2014 July 20, 2026")
    canvas.drawRightString(PAGE_W - M, 0.46*inch, f"Page {doc.page}")
    canvas.setFont("Helvetica-Oblique", 7.0)
    canvas.drawString(M, 0.33*inch,
        "Planning-level study for the owners' internal use \u2014 not legal, tax, investment, or engineering advice. Verify all items with the City of Portland and licensed professionals.")
    canvas.restoreState()

def on_first(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(FOREST)
    canvas.rect(0, PAGE_H - 2.05*inch, PAGE_W, 2.05*inch, stroke=0, fill=1)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, PAGE_H - 2.05*inch - 5, PAGE_W, 5, stroke=0, fill=1)
    canvas.restoreState()
    on_page(canvas, doc)

doc = BaseDocTemplate("/home/claude/northgate/S_Northgate_Development_Options_Report.pdf",
                      pagesize=letter, leftMargin=M, rightMargin=M,
                      topMargin=M, bottomMargin=0.85*inch,
                      title="S Northgate Ave Development Options Study",
                      author="Prepared with Claude")
frame_first = Frame(M, 0.85*inch, PAGE_W - 2*M, PAGE_H - 2.05*inch - 0.35*inch - 0.85*inch, id="f1")
frame_rest  = Frame(M, 0.85*inch, PAGE_W - 2*M, PAGE_H - M - 0.85*inch, id="fr")
doc.addPageTemplates([PageTemplate(id="First", frames=[frame_first], onPage=on_first),
                      PageTemplate(id="Rest",  frames=[frame_rest],  onPage=on_page)])

story = [NextPageTemplate("Rest")]

# ---------- cover header text drawn as flowables in band ----------
class Cover(HRFlowable):
    pass

from reportlab.platypus import Flowable
class CoverText(Flowable):
    def __init__(self):
        Flowable.__init__(self); self.width = PAGE_W - 2*M; self.height = 0
    def draw(self):
        c = self.canv; c.saveState()
        top = PAGE_H - M - (PAGE_H - 2.05*inch - 0.35*inch - 0.85*inch) - 0.85*inch  # not used
        c.restoreState()

# simpler: draw cover text inside the band via absolute canvas coords in on_first
def on_first2(canvas, doc):
    on_first(canvas, doc)
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 23)
    canvas.drawString(M, PAGE_H - 0.95*inch, "Development Options Study")
    canvas.setFont("Helvetica", 11.5)
    canvas.setFillColor(colors.HexColor("#DCE5DC"))
    canvas.drawString(M, PAGE_H - 1.25*inch,
        "Vacant land \u2014 S Northgate Ave, Portland, Oregon 97219  \u00b7  Multnomah County tax account R547474")
    canvas.drawString(M, PAGE_H - 1.47*inch,
        "0.58 acres (25,281 sq ft) flag lot adjoining the owners' residence  \u00b7  Zoning R20, City of Portland")
    canvas.setFont("Helvetica-Bold", 9.5)
    canvas.setFillColor(colors.HexColor("#F0C89A"))
    canvas.drawString(M, PAGE_H - 1.78*inch,
        "DRAFT v1 \u2014 July 20, 2026   \u00b7   Pending: preliminary title report (disclosed non-utility easement unidentified)")
    canvas.restoreState()

doc.pageTemplates[0].onPage = on_first2

# ================= EXECUTIVE SUMMARY =================
story.append(Paragraph("Executive summary", S_H1))
story.append(P(
 "The subject property is a 0.58-acre (25,281 sq ft) vacant flag lot whose access pole fronts S Northgate Ave, "
 "directly adjoining the owners' current residence at the seam between Portland's Collins View area and unincorporated "
 "Dunthorpe. PortlandMaps confirms the parcel has been <b>annexed into the City of Portland</b> (jurisdiction "
 "\u201cPortland / Multnomah,\u201d City Council District 4) and carries a <b>clean R20 base zone</b> with no overlay "
 "letters observed. That combination is unusually favorable: Portland's Residential Infill Project rules allow far more "
 "than one house here, while the annexation replaces Multnomah County's short-term-rental prohibition with Portland's "
 "narrower accessory-STR program."))
story.append(P(
 "Four development paths are evaluated. The strongest all-around fit for the owners' stated goals \u2014 rental income "
 "plus space for visiting family \u2014 is <b>Option A: a right-sized rental house with a detached ADU</b>. "
 "<b>Option B (duplex)</b> is the best pure-yield alternative; <b>Option C (single house)</b> is the simplest, "
 "lowest-risk build; <b>Option D (consolidating the lot with the owners' existing property)</b> is the best lifestyle "
 "path and the only one with a lawful short-term-rental route. All figures are planning ranges (roughly \u00b125%) "
 "pending geotechnical work, utility quotes, and the title report."))

facts = [
    ["Location", "S Northgate Ave, Portland, OR 97219 \u2014 flag lot; pole meets the S Northgate Ave public right of way"],
    ["Tax account", "R547474 (Multnomah County). Note: aggregator sites show a sibling record, R547473 \u2014 not this parcel."],
    ["Size / shape", "0.58 acres (25,281 sq ft) per PortlandMaps; flag body sits behind neighboring rear yards"],
    ["Jurisdiction", "City of Portland (annexed) \u00b7 Council District 4 \u00b7 neighborhood area \u201cMC Unclaimed #13\u201d"],
    ["Zoning", "R20 \u2014 Residential 20,000. No c / p / z overlay letters observed; confirm on the official zoning map."],
    ["Schools", "Riverdale School District 51J (a materially positive rental-demand factor)"],
    ["Survey", "Record of Survey No. 68582, filed May 18, 2023 (Centerline Concepts Land Surveying, Inc.)"],
    ["Disclosure", "Oregon REALTORS Form 3.3 Seller's Vacant Land Disclosure, signed June 29, 2026"],
    ["Status", "Under contract; preliminary title report pending \u2014 findings to be folded into this study"],
]
tf = Table([[P(a, S_CELL_B), P(b, S_CELL)] for a, b in facts],
           colWidths=[1.25*inch, PAGE_W - 2*M - 1.25*inch])
tf.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), SAND),
    ("ROWBACKGROUNDS", (1,0), (1,-1), [colors.white, SANDLT]),
    ("GRID", (0,0), (-1,-1), 0.5, RULE),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 3.5), ("BOTTOMPADDING", (0,0), (-1,-1), 3.5),
]))
story.append(tf)

# ================= SECTION 1 =================
story.append(Paragraph("1.  Property and site", S_H1))
story.append(Paragraph("1.1  Parcel composition and the legal-lot question", S_H2))
story.append(P(
 "The 2023 Record of Survey narrative shows the parcel was assembled from several recorded pieces: Lots 2 and 3 of "
 "Block 1, \u201cWest Palatine Ridge\u201d; a portion of Block 63, \u201cPalatine Hill\u201d; Parcel 3 of Partition "
 "Plat No. 2004-35; and the vacated S Northgate Court right of way (a street vacation dating to 1947). Two implications: "
 "first, a formal <b>lot-of-record confirmation</b> should establish how many legal lots exist inside this single tax "
 "account \u2014 if more than one, the development math improves materially; second, vacated streets commonly retain "
 "public utility easements, which the title report should surface."))
story.append(Paragraph("1.2  Flag geometry", S_H2))
story.append(P(
 "The pole-and-flag shape cuts both ways. The body is private, quiet, and screened \u2014 ideal for a rental dwelling, "
 "a family ADU, or a compound. But every service (sewer lateral, water, power, gas) plus a driveway must run the length "
 "of the pole on West Hills grade: plan a <b>$40K\u2013$80K site premium</b> over a conventional lot. If finished "
 "structures sit beyond roughly 150 ft of fire-hose lay from the street, Portland generally requires an approved "
 "turnaround or residential fire sprinklers; <b>sprinklers (~$10K\u2013$18K) are usually the cheaper fix</b> and "
 "should simply be designed in. Because the body abuts neighbors' rear yards, noise- and light-sensitive uses (a sport "
 "court in particular) deserve careful siting."))
story.append(Paragraph("1.3  Utilities and services (seller disclosure, June 2026)", S_H2))
story.append(B("Not connected to any utility today; no wells, tanks, or on-site systems; no known contamination; no soil tests performed."))
story.append(B("<b>Public water:</b> system access at the boundary \u2014 yes; hook-up charge unknown (obtain a quote)."))
story.append(B("<b>Public sewer:</b> not connected, but available / able to be attached (lateral length and depth down the pole will drive cost)."))
story.append(B("<b>Electric, natural gas, telephone, internet:</b> all present at the boundary."))
story.append(B("Property lies within a fire-protection service area; no development-permit applications disclosed; no known nearby proposed changes."))
story.append(Paragraph("1.4  Topography, geology, trees, stormwater", S_H2))
story.append(P(
 "The setting implies cross-slope and a territorial outlook typical of the West Hills. Expect a <b>geotechnical "
 "report</b> to accompany any building permit; foundations, retaining, and stormwater disposal are the main cost "
 "variables. Check PortlandMaps' landslide-susceptibility and slope layers early. Portland's tree code applies at "
 "permit (preservation or density standards), and BES will require an approved on-site stormwater approach \u2014 "
 "infiltration testing determines whether drywells work or detention is needed."))

# ================= SECTION 2 =================
sec2 = []
sec2.append(Paragraph("2.  Regulatory framework \u2014 what R20 allows here", S_H1))
sec2.append(P(
 "Portland's Residential Infill Project (RIP, 2021) and RIP2 (effective June 30, 2022) extended \u201cmiddle "
 "housing\u201d and ADU allowances into the R10 and R20 zones. Applied to this parcel:"))
sec2.append(B("<b>One house by right.</b> Floor-area-ratio limits adopted with RIP2 cap total house size in R10/R20 \u2014 plan a right-sized home, not a mansion."))
sec2.append(B("<b>Duplex on any buildable R20 lot.</b> Triplex/fourplex, attached houses, and cottage clusters are allowed in certain areas \u2014 confirm map applicability with a planner."))
sec2.append(B("<b>ADUs:</b> a house with up to two ADUs, or a duplex with one ADU, where the infill options apply. ADUs are limited to 800 sq ft (or 75% of the primary unit)."))
sec2.append(B("<b>Duplex + detached ADU combo:</b> requires at least 12,000 sq ft of site in R20 (met at 25,281), frontage on a city-maintained street (verify \u2014 see \u00a76), and no constrained-sites \u201cz\u201d overlay (none observed)."))
sec2.append(B("<b>No off-street parking minimums</b> in single-dwelling zones \u2014 helpful on a flag lot."))
sec2.append(B("<b>Middle-housing land division</b> (SB 458) can put each duplex unit on its own saleable lot \u2014 but is not allowed on sites with an ADU, and on a flag lot leaves every resulting lot sharing pole-access easements with maintenance agreements. Treat it as a fallback exit, not the plan."))
sec2.append(B("<b>No conventional partition:</b> at 25,281 sq ft the site cannot be split into two standard R20 lots (40,000 sq ft required)."))
sec2.append(Paragraph("2.1  The accessory-use rule (why Option D requires consolidation)", S_H2))
sec2.append(P(
 "ADUs, workshops, sport courts and similar are <b>accessory</b> uses \u2014 they must share a lot with a primary "
 "dwelling. None can stand alone on vacant land. So the guest cottage / workshop / court program only works after "
 "either (a) building a primary dwelling on this lot, or (b) consolidating this lot with the owners' adjoining "
 "residential lot so the existing house becomes the primary dwelling."))
sec2.append(Paragraph("2.2  Short-term rental rules", S_H2))
sec2.append(P(
 "Because the parcel is annexed, Multnomah County's unincorporated-area prohibition on whole-house and ADU short-term "
 "rentals does not apply. Portland's program does: a <b>Type A accessory STR permit</b> requires the operator to occupy "
 "a dwelling on the same site roughly 270+ days per year, so a non-resident whole-home STR on a separate lot is "
 "effectively unavailable (Type B conditional use is a commercial-style review, rarely practical in R20). The workable "
 "STR route is Option D \u2014 owners residing on a consolidated site. One tradeoff: Portland's ADU fee exemption "
 "carries a roughly 10-year no-STR covenant; converting the ADU to STR triggers repayment of waived charges."))
sec2.append(Paragraph("2.3  Fees", S_H2))
sec2.append(P(
 "Plan roughly <b>$35K\u2013$60K in system development charges per new primary dwelling</b> plus permit and plan-review "
 "fees (verify current adopted schedules). ADUs are largely exempt from City SDCs with the covenant noted above."))
story.append(KeepTogether(sec2[:2]))
story.extend(sec2[2:])

# ================= SECTION 3 : OPTIONS =================
story.append(Paragraph("3.  Development options", S_H1))
story.append(P(
 "Costs are planning ranges in thousands of 2026 dollars, <b>excluding land</b>, inclusive of the flag-lot site premium "
 "and fire sprinklers where noted. \u201cGross yield\u201d adds a $500K land-basis placeholder (replace with the actual "
 "contract price) and is gross of vacancy, operating costs, and property tax."))

def cost_table(rows, total):
    data = [[P("Cost element", S_CELL_W), P("Planning range", S_CELL_W)]]
    for a, b in rows:
        data.append([P(a, S_CELL), P(b, S_CELL)])
    data.append([P("<b>Total (excl. land)</b>", S_CELL_B), P(f"<b>{total}</b>", S_CELL_B)])
    t = Table(data, colWidths=[3.6*inch, 2.1*inch], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), MOSS),
        ("BACKGROUND", (0,-1), (-1,-1), SAND),
        ("ROWBACKGROUNDS", (0,1), (-1,-2), [colors.white, SANDLT]),
        ("GRID", (0,0), (-1,-1), 0.5, RULE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    return t

def option_block(kicker, title, concept, table, income, pros, cons):
    blk = [Paragraph(kicker, S_KICKER), Paragraph(title, S_H2), P(concept), Spacer(1, 3), table, Spacer(1, 5),
           P(f"<b>Income potential:</b> {income}")]
    blk.append(P("<b>Advantages</b>", S_CELL_B))
    for x in pros: blk.append(B(x))
    blk.append(P("<b>Watch-outs</b>", S_CELL_B))
    for x in cons: blk.append(B(x))
    return blk

# --- Option A
optA = option_block(
 "OPTION A \u2014 RECOMMENDED BASELINE",
 "Rental house + detached ADU",
 "A right-sized single-family rental of about 2,400 sq ft in the flag body, paired with an 800 sq ft detached ADU. "
 "The house leases long-term; the ADU serves visiting family and can lease long-term when idle. Best overall match to "
 "the owners' stated goals.",
 cost_table([
    ("Site work / flag premium (driveway, utility runs)", "$40 \u2013 $80"),
    ("House, ~2,400 sq ft hard cost ($420\u2013$500/sq ft)", "$1,000 \u2013 $1,200"),
    ("Detached ADU, 800 sq ft, all-in (City SDC-exempt with covenant)", "$250 \u2013 $330"),
    ("SDCs + permits (house)", "$45 \u2013 $75"),
    ("Fire sprinklers (13D, both structures)", "$12 \u2013 $18"),
 ], "~$1.35M \u2013 $1.70M"),
 "house $4,800\u2013$5,800/mo; ADU $2,000\u2013$2,400/mo when leased \u2014 up to $6,800\u2013$8,200/mo combined. "
 "Approximate gross yield with land: 4\u20135% (both units leased).",
 ["Delivers income and dedicated family space simultaneously; occupancy can flex over time (owners could later occupy either unit).",
  "ADU rides the City SDC exemption; small units lease quickly given Riverdale schools and Lewis & Clark demand.",
  "Single-lot, by-right permitting path (no land-use review expected if standards are met)."],
 ["Two structures on a sloped flag = the most site work of the separate-lot paths.",
  "An ADU on site forecloses a future middle-housing land division; the SDC covenant bars ADU short-term rental for ~10 years.",
  "FAR caps limit total building size \u2014 confirm the program fits early in design."])
story.append(KeepTogether(optA))

# --- Option B
optB = option_block(
 "OPTION B \u2014 BEST PURE YIELD",
 "Duplex (hold both units)",
 "A single structure of about 3,000 sq ft containing two ~1,500 sq ft units. One foundation and one roof suit a sloped "
 "site; two mid-size units out-earn one large house in this sub-market.",
 cost_table([
    ("Site work / flag premium", "$40 \u2013 $80"),
    ("Duplex, ~3,000 sq ft hard cost ($385\u2013$435/sq ft)", "$1,150 \u2013 $1,300"),
    ("SDCs + permits (two units)", "$80 \u2013 $120"),
    ("Fire sprinklers (13D)", "$12 \u2013 $18"),
 ], "~$1.30M \u2013 $1.50M"),
 "$3,000\u2013$3,600 per unit = $6,000\u2013$7,200/mo gross. Approximate gross yield with land: 4\u20134.5%+ \u2014 "
 "the strongest cash-on-cost of the four paths.",
 ["Best income per dollar; two smaller units carry lower vacancy risk than one large home.",
  "Duplexes are allowed on every buildable R20 lot \u2014 no special review.",
  "Option value: the site also meets the 12,000 sq ft threshold to add a detached ADU later (needs city-maintained frontage; adding it would bar unit division)."],
 ["A duplex product in an estate-scale pocket \u2014 invest in design so it reads as one house.",
  "Unit-by-unit division for separate sale is possible only with no ADU on site, and on this flag it leaves all lots sharing pole easements \u2014 workable but clunky; treat as fallback exit.",
  "Appraisal and financing comps for duplexes are thinner in this neighborhood."])
story.append(KeepTogether(optB))

# --- Option C
optC = option_block(
 "OPTION C \u2014 SIMPLEST BUILD",
 "Single rental house",
 "One ~2,400 sq ft house; the simplest permit path, cleanest resale story, and the least to manage. Preserves options: "
 "an ADU can be added later, and no entitlement doors close.",
 cost_table([
    ("Site work / flag premium", "$40 \u2013 $80"),
    ("House, ~2,400 sq ft hard cost", "$1,000 \u2013 $1,200"),
    ("SDCs + permits", "$45 \u2013 $75"),
    ("Fire sprinklers (13D)", "$8 \u2013 $14"),
 ], "~$1.10M \u2013 $1.35M"),
 "$4,800\u2013$5,800/mo. Approximate gross yield with land: 3\u20134% \u2014 honest framing: this is a "
 "wealth-storage / Riverdale-scarcity appreciation play more than a cash-flow play.",
 ["Lowest execution risk and management burden; broadest resale market (single-family).",
  "Keeps every future option open \u2014 add an ADU later, or owners occupy it themselves someday."],
 ["Weakest income relative to capital deployed; leaves R20 entitlement value on the table.",
  "Same flag-lot site premium as richer programs, spread over less income."])
story.append(KeepTogether(optC))

# --- Option D
optD = option_block(
 "OPTION D \u2014 LIFESTYLE PATH (AND THE ONLY LAWFUL STR ROUTE)",
 "Consolidate with the owners' lot: ADU + workshop + sport court",
 "Consolidate this lot with the owners' adjoining property (a property-line adjustment / lot consolidation through the "
 "City), making everything new <b>accessory to the existing residence</b>: a detached ADU (the \u201ctiny home\u201d for "
 "visiting family), a workshop \u2014 optionally with a studio above serving as the ADU \u2014 and a sport court in the "
 "screened flag body. Fully phase-able; build elements as budget allows. Daily access may even come from the owners' "
 "side, trimming pole costs.",
 cost_table([
    ("Detached ADU, 800 sq ft (family suite / long-term rental / permitted STR)", "$250 \u2013 $350"),
    ("Workshop with studio above (combined, if studio serves as the ADU)", "$450 \u2013 $600"),
    ("Sport court, incl. hillside grading/retaining (unlit simplest)", "$60 \u2013 $120"),
    ("Utility extensions / shared site work (scope-dependent)", "$30 \u2013 $60"),
 ], "~$0.8M \u2013 $1.1M full scope (elements can stand alone)"),
 "ADU $2,000\u2013$2,400/mo long-term \u2014 or short-term rental under a Type A permit, since the owners reside on the "
 "consolidated site (STR use forfeits/repays the ADU SDC exemption). Lowest income ceiling of the four paths; highest "
 "lifestyle value.",
 ["Delivers the full family wish list \u2014 guest quarters, workshop, court \u2014 on the most private part of the site.",
  "Only path with a lawful short-term-rental option; spending can be phased element by element.",
  "If the owners' existing lot adjoins the flag body, access and utilities may run from their side rather than down the pole."],
 ["Forfeits the separate lot's standalone value, independent financing, and future independent sale.",
  "Consolidation is hard to reverse \u2014 re-dividing later must meet R20 partition standards, which the combined area may not support. Check before consolidating.",
  "Sport-court siting abuts neighbors' rear yards: mind noise, setbacks, and lighting/glare standards (an unlit court is simplest)."])
story.append(KeepTogether(optD))

story.append(Paragraph("3.1  Program variants worth knowing", S_H2))
story.append(B("<b>The \u201ctiny home.\u201d</b> Delivered best as the ADU (a full dwelling), or \u2014 cheaper \u2014 as a no-kitchen guest studio treated as a plain accessory structure: no SDCs and lighter permitting, but it is not a dwelling and cannot be rented separately."))
story.append(B("<b>Two ADUs.</b> Where the infill options apply, a house may carry two ADUs \u2014 e.g., a garden cottage for family plus a studio over the workshop. Confirm applicability with a planner before counting on it."))

# ================= SECTION 4 : COMPARISON =================
sec4 = [Paragraph("4.  Side-by-side comparison", S_H1)]
cmp_head = [P("", S_CELL_W), P("A \u2014 House + ADU", S_CELL_W), P("B \u2014 Duplex", S_CELL_W),
            P("C \u2014 House only", S_CELL_W), P("D \u2014 Consolidation", S_CELL_W)]
cmp_rows = [
 ("Cost, excl. land", "$1.35\u2013$1.70M", "$1.30\u2013$1.50M", "$1.10\u2013$1.35M", "$0.8\u2013$1.1M full scope"),
 ("Gross income /mo", "$6,800\u2013$8,200 (both leased)", "$6,000\u2013$7,200", "$4,800\u2013$5,800", "$2,000\u2013$2,400 (ADU)"),
 ("Approx. gross yield*", "4\u20135%", "4\u20134.5%+", "3\u20134%", "~2% \u2014 lifestyle-weighted"),
 ("Short-term rental", "No (no on-site resident)", "No (no on-site resident)", "No (no on-site resident)", "Yes \u2014 Type A permit; ADU covenant tradeoff"),
 ("Family guest space", "Yes \u2014 the ADU", "Possible (hold a unit open)", "No (until ADU added)", "Yes \u2014 the ADU"),
 ("Keeps lot separately saleable", "Yes", "Yes (unit division = clunky fallback)", "Yes", "No \u2014 consolidated"),
 ("Key constraint", "ADU blocks unit division; most site work", "Design fit in estate pocket", "Weakest yield", "Hard to reverse; court noise siting"),
 ("Best for", "Income + family space together", "Maximum cash flow", "Simplicity, appreciation", "Lifestyle, phased budget, STR"),
]
cmp_data = [cmp_head] + [[P(r[0], S_CELL_B)] + [P(x, S_CELL) for x in r[1:]] for r in cmp_rows]
w0 = 1.35*inch; wc = (PAGE_W - 2*M - w0) / 4.0
tc = Table(cmp_data, colWidths=[w0, wc, wc, wc, wc], repeatRows=1)
tc.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), FOREST),
    ("BACKGROUND", (0,1), (0,-1), SAND),
    ("ROWBACKGROUNDS", (1,1), (-1,-1), [colors.white, SANDLT]),
    ("GRID", (0,0), (-1,-1), 0.5, RULE),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 3.5), ("BOTTOMPADDING", (0,0), (-1,-1), 3.5),
]))
sec4.append(tc)
sec4.append(Spacer(1, 3))
sec4.append(P("*Gross yield adds a $500K land-basis placeholder and is gross of vacancy, operating costs, and City of "
              "Portland property tax \u2014 net yields run materially lower. Replace with actual contract economics.", S_SMALL))
story.append(KeepTogether(sec4))

# ================= SECTION 5 : ASSUMPTIONS =================
story.append(Paragraph("5.  Financial assumptions and method", S_H1))
story.append(B("Construction costs are July 2026 planning ranges for custom West Hills work: houses ~$420\u2013$500/sq ft hard cost; duplex ~$385\u2013$435/sq ft; ADUs ~$310\u2013$420/sq ft all-in. Treat every figure as \u00b125% until geotech, concept design, and contractor pricing exist."))
story.append(B("Land basis is a $500K placeholder drawn from prior-cycle area land listings \u2014 substitute the actual contract price."))
story.append(B("Rents are scaled from area comparables and platform estimates ($4,800\u2013$7,900/mo for larger Riverdale-district homes) with small-unit demand supported by Lewis & Clark College proximity. Figures are gross \u2014 no vacancy, management, maintenance, insurance, or property-tax deductions."))
story.append(B("SDC and permit allowances are planning figures; the City's adopted fee schedules govern and change annually each July."))

# ================= SECTION 6 : RISK REGISTER =================
sec6 = [Paragraph("6.  Risk and diligence register", S_H1)]
reg = [
 ("Preliminary title report", "Seller discloses easements beyond utility/drainage \u2014 instrument unidentified. Also surfaces any Palatine Hill / West Palatine Ridge plat CC&Rs; private deed restrictions can prohibit what zoning allows.", "PENDING \u2014 order via escrow now; attorney review of any easement burdening the pole or body"),
 ("Legal-lot / lot-of-record confirmation", "Parcel assembled from multiple plat pieces plus a 1947 street vacation; more than one legal lot would upgrade every option.", "Open \u2014 title officer + City lot-confirmation process"),
 ("City-maintained street check", "Code precondition for the duplex + detached ADU combination at this frontage.", "Open \u2014 PortlandMaps street layer / PBOT"),
 ("Official overlay confirmation", "Verify no c / p / z overlays and whether infill options (\u201ca\u201d) apply as assumed.", "Open \u2014 free 15-minute planner appointment or Early Assistance"),
 ("Geotechnical reconnaissance", "West Hills slope and soils drive foundation, retaining, and stormwater budgets.", "Open \u2014 commission recon before concept design"),
 ("Utility quotes", "Sewer lateral route/depth down the pole; water hook-up charge disclosed as unknown; power/gas service runs.", "Open \u2014 BES, Water Bureau, franchise utilities"),
 ("Stormwater infiltration testing", "Determines drywell feasibility vs. detention \u2014 sets civil design.", "Open"),
 ("Tree survey", "Preservation / density standards apply at permit.", "Open"),
 ("Fire access determination", "Hose-lay distance drives turnaround vs. 13D sprinklers; assume sprinklers.", "Open \u2014 confirm at Early Assistance"),
 ("Boundary staking", "Disclosure marks boundary marking \u201cunknown\u201d; 2023 survey set monuments \u2014 locate pins on the ground.", "Open"),
 ("Contract economics", "Insert actual land price, financing terms, and tax estimates into the model.", "Open"),
]
rt = Table([[P("Item", S_CELL_W), P("Why it matters", S_CELL_W), P("Status / next action", S_CELL_W)]] +
           [[P(a, S_CELL_B), P(b, S_CELL), P(c, S_CELL)] for a, b, c in reg],
           colWidths=[1.55*inch, 3.35*inch, 1.95*inch], repeatRows=1)
rt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), FOREST),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, SANDLT]),
    ("GRID", (0,0), (-1,-1), 0.5, RULE),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 3.5), ("BOTTOMPADDING", (0,0), (-1,-1), 3.5),
]))
sec6.append(rt)
story.append(KeepTogether(sec6))

# ================= SECTION 7 : SEQUENCE =================
story.append(Paragraph("7.  Suggested sequence", S_H1))
story.append(B("<b>Now, pre-closing:</b> obtain the preliminary title report and the disclosed easement instrument; pose the legal-lot question to the title officer; book the free 15-minute City planner conversation (overlays, street-maintenance status, infill-option applicability); walk the 2023 survey pins."))
story.append(B("<b>0\u201360 days after closing:</b> geotechnical reconnaissance; utility connection quotes; decide the fork \u2014 separate-lot income build (A/B/C) versus consolidation compound (D). The fork decision precedes design."))
story.append(B("<b>60\u2013180 days:</b> concept design and contractor budget pricing on the chosen path; refine the pro forma with actual land, fee, and financing numbers; submit for permits."))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=0.8, color=RULE))
story.append(Spacer(1, 4))
story.append(P("This study is a planning-level synthesis prepared for the owners' internal decision-making. It is not "
 "legal, tax, investment, engineering, or brokerage advice, and no figure herein is a bid, appraisal, or code "
 "determination. Zoning interpretations, fee schedules, and market figures change; verify every material item with the "
 "City of Portland, licensed design professionals, and contractors before committing funds. Prepared July 20, 2026; to "
 "be revised on receipt of the preliminary title report.", S_SMALL))

doc.build(story)
print("report built")
