# Assignment 1 – Data Visualization Checklist

## Deliverable 1: Measurement Framework (PDF)

- [ ] Define **at least 1 business objective** (e.g. increase e-commerce revenue)
- [ ] Define and explain **at least 3 KPIs** — each must be S.M.A.R.T. (Specific, Measurable, Achievable, Relevant, Time-bound)
- [ ] For each KPI, **list the GA4 metrics** used to calculate it
- [ ] Show a **clear visual hierarchy**: Business Objective → KPIs → Metrics (e.g. tree diagram, table, or structured layout)
- [ ] Justify why each KPI and visualization choice is relevant to the business objective
- [ ] Include a **public link to the dashboard** in the PDF
- [ ] Export as **PDF, max 1 page**

---

## Deliverable 2: Interactive Dashboard

### Setup
- [x] Set up a Google Account with access to the GA4 e-commerce BigQuery sample dataset
- [x] Set up a data platform (Google Cloud — service account configured, BigQuery connected)

### Content — 3 Focus Areas
- [x] **General website performance** — daily sessions/users trend, device breakdown, top countries
- [x] **Sales trends** — daily revenue & AOV, purchase funnel, revenue by product category
- [x] **Traffic sources** — sessions by source/medium, conversion rate by source, new vs returning users

### Visualizations (dashboard.py — run with `streamlit run dashboard.py`)
- [x] 6 KPI scorecards (users, sessions, pageviews, revenue, transactions, conv. rate)
- [x] Sessions & Users trend line chart
- [x] Device breakdown donut chart
- [x] Top countries bar chart
- [x] Daily Revenue & AOV dual-axis chart
- [x] Purchase funnel chart
- [x] Revenue by product category bar chart
- [x] Sessions by traffic source bar chart
- [x] Conversion rate by source bar chart
- [x] New vs Returning users stacked bar chart
- [x] Each visualization has a plain-language CMO-friendly caption
- [x] Interactive filters: date range selector + traffic source/medium dropdown

### Delivery
- [ ] **Deploy dashboard publicly** — options: Streamlit Community Cloud (free) or Looker Studio
  - Streamlit Cloud: push `dashboard.py` + credentials to GitHub, deploy at share.streamlit.io
  - Looker Studio: connect BigQuery public dataset, recreate charts (no code needed)
- [ ] Dashboard link is **public** and included in the Measurement Framework PDF
