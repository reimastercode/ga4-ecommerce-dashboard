# Measurement Framework — GA4 E-Commerce Dashboard
**Course:** Digital Marketing and Data Science (2025-2026) · Assignment 1
**Dashboard:** _[paste your Streamlit public link here]_

---

## Business Objective

> **Increase online revenue of the Google Merchandise Store by improving conversion efficiency and optimising marketing channel investment.**

---

## Visual Hierarchy

```
BUSINESS OBJECTIVE
└── Grow online revenue through smarter marketing decisions
    │
    ├── KPI 1: E-commerce Conversion Rate
    │   ├── Metric: transactions (purchase events)
    │   └── Metric: sessions
    │
    ├── KPI 2: Average Order Value (AOV)
    │   ├── Metric: purchase_revenue_in_usd
    │   └── Metric: transaction_id (distinct count)
    │
    └── KPI 3: Organic Traffic Share
        ├── Metric: traffic_source.source
        ├── Metric: traffic_source.medium
        └── Metric: sessions (by source/medium)
```

---

## KPI Definitions

### KPI 1 — E-commerce Conversion Rate
**Formula:** `(Transactions ÷ Sessions) × 100`

| S.M.A.R.T. criterion | Definition |
|---|---|
| **Specific** | Measures the percentage of website sessions that result in a completed purchase |
| **Measurable** | Expressed as a percentage; calculated from GA4 `purchase` events and session count |
| **Achievable** | Current baseline is ~1.6%; industry average for e-commerce is 2–3%, making 2% a realistic target |
| **Relevant** | Directly ties marketing traffic to revenue outcomes — more conversions = more revenue without needing more visitors |
| **Time-bound** | Tracked monthly; target: reach 2% conversion rate within the 3-month data window (Nov 2020 – Jan 2021) |

**GA4 Metrics used:**
- `event_name = 'purchase'` → counts completed transactions
- `ecommerce.transaction_id` → unique transaction count
- `ga_session_id` (event param) → unique session count

**Why this KPI?** The funnel data shows 61,252 users viewed a product but only 4,419 completed a purchase — a 92.8% drop-off. Even a small improvement in conversion rate has a large revenue impact, making this the most actionable KPI for the CMO.

---

### KPI 2 — Average Order Value (AOV)
**Formula:** `Total Revenue (USD) ÷ Number of Transactions`

| S.M.A.R.T. criterion | Definition |
|---|---|
| **Specific** | Measures the average amount spent per completed order |
| **Measurable** | Expressed in USD; directly readable from GA4 ecommerce data |
| **Achievable** | Baseline AOV varies by day; target is to maintain or grow AOV month-over-month |
| **Relevant** | Growing AOV increases revenue without requiring more traffic or higher conversion rates — a highly cost-efficient lever |
| **Time-bound** | Monitored monthly; target: sustain or increase AOV from November 2020 baseline through January 2021 |

**GA4 Metrics used:**
- `ecommerce.purchase_revenue_in_usd` → total revenue per transaction
- `ecommerce.transaction_id` → denominator for average calculation
- `event_date` → time-series trending

**Why this KPI?** AOV reflects the quality of each purchase, not just the volume. If AOV drops while transactions rise, it may indicate discount-driven behaviour that hurts margins. The CMO can use this alongside promotions data to assess campaign profitability.

---

### KPI 3 — Organic Traffic Share
**Formula:** `(Sessions from organic search ÷ Total sessions) × 100`

| S.M.A.R.T. criterion | Definition |
|---|---|
| **Specific** | Measures the proportion of traffic arriving via unpaid (organic) search |
| **Measurable** | Expressed as a percentage; derived from `traffic_source.medium = 'organic'` |
| **Achievable** | Organic is already the #1 source (103k users); target is to maintain >40% organic share |
| **Relevant** | Organic traffic has no per-click cost — a high organic share reduces customer acquisition cost and signals strong SEO health |
| **Time-bound** | Reported monthly; target: organic share stays above 40% across the Nov 2020 – Jan 2021 period |

**GA4 Metrics used:**
- `traffic_source.source` → identifies the traffic origin (e.g. google, direct)
- `traffic_source.medium` → classifies channel type (organic, referral, cpc, none)
- `user_pseudo_id` + `ga_session_id` → session and user counts per source

**Why this KPI?** Traffic source data shows Google organic is the dominant channel (103k users), followed by direct (76k). Monitoring the organic share helps the CMO detect if paid spend is replacing what should be free traffic, and informs SEO investment decisions.

---

## Metric–KPI–Objective Map

| GA4 Metric | KPI | Business Objective |
|---|---|---|
| `purchase` event count | Conversion Rate | Increase revenue |
| `ecommerce.transaction_id` | Conversion Rate + AOV | Increase revenue |
| `ecommerce.purchase_revenue_in_usd` | AOV | Increase revenue |
| `ga_session_id` (event param) | Conversion Rate + Organic Share | Increase revenue |
| `traffic_source.source` | Organic Traffic Share | Increase revenue |
| `traffic_source.medium` | Organic Traffic Share | Increase revenue |
| `event_date` | All KPIs (time-series) | Increase revenue |
| `device.category` | Supporting context | Increase revenue |
| `geo.country` | Supporting context | Increase revenue |
