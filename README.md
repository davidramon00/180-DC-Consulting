# 180DC ESCP — Financial Dashboard

Executive financial dashboard for **180 Degrees Consulting ESCP**, Fall Semester 2026.  
Built with **Streamlit** and **Plotly**, reading live data from the Excel financial model.

---

## Project structure

```
180dc_dashboard/
├── app.py                  # Streamlit entry point
├── data_loader.py          # Excel reader — all cell refs in one place
├── requirements.txt        # Python dependencies
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml         # Theme and server settings
└── data/
    └── 180DC_ESCP_FinancialModel_Fall2026_v3.xlsx
```

---

## Running locally

**Prerequisites:** Python 3.9+

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/180dc-dashboard.git
cd 180dc-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place the Excel model inside data/
#    data/180DC_ESCP_FinancialModel_Fall2026_v3.xlsx

# 4. Start
streamlit run app.py
# Opens at http://localhost:8501
```

---

## Deploying to Streamlit Community Cloud (free)

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → sign in with GitHub.
3. **New app** → select repo → set main file to `app.py` → **Deploy**.
4. Live at `https://<your-app>.streamlit.app`.

> The Excel file must be committed inside the `data/` folder — Streamlit Community Cloud has no persistent storage.

---

## Data flow

```
Excel model  →  data_loader.py (openpyxl, data_only=True)  →  app.py (Streamlit + Plotly)
```

All cell references are centralised in `data_loader.py`. If the model structure changes, only that file needs updating.

---

## Dashboard sections

| Section | Content |
|---|---|
| KPI cards | Revenue, Costs, Surplus, Margin, Active Members |
| Monthly Revenue vs. Costs | Grouped bars + surplus line |
| Revenue Mix | Donut: fees, sponsorships, grant, membership, events |
| Cumulative Net Position | Area chart of running surplus |
| Cost Structure | Donut of cost categories |
| KPI Status | 8 KPIs with RAG badges |
| Monthly Detail | Full P&L table (collapsible) |
| Assumptions | Key model inputs (collapsible) |

---

## Model rationale (research-based)

180DC operates a **pro-bono / symbolic-fee** model. Clients are nonprofits  
(Amnesty International, Rainforest Alliance, Les Restos du Coeur, Enercoop, etc.)  
that cannot afford standard consulting rates. Revenue is driven primarily by  
**corporate sponsorships** and the **ESCP institutional grant**, not project fees.  
The branch spans 5 campuses: Paris, Berlin, London, Madrid, Turin.

---

## Updating the model

Edit blue cells in the **Assumptions** sheet → save → re-run or push to GitHub.  
The app caches data for 60 seconds; a browser refresh will reload it.
