"""
app.py — 180DC ESCP Executive Financial Dashboard
Fall Semester 2026
"""

import base64
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
from data_loader import load_model, MONTHS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="180DC ESCP | Financial Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Logo loader ───────────────────────────────────────────────────────────────
ASSETS = Path(__file__).parent / "assets"

def img_b64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_180dc = img_b64(ASSETS / "logo_180dc.png")
logo_escp  = img_b64(ASSETS / "logo_escp.png")

# ── Design tokens ─────────────────────────────────────────────────────────────
# Primary: 180DC green  |  Secondary: ESCP purple  |  Base: near-black
GREEN_DARK   = "#1A5C25"
GREEN_MID    = "#2E8B3A"
GREEN_LIGHT  = "#4CAF50"
GREEN_PALE   = "#D6E4D8"
PURPLE       = "#3D2785"
PURPLE_LIGHT = "#6B57C0"
PURPLE_PALE  = "#E8E4F5"
BLACK        = "#0A0A0A"
DARK         = "#111827"
DARK_CARD    = "#1A1F2E"
SILVER       = "#C8D0D8"
PALE         = "#F2F4F7"
WHITE        = "#FFFFFF"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* ── Base ── */
  [data-testid="stAppViewContainer"] {{
    background: {DARK};
  }}
  [data-testid="stHeader"] {{ background: transparent; }}
  .block-container {{ padding: 0 2rem 2rem 2rem; }}

  /* ── Hero header ── */
  .hero {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: {BLACK};
    border-bottom: 2px solid {GREEN_MID};
    padding: 0.6rem 1.5rem;
    margin-bottom: 1.2rem;
    border-radius: 0 0 6px 6px;
  }}
  .hero-logos {{
    display: flex;
    align-items: center;
    gap: 1rem;
  }}
  .hero-logo-180dc {{
    height: 52px;
    width: auto;
  }}
  .hero-divider {{
    width: 1px;
    height: 40px;
    background: #333;
  }}
  .hero-logo-escp {{
    height: 44px;
    width: auto;
  }}
  .hero-title {{
    text-align: center;
    flex: 1;
    padding: 0 1rem;
  }}
  .hero-title-main {{
    font-size: 1.05rem;
    font-weight: 700;
    color: {WHITE};
    letter-spacing: 0.04em;
  }}
  .hero-title-sub {{
    font-size: 0.72rem;
    color: #8FA8C8;
    margin-top: 0.1rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }}
  .hero-meta {{
    text-align: right;
    font-size: 0.68rem;
    color: #556;
    line-height: 1.5;
  }}
  .hero-meta span {{
    display: block;
    color: {GREEN_LIGHT};
    font-weight: 600;
  }}

  /* ── KPI cards ── */
  .card {{
    background: {DARK_CARD};
    border: 1px solid #252D3D;
    border-top: 3px solid {GREEN_MID};
    border-radius: 6px;
    padding: 1rem 1.2rem 0.9rem;
    text-align: center;
  }}
  .card-label {{
    font-size: 0.65rem;
    font-weight: 700;
    color: #8FA8C8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
  }}
  .card-value {{
    font-size: 1.6rem;
    font-weight: 700;
    line-height: 1.1;
  }}
  .card-sub {{
    font-size: 0.68rem;
    color: #556;
    margin-top: 0.3rem;
  }}

  /* ── Section headers ── */
  .section-hdr {{
    font-size: 0.68rem;
    font-weight: 700;
    color: {GREEN_LIGHT};
    border-left: 3px solid {GREEN_LIGHT};
    padding: 0.15rem 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.55rem;
    margin-top: 0.1rem;
    background: rgba(46,139,58,0.08);
    border-radius: 0 3px 3px 0;
  }}

  /* ── KPI table ── */
  .kpi-grid {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.855rem;
  }}
  .kpi-grid th {{
    background: {BLACK};
    color: {GREEN_LIGHT};
    font-weight: 600;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 0.55rem 0.85rem;
    text-align: left;
    border-bottom: 1px solid {GREEN_DARK};
  }}
  .kpi-grid td {{
    padding: 0.5rem 0.85rem;
    border-bottom: 1px solid #1A2030;
    color: {WHITE};
    vertical-align: middle;
  }}
  .kpi-grid tr:nth-child(even) td {{ background: rgba(255,255,255,0.02); }}
  .kpi-grid tr:nth-child(odd)  td {{ background: transparent; }}
  .kpi-grid tr:hover td {{ background: rgba(46,139,58,0.06); }}

  /* ── RAG badges ── */
  .badge {{
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 3px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.03em;
  }}
  .badge-green   {{ background: rgba(26,92,37,0.35);  color: #6FCF7A; border: 1px solid #2E8B3A; }}
  .badge-amber   {{ background: rgba(122,82,0,0.30);  color: #F5C842; border: 1px solid #7A5200; }}
  .badge-red     {{ background: rgba(139,26,26,0.30); color: #F47070; border: 1px solid #8B1A1A; }}
  .badge-neutral {{ background: rgba(200,208,216,0.1);color: #8FA8C8; border: 1px solid #333; }}

  /* ── Expander ── */
  [data-testid="stExpander"] {{
    background: {DARK_CARD};
    border: 1px solid #252D3D;
    border-radius: 6px;
  }}
  [data-testid="stExpander"] summary {{
    color: {GREEN_LIGHT} !important;
    font-size: 0.82rem;
    font-weight: 600;
  }}

  /* ── Metric widget ── */
  [data-testid="stMetric"] {{
    background: {DARK_CARD};
    border: 1px solid #252D3D;
    border-radius: 6px;
    padding: 0.75rem 1rem;
  }}
  [data-testid="stMetricLabel"] p  {{ color: #8FA8C8 !important; font-size: 0.72rem !important; }}
  [data-testid="stMetricValue"]    {{ color: {WHITE} !important; }}

  /* ── Footer ── */
  .footer {{
    text-align: right;
    font-size: 0.68rem;
    color: #444;
    margin-top: 1.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #1A2030;
  }}
  .footer span {{ color: {GREEN_DARK}; }}
</style>
""", unsafe_allow_html=True)

# ── Colours (Python-side for Plotly) ─────────────────────────────────────────
P_GREEN  = "#4CAF50"
P_GREEN2 = "#2E8B3A"
P_PURPLE = "#6B57C0"
P_GOLD   = "#B8922A"
P_DARK   = "#111827"
P_SILVER = "#8FA8C8"
P_WHITE  = "#E8ECF5"
P_PALE   = "#1A2030"
P_RED    = "#F47070"

CHART_FONT   = dict(family="'Helvetica Neue', Arial, sans-serif", size=11, color=P_WHITE)
CHART_LAYOUT = dict(
    plot_bgcolor=P_DARK, paper_bgcolor=P_DARK, font=CHART_FONT,
    margin=dict(l=10, r=10, t=24, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=10, color=P_WHITE)),
    xaxis=dict(color=P_SILVER, gridcolor="#1A2030", linecolor="#252D3D"),
    yaxis=dict(color=P_SILVER, gridcolor="#1A2030", linecolor="#252D3D",
               zeroline=True, zerolinecolor="#333"),
)

# ── Formatters ────────────────────────────────────────────────────────────────
def fmt_eur(v) -> str:
    if v is None: return "—"
    v = float(v)
    return f"(€{abs(v):,.0f})" if v < 0 else f"€{v:,.0f}"

def fmt_pct(v) -> str:
    if v is None: return "—"
    return f"{float(v) * 100:.1f}%"

def fmt_value(v, fmt: str) -> str:
    return fmt_pct(v) if fmt == "pct" else fmt_eur(v)

def badge(status: str) -> str:
    s = str(status).strip()
    css = {
        "On Target": "badge-green", "Surplus": "badge-green", "Healthy": "badge-green",
        "Below Target": "badge-amber", "Above Target": "badge-amber",
        "Review Mix": "badge-amber", "Overspend": "badge-amber",
        "Deficit": "badge-red",
    }.get(s, "badge-neutral")
    return f'<span class="badge {css}">{s}</span>'

# ── Load data ─────────────────────────────────────────────────────────────────
try:
    data = load_model()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

pl   = data["pl"]
asmp = data["assumptions"]
kpis = data["kpis"]

total_rev  = pl["total_revenue"]["total"]
total_cost = pl["total_costs"]["total"]
net_sur    = pl["net_surplus"]["total"]
net_mar    = net_sur / total_rev if total_rev else 0

rev_monthly  = pl["total_revenue"]["monthly"]
cost_monthly = pl["total_costs"]["monthly"]
sur_monthly  = pl["monthly_surplus"]["monthly"]
cum_monthly  = pl["cumulative_surplus"]["monthly"]

# ── Hero Header with logos ────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="hero">
      <div class="hero-logos">
        <img class="hero-logo-180dc"
             src="data:image/png;base64,{logo_180dc}"
             alt="180 Degrees Consulting" />
        <div class="hero-divider"></div>
        <img class="hero-logo-escp"
             src="data:image/png;base64,{logo_escp}"
             alt="ESCP Business School" />
      </div>

      <div class="hero-title">
        <div class="hero-title-main">Executive Financial Dashboard</div>
        <div class="hero-title-sub">Fall Semester 2026 &nbsp;·&nbsp; Pro-bono / Symbolic-Fee Model</div>
      </div>

      <div class="hero-meta">
        <span>Live data from Excel model</span>
        Finance Position — Case Study
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
surplus_color = P_GREEN  if net_sur > 0                                    else P_RED
margin_color  = P_GREEN  if net_mar >= asmp.get("target_margin", 0.05)    else "#F5C842"

c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    (c1, "Total Revenue",   fmt_eur(total_rev),  "Full semester",       P_GREEN),
    (c2, "Total Costs",     fmt_eur(total_cost), "Full semester",       P_SILVER),
    (c3, "Net Surplus",     fmt_eur(net_sur),    "Revenue minus costs", surplus_color),
    (c4, "Net Margin",      fmt_pct(net_mar),    "Surplus / Revenue",   margin_color),
    (c5, "Active Members",  str(int(asmp.get("active_members", 0))),
                            f"{int(asmp.get('projects', 0))} projects", P_SILVER),
]
for col, label, value, sub, color in cards:
    col.markdown(
        f'<div class="card">'
        f'<div class="card-label">{label}</div>'
        f'<div class="card-value" style="color:{color};">{value}</div>'
        f'<div class="card-sub">{sub}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:.9rem'></div>", unsafe_allow_html=True)

# ── Row 1: Revenue vs Costs | Revenue Mix ─────────────────────────────────────
col_l, col_r = st.columns([3, 2], gap="medium")

with col_l:
    st.markdown('<div class="section-hdr">Monthly Revenue vs. Costs</div>',
                unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_bar(
        name="Revenue", x=MONTHS, y=rev_monthly,
        marker_color=P_GREEN2,
        marker_line=dict(color=P_GREEN, width=1),
        text=[fmt_eur(v) for v in rev_monthly],
        textposition="outside", textfont=dict(size=10, color=P_WHITE),
    )
    fig.add_bar(
        name="Costs", x=MONTHS, y=cost_monthly,
        marker_color="#2A3550",
        marker_line=dict(color=P_SILVER, width=1),
        text=[fmt_eur(v) for v in cost_monthly],
        textposition="outside", textfont=dict(size=10, color=P_SILVER),
    )
    fig.add_scatter(
        name="Net Surplus", x=MONTHS, y=sur_monthly,
        mode="lines+markers",
        line=dict(color=P_GREEN, width=2.5, dash="solid"),
        marker=dict(size=8, color=P_GREEN,
                    line=dict(color=P_DARK, width=2)),
    )
    fig.update_layout(**CHART_LAYOUT, barmode="group", height=295,
                      yaxis_tickprefix="€")
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.markdown('<div class="section-hdr">Revenue Mix</div>',
                unsafe_allow_html=True)
    fig2 = go.Figure(go.Pie(
        labels=["Symbolic Project Fees", "Corporate Sponsorships",
                "ESCP Institutional Grant", "Membership Fees", "Events & Other"],
        values=[
            pl["project_fees"]["total"],  pl["sponsorship"]["total"],
            pl["escp_grant"]["total"],    pl["membership"]["total"],
            pl["event_revenue"]["total"] + pl["other_revenue"]["total"],
        ],
        hole=0.52,
        marker_colors=[P_GREEN, P_GREEN2, P_PURPLE, P_GOLD, "#334"],
        textinfo="percent", textfont=dict(size=10, color=P_WHITE),
        hovertemplate="%{label}<br>%{value:€,.0f}<br>%{percent}<extra></extra>",
    ))
    fig2.update_layout(
        **CHART_LAYOUT, height=295,
        showlegend=True,
        legend=dict(orientation="v", x=1.02, y=0.5, font=dict(size=9),
                    bgcolor="rgba(0,0,0,0)"),
        annotations=[dict(text="Revenue<br>Mix", x=0.5, y=0.5,
                          font=dict(size=11, color=P_SILVER), showarrow=False)],
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Cumulative Position | Cost Structure ────────────────────────────────
col_a, col_b = st.columns([3, 2], gap="medium")

with col_a:
    st.markdown('<div class="section-hdr">Cumulative Net Position</div>',
                unsafe_allow_html=True)
    fig3 = go.Figure()
    fig3.add_scatter(
        x=MONTHS, y=cum_monthly,
        mode="lines+markers+text",
        line=dict(color=P_GREEN, width=2.5),
        marker=dict(size=10, color=P_DARK,
                    line=dict(color=P_GREEN, width=2.5)),
        text=[fmt_eur(v) for v in cum_monthly],
        textposition="top center",
        textfont=dict(size=10, color=P_GREEN),
        fill="tozeroy",
        fillcolor="rgba(46,139,58,0.10)",
        name="Cumulative surplus",
    )
    fig3.add_hline(y=0, line_dash="dot", line_color="#F47070", line_width=1.2)
    fig3.update_layout(**CHART_LAYOUT, height=215, showlegend=False,
                       yaxis_tickprefix="€")
    st.plotly_chart(fig3, use_container_width=True)

with col_b:
    st.markdown('<div class="section-hdr">Cost Structure</div>',
                unsafe_allow_html=True)
    fig4 = go.Figure(go.Pie(
        labels=["Events", "Project Delivery", "Travel",
                "Marketing", "Software", "Admin", "Contingency"],
        values=[pl["events_cost"]["total"], pl["proj_delivery"]["total"],
                pl["travel"]["total"],      pl["marketing"]["total"],
                pl["software"]["total"],    pl["admin"]["total"],
                pl["contingency"]["total"]],
        hole=0.52,
        marker_colors=[P_PURPLE, P_GREEN2, "#334", P_GOLD,
                       P_GREEN, P_SILVER, "#445"],
        textinfo="percent", textfont=dict(size=10, color=P_WHITE),
        hovertemplate="%{label}<br>%{value:€,.0f}<br>%{percent}<extra></extra>",
    ))
    fig4.update_layout(
        **CHART_LAYOUT, height=215,
        showlegend=True,
        legend=dict(orientation="v", x=1.02, y=0.5, font=dict(size=9),
                    bgcolor="rgba(0,0,0,0)"),
        annotations=[dict(text="Cost<br>Split", x=0.5, y=0.5,
                          font=dict(size=11, color=P_SILVER), showarrow=False)],
    )
    st.plotly_chart(fig4, use_container_width=True)

# ── KPI Table ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr">KPI Status</div>', unsafe_allow_html=True)

rows_html = "".join(
    f"<tr><td><strong>{k['name']}</strong></td>"
    f"<td style='text-align:right;font-variant-numeric:tabular-nums;"
    f"font-family:monospace;color:#BDD7EE;'>"
    f"{fmt_value(k['value'], k['format'])}</td>"
    f"<td style='color:#8FA8C8;font-size:.82rem;'>{k['target']}</td>"
    f"<td>{badge(k['status'])}</td></tr>"
    for k in kpis
)
st.markdown(
    f"<table class='kpi-grid'><thead><tr>"
    f"<th style='width:42%'>KPI</th>"
    f"<th style='width:16%;text-align:right'>Value</th>"
    f"<th style='width:18%'>Target</th>"
    f"<th style='width:24%'>Status</th>"
    f"</tr></thead><tbody>{rows_html}</tbody></table>",
    unsafe_allow_html=True,
)

st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

# ── Monthly Detail ────────────────────────────────────────────────────────────
with st.expander("Monthly P&L Breakdown", expanded=False):
    lines = [
        ("1.1  Symbolic Project Contributions", "project_fees",  "eur"),
        ("1.2  Corporate Sponsorships",         "sponsorship",   "eur"),
        ("1.3  ESCP Institutional Grant",       "escp_grant",    "eur"),
        ("1.4  Membership Fees",                "membership",    "eur"),
        ("1.5  Event / Workshop Revenue",       "event_revenue", "eur"),
        ("1.6  Other / Miscellaneous",          "other_revenue", "eur"),
        ("TOTAL REVENUE",                       "total_revenue", "eur"),
        ("2.1  Events & Activities",            "events_cost",   "eur"),
        ("2.2  Project Delivery",               "proj_delivery", "eur"),
        ("2.3  Travel & Client Meetings",       "travel",        "eur"),
        ("2.4  Marketing & Communications",     "marketing",     "eur"),
        ("2.5  Software & Digital Tools",       "software",      "eur"),
        ("2.6  Admin & Miscellaneous",          "admin",         "eur"),
        ("2.7  Contingency Reserve",            "contingency",   "eur"),
        ("TOTAL COSTS",                         "total_costs",   "eur"),
        ("Gross Surplus / (Deficit)",           "net_surplus",   "eur"),
        ("Net Margin (%)",                      "net_margin",    "pct"),
    ]
    totals   = {"TOTAL REVENUE", "TOTAL COSTS", "Gross Surplus / (Deficit)"}
    dividers = {"2.1  Events & Activities", "Gross Surplus / (Deficit)"}

    hdr = (
        "<table class='kpi-grid' style='font-size:.80rem'><thead><tr>"
        "<th style='width:36%;text-align:left'>Line Item</th>"
        + "".join(f"<th style='text-align:right'>{m[:3]}</th>" for m in MONTHS)
        + f"<th style='text-align:right;color:{P_GOLD};'>Total</th>"
        "</tr></thead><tbody>"
    )
    body = ""
    for label, key, fmt in lines:
        is_tot = label in totals
        b_top  = "border-top:1px solid #2E8B3A;" if label in dividers else ""
        b_st   = "font-weight:700;" if is_tot else ""
        r_st   = "background:rgba(46,139,58,0.08);" if is_tot else ""
        cells  = "".join(
            f"<td style='text-align:right;font-family:monospace;{b_st}{r_st}'>"
            f"{fmt_value(v, fmt)}</td>"
            for v in pl[key]["monthly"]
        )
        body += (
            f"<tr style='{b_top}'>"
            f"<td style='{b_st}{r_st}'>{label}</td>{cells}"
            f"<td style='text-align:right;font-weight:700;font-family:monospace;"
            f"color:{P_GREEN};{r_st}'>{fmt_value(pl[key]['total'], fmt)}</td>"
            f"</tr>"
        )
    st.markdown(hdr + body + "</tbody></table>", unsafe_allow_html=True)

# ── Assumptions Panel ─────────────────────────────────────────────────────────
with st.expander("Model Assumptions", expanded=False):
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Total Members",       int(asmp.get("total_members", 0)))
    a1.metric("Active Consultants",  int(asmp.get("active_members", 0)))
    a2.metric("Campuses",            int(asmp.get("campuses", 0)))
    a2.metric("Projects / Semester", int(asmp.get("projects", 0)))
    a3.metric("Symbolic Fee / Proj.",fmt_eur(asmp.get("symbolic_fee", 0)))
    a3.metric("Contribution Rate",   fmt_pct(asmp.get("contribution_rate", 0)))
    a4.metric("Sponsorship Revenue", fmt_eur(asmp.get("sponsorship_revenue", 0)))
    a4.metric("ESCP Grant",          fmt_eur(asmp.get("escp_grant", 0)))
    st.caption(
        "Edit blue cells in the Assumptions sheet of the Excel model to update all values."
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='footer'>180 Degrees Consulting ESCP &nbsp;·&nbsp; "
    "Financial Model Fall 2026 &nbsp;·&nbsp; "
    "<span>Pro-bono / symbolic-fee model</span> &nbsp;·&nbsp; v3</div>",
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════════════════════
# EXTENDED SECTIONS  (added with v4 Excel model)
# ═══════════════════════════════════════════════════════════════════════════════
from data_loader import load_projects, load_scenarios, load_variance

try:
    projects  = load_projects()
    scenarios = load_scenarios()
    variance  = load_variance()
    has_ext   = True
except Exception:
    has_ext   = False

if has_ext:

    # ── Project Pipeline ─────────────────────────────────────────────────────
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-hdr">Project Pipeline — Fall 2026</div>',
                unsafe_allow_html=True)

    STATUS_STYLE = {
        "Completed":    ("#D6E4D8","#1A5C25","2E8B3A"),
        "Active":       ("#DBEAFE","#1E3A8A","2E5EAE"),
        "Under Review": ("#FDF2D0","#7A5200","B8922A"),
        "Scoping":      ("#F3F4F6","#374151","8F9BB3"),
        "On Hold":      ("#F5D5D5","#8B1A1A","CC3333"),
    }

    proj_cols = st.columns(4)
    for i, proj in enumerate(projects):
        status = str(proj.get("status") or "Scoping")
        bg, fg, border = STATUS_STYLE.get(status, ("#F3F4F6","#374151","8F9BB3"))
        hrs_b = proj.get("hrs_budget") or 1
        hrs_a = proj.get("hrs_actual") or 0
        pct   = min(hrs_a / hrs_b, 1.0) if hrs_b else 0
        fee   = proj.get("fee") or 0
        rcvd  = proj.get("received") or 0
        inv   = proj.get("invoiced") or "No"

        proj_cols[i % 4].markdown(
            f'<div style="background:{bg};border:1px solid #{border};border-radius:5px;'
            f'padding:.7rem .85rem .6rem;margin-bottom:.6rem;">'
            f'<div style="font-size:.65rem;font-weight:700;color:#{border};'
            f'text-transform:uppercase;letter-spacing:.08em;">{status}</div>'
            f'<div style="font-size:.92rem;font-weight:700;color:{fg};margin:.2rem 0 .1rem;">'
            f'{proj.get("client","—")}</div>'
            f'<div style="font-size:.72rem;color:{fg};opacity:.7;margin-bottom:.4rem;">'
            f'{proj.get("sector","")}</div>'
            f'<div style="background:#DDD;border-radius:3px;height:4px;margin-bottom:.35rem;">'
            f'<div style="background:#{border};width:{pct*100:.0f}%;height:4px;border-radius:3px;"></div>'
            f'</div>'
            f'<div style="display:flex;justify-content:space-between;font-size:.68rem;color:{fg};">'
            f'<span>{hrs_a} / {hrs_b} hrs</span>'
            f'<span>{"€"+str(int(rcvd)) if fee>0 else "Pro-bono"}</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    # ── Scenario Comparison ──────────────────────────────────────────────────
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    col_sc, col_var = st.columns([1, 1], gap="medium")

    with col_sc:
        st.markdown('<div class="section-hdr">Scenario Comparison</div>',
                    unsafe_allow_html=True)

        sc_labels = ["Conservative", "Base (Budget)", "Optimistic"]
        sc_colors = [P_RED, P_GREEN2, P_GREEN]

        fig_sc = go.Figure()
        for metric, fmt_type in [
            ("total_revenue", "eur"), ("total_costs", "eur"), ("net_surplus", "eur")
        ]:
            vals = [scenarios[metric]["conservative"],
                    scenarios[metric]["base"],
                    scenarios[metric]["optimistic"]]
            labels_fmt = [fmt_eur(v) for v in vals]
            fig_sc.add_bar(
                name=metric.replace("_"," ").title(),
                x=sc_labels, y=vals,
                marker_color=sc_colors,
                text=labels_fmt, textposition="outside",
                textfont=dict(size=9, color=P_WHITE),
            )

        fig_sc.update_layout(
            **CHART_LAYOUT, barmode="group", height=270,
            yaxis_tickprefix="€",
            showlegend=True,
        )
        st.plotly_chart(fig_sc, use_container_width=True)

    # ── Spring vs Fall Variance ───────────────────────────────────────────────
    with col_var:
        st.markdown('<div class="section-hdr">Spring vs. Fall Variance</div>',
                    unsafe_allow_html=True)

        key_lines = [
            ("Proj. Fees",   "project_fees"),
            ("Sponsorship",  "sponsorship"),
            ("ESCP Grant",   "escp_grant"),
            ("Membership",   "membership"),
        ]
        var_labels  = [l for l, _ in key_lines]
        spring_vals = [variance[k]["spring"] for _, k in key_lines]
        fall_vals   = [variance[k]["fall"]   for _, k in key_lines]

        fig_var = go.Figure()
        fig_var.add_bar(name="Spring 2026 (Est.)", x=var_labels, y=spring_vals,
                        marker_color="#334", marker_line=dict(color=P_SILVER, width=1),
                        text=[fmt_eur(v) for v in spring_vals],
                        textposition="outside", textfont=dict(size=9, color=P_SILVER))
        fig_var.add_bar(name="Fall 2026 (Budget)", x=var_labels, y=fall_vals,
                        marker_color=P_GREEN2, marker_line=dict(color=P_GREEN, width=1),
                        text=[fmt_eur(v) for v in fall_vals],
                        textposition="outside", textfont=dict(size=9, color=P_WHITE))

        total_var_pct = variance["total_revenue"]["var_pct"]
        fig_var.update_layout(
            **CHART_LAYOUT, barmode="group", height=270,
            yaxis_tickprefix="€",
            title=dict(
                text=f"Total Revenue +{total_var_pct*100:.1f}% semester-on-semester",
                font=dict(size=10, color=P_GREEN), x=0.5,
            ),
        )
        st.plotly_chart(fig_var, use_container_width=True)

    # ── Campus Budget Split ───────────────────────────────────────────────────
    st.markdown('<div class="section-hdr">Campus Budget Allocation</div>',
                unsafe_allow_html=True)

    campuses = ["Paris", "Berlin", "London", "Madrid", "Turin"]
    weights  = [30/85, 22/85, 18/85, 10/85, 5/85]
    camp_rev  = [total_rev  * w for w in weights]
    camp_cost = [total_cost * w for w in weights]
    camp_sur  = [total_sur  * w for w in weights]

    fig_camp = go.Figure()
    fig_camp.add_bar(name="Revenue",  x=campuses, y=camp_rev,
                     marker_color=P_GREEN2,
                     text=[fmt_eur(v) for v in camp_rev],
                     textposition="outside", textfont=dict(size=9, color=P_WHITE))
    fig_camp.add_bar(name="Costs",    x=campuses, y=camp_cost,
                     marker_color="#2A3550",
                     text=[fmt_eur(v) for v in camp_cost],
                     textposition="outside", textfont=dict(size=9, color=P_SILVER))
    fig_camp.add_scatter(name="Net Surplus", x=campuses, y=camp_sur,
                         mode="lines+markers",
                         line=dict(color=P_GREEN, width=2),
                         marker=dict(size=7, color=P_GREEN))
    fig_camp.update_layout(
        **CHART_LAYOUT, barmode="group", height=270,
        yaxis_tickprefix="€",
    )
    st.plotly_chart(fig_camp, use_container_width=True)

