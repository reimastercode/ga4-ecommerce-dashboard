# KPI Framework — GA4 Ecommerce Measurement
**Dataset:** `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`  
**Period:** Nov 2020 – Jan 2021 (92 days)  
**Audience:** CMO  

---

## Group 1 — Revenue & Transaction Performance

---

### KPI 1: Total Purchase Revenue

**Why this KPI was chosen:**
This is the single most direct measure of business outcome. Every other KPI is a lever that moves this number. It anchors the entire dashboard and gives the CMO an unambiguous headline figure.

**SMART:**
- **Specific** — total monetary value of all completed purchase transactions across the dataset period
- **Measurable** — `SUM(ecommerce.purchase_revenue)` filtered to `event_name = 'purchase'`
- **Achievable** — purchase revenue is directly stored in the ecommerce nested field, no derivation needed
- **Relevant** — directly maps to the core business objective of revenue growth
- **Time-bound** — measured across the full Nov 2020 – Jan 2021 period, then broken down by month

**BigQuery fields:**
- `ecommerce.purchase_revenue`
- `event_name = 'purchase'`
- `PARSE_DATE('%Y%m%d', event_date)`

**Visualization:**
Scorecard (headline number) + grouped bar chart (Nov / Dec / Jan comparison). The scorecard gives the CMO the full-period total at a glance — one number, instantly readable. The bar chart alongside it shows the seasonal shape of that revenue across the three months, which is essential context because December is peak holiday season and should visibly dominate.

**Action trigger:**
If December revenue is not at least 30% above November, the holiday campaign underperformed relative to seasonal expectation. The CMO should immediately review the channel mix for December to identify whether paid spend was misallocated.

---

### KPI 2: Average Order Value (AOV)

**Why this KPI was chosen:**
Growing revenue without growing transaction count is the most margin-efficient path to the business objective. AOV captures whether customers are spending more per visit, which is directly controllable through merchandising tactics like product bundles, upsells, and free shipping thresholds. It separates volume growth from value growth.

**SMART:**
- **Specific** — average revenue generated per completed transaction
- **Measurable** — `SUM(ecommerce.purchase_revenue) / COUNT(DISTINCT ecommerce.transaction_id)`
- **Achievable** — both fields are directly available in purchase events
- **Relevant** — a higher AOV means more revenue per customer acquired, improving efficiency
- **Time-bound** — tracked monthly across Nov, Dec, Jan to capture seasonal AOV shift

**BigQuery fields:**
- `ecommerce.purchase_revenue`
- `ecommerce.transaction_id`
- `COUNT(DISTINCT transaction_id)` — DISTINCT is critical to avoid double-counting transactions that appear across multiple event rows

**Visualization:**
Scorecard (full-period AOV) + line chart (monthly AOV trend). The line chart is specifically chosen over a bar here because AOV is a continuous value and the CMO's question is directional — is it going up or down? A line encodes direction more naturally than bars, and the rise into December followed by the January drop is the story the CMO needs to see.

**Action trigger:**
If January AOV drops more than 20% below December, the post-holiday deflation is structurally significant. The CMO's response is to evaluate a bundle promotion or a minimum basket free-shipping threshold to defend the higher spend-per-visit established in December.

---

## Group 2 — Funnel & Conversion Efficiency

---

### KPI 3: End-to-End Conversion Rate

**Why this KPI was chosen:**
This is the headline efficiency metric for the site itself, independent of traffic volume. A CMO can buy more traffic indefinitely, but if the site converts at 0.5% when the industry benchmark is 2%, the problem is the site — not the acquisition. This KPI frames the conversation correctly: is traffic the constraint or is conversion the constraint?

**SMART:**
- **Specific** — percentage of sessions that result in a completed purchase
- **Measurable** — `COUNT(DISTINCT purchasers) / COUNT(DISTINCT session_starters) × 100`
- **Achievable** — both `session_start` and `purchase` events are fully tracked in the dataset
- **Relevant** — the most direct measure of site effectiveness for the CMO
- **Time-bound** — full-period rate as baseline, with monthly breakdown to track trend

**BigQuery fields:**
- `event_name = 'session_start'`
- `event_name = 'purchase'`
- `COUNT(DISTINCT user_pseudo_id)` for both — using `user_pseudo_id` rather than raw event count prevents inflation from users with multiple sessions

**Visualization:**
Funnel chart showing user counts at each stage — `session_start → view_item → add_to_cart → begin_checkout → purchase`. The funnel chart is the right choice here because the CMO's cognitive task is to find the biggest drop-off, and a funnel makes that effortless. The widest-to-narrowest visual encoding means the eye goes directly to the stage where the most users are lost, without any mental arithmetic.

**Action trigger:**
Overall rate below 2% triggers a CRO escalation. The funnel chart enables more precise routing:
- Drop at `begin_checkout → purchase` below 50% → checkout UX audit (payment options, form length, trust signals)
- Drop at `view_item → add_to_cart` below 10% → product page audit (images, copy, pricing)

---

### KPI 4: Checkout Abandonment Rate

**Why this KPI was chosen:**
Of all the places a user can drop off the funnel, checkout abandonment is the most expensive loss because these users have demonstrated the highest purchase intent — they selected products, added to cart, and initiated checkout. Recovering even a small percentage of these users requires no additional acquisition spend. It is the cheapest revenue recovery available to the CMO.

**SMART:**
- **Specific** — percentage of users who initiated checkout but did not complete a purchase
- **Measurable** — `(checkout_users − purchase_users) / checkout_users × 100`
- **Achievable** — `begin_checkout` and `purchase` events are both fully tracked
- **Relevant** — highest-intent funnel stage, directly actionable via UX changes
- **Time-bound** — full period rate with Nov / Dec / Jan monthly comparison

**BigQuery fields:**
- `event_name = 'begin_checkout'`
- `event_name = 'purchase'`
- `COUNT(DISTINCT user_pseudo_id)` for each — the subtraction of purchasers from checkout starters gives the abandoned user count

**Visualization:**
Large scorecard for the abandonment percentage as the primary number, with a grouped bar chart comparing the rate across Nov, Dec, and Jan. The scorecard format is deliberate — abandonment rate is a single number that carries emotional weight when displayed prominently (e.g. "67% of people who started checkout never bought"). That framing motivates urgency in a way a table row would not.

**Action trigger:**
Rate above 50% → CMO flags to development and UX teams with a specific brief: audit the checkout page for payment option variety, form field count, visible trust badges, and mobile-specific checkout friction. This is not a marketing spend decision — it is a product/UX investment decision.

---

## Group 3 — Traffic Source Quality

---

### KPI 5: Revenue by Traffic Channel

**Why this KPI was chosen:**
Without ad spend data in the GA4 dataset, true ROI cannot be calculated. Revenue by channel is the closest honest proxy — it shows which sources actually produce buyers rather than just visitors. This directly informs the CMO's budget allocation question: which channels deserve more investment and which should be cut?

**SMART:**
- **Specific** — total purchase revenue attributed to each traffic medium (organic, cpc, email, direct, referral)
- **Measurable** — `SUM(ecommerce.purchase_revenue) GROUP BY traffic_source.medium`, filtered to purchase events only
- **Achievable** — `traffic_source.medium` is a top-level field available on all events
- **Relevant** — the primary input for channel budget reallocation decisions
- **Time-bound** — full-period total, with the ability to filter to any single month

**BigQuery fields:**
- `traffic_source.medium`
- `traffic_source.source`
- `ecommerce.purchase_revenue` — must be filtered to `event_name = 'purchase'` only; querying revenue across all events misrepresents channel contribution

**Visualization:**
Horizontal bar chart with channels ranked from highest to lowest revenue. Horizontal orientation is chosen because channel names are labels of varying length that render cleanly on a horizontal axis. The top-to-bottom ranking functions as a priority list — the CMO reads it as "these are the channels I should invest in, in this order."

**Action trigger:**
If organic search revenue is 2× or more than paid (cpc) revenue, the CMO is likely over-spending on paid acquisition. Recommended response: shift budget toward content and SEO. If paid significantly outperforms organic, scaling paid is justified — but KPI 6 must be checked alongside to confirm quality, not just volume.

---

### KPI 6: Conversion Rate by Channel

**Why this KPI was chosen:**
KPI 5 shows which channels bring revenue volume. KPI 6 shows which channels bring revenue quality. A channel can rank highly on KPI 5 simply because it sends enormous traffic — but if its conversion rate is 0.3%, a large proportion of that spend is wasted on users with no purchase intent. These two KPIs must be read together to make a sound budget decision.

**SMART:**
- **Specific** — purchase conversion rate calculated separately for each traffic medium
- **Measurable** — `purchase_users / session_users` per medium, expressed as a percentage
- **Achievable** — requires a CTE joining session counts and purchase counts per medium; all underlying data is available
- **Relevant** — identifies budget waste and channel efficiency gaps
- **Time-bound** — full-period rate; flag any channel below 1% CVR as a structural issue

**BigQuery fields:**
- `traffic_source.medium`
- `event_name IN ('session_start', 'purchase')`
- `COUNT(DISTINCT user_pseudo_id)` — requires two aggregations (sessions per medium, purchases per medium) joined via a CTE

**Visualization:**
Scatter plot where the X-axis is session volume, the Y-axis is conversion rate, and the size of each dot represents revenue. This reveals the volume-quality trade-off in two dimensions simultaneously:
- Top-right: high volume, high CVR → scale aggressively
- Bottom-right: high volume, low CVR → budget waste, investigate or cut
- Top-left: low volume, high CVR → scale carefully

A bar chart of CVR alone would hide the volume dimension entirely and lead to incorrect conclusions.

**Action trigger:**
Any channel with high session volume but CVR below 1% triggers an immediate review. The CMO's diagnostic question: is the audience targeting wrong (wrong users arriving) or is the landing page wrong (right users, wrong message)? These require different fixes and different teams.

---

## Group 4 — Product & Audience Insights

---

### KPI 7: Top Product Revenue Concentration

**Why this KPI was chosen:**
This KPI surfaces a strategic risk that is invisible without data — revenue fragility. If three products generate 65% of total revenue and one goes out of stock or faces a competitor, the business has no buffer. The CMO needs to know whether the portfolio is resilient or fragile, and this is the metric that answers that question precisely.

**SMART:**
- **Specific** — the share of total revenue generated by the top 5 SKUs
- **Measurable** — `top_5_sku_revenue / total_revenue × 100`
- **Achievable** — requires `UNNEST(items)` to unpack the product array from purchase events, then aggregation by item name
- **Relevant** — flags portfolio concentration risk and informs product marketing allocation
- **Time-bound** — full-period concentration figure; flag if top 5 SKUs exceed 60% of total revenue

**BigQuery fields:**
- `UNNEST(items)` — unpacks the nested items repeated record field
- `items.item_name`
- `items.price × items.quantity` — calculates per-item revenue contribution

Note: this is one of the more technically complex queries because `items` is a repeated record field requiring unnesting before aggregation.

**Visualization:**
Treemap, where each rectangle represents one SKU and the area is proportional to its revenue contribution. A treemap is chosen over a pie chart deliberately — the human eye is poor at comparing angles and arc lengths in pie charts, but reads rectangular area comparisons accurately. If two or three blocks dominate the canvas, the concentration problem is visually immediate without any numbers needing to be read.

**Action trigger:**
If the top 5 SKUs account for more than 60% of total revenue, the CMO faces a binary strategic choice:
- **Decision A — diversify:** shift marketing spend toward tier-2 products to reduce fragility over time
- **Decision B — double down:** maximise margin on hero products and build inventory buffer as a hedge

Both are valid. The KPI ensures the choice is made consciously rather than remaining a blind spot.

---

### KPI 8: Device Conversion Gap

**Why this KPI was chosen:**
Mobile typically accounts for 55–70% of ecommerce traffic but a disproportionately small share of purchases. The gap between those two percentages is not random — it is a quantified UX failure. This KPI converts an intuitive assumption ("mobile probably converts less") into a precise number the CMO can use to justify a specific investment: mobile checkout UX improvement.

**SMART:**
- **Specific** — the difference in percentage points between mobile's share of sessions and mobile's share of purchases
- **Measurable** — `(mobile_sessions / total_sessions) − (mobile_purchases / total_purchases)` in percentage points
- **Achievable** — `device.category` is available on all events; requires two aggregations joined by device type
- **Relevant** — directly quantifies the mobile UX investment opportunity in revenue terms
- **Time-bound** — full-period gap measurement; a gap above 30 percentage points is the action threshold

**BigQuery fields:**
- `device.category` — returns mobile, desktop, tablet
- `event_name = 'session_start'` for traffic distribution
- `event_name = 'purchase'` for purchase distribution
- Two separate aggregations compared side by side

**Visualization:**
Two side-by-side donut charts. Left donut shows the device split of all sessions (traffic). Right donut shows the device split of all purchases (buyers). The visual gap between mobile's slice in the left donut versus the right donut makes the conversion disparity immediately visible without any arithmetic. A single bar chart showing CVR by device would also work but would not convey the composition shift as intuitively.

**Action trigger:**
A gap exceeding 30 percentage points between mobile traffic share and mobile purchase share means the problem is not traffic acquisition — it is mobile checkout UX. The CMO's response is to reallocate budget from paid traffic campaigns toward mobile UX and development work on the checkout flow. This is a cross-functional decision requiring the CMO to brief both the marketing and product teams with the same data point.

---

## Summary Table

| # | KPI | Group | Visualization | Action threshold |
|---|-----|-------|---------------|-----------------|
| 1 | Total purchase revenue | Revenue | Scorecard + bar chart | Dec not 30%+ above Nov |
| 2 | Average order value | Revenue | Scorecard + line chart | Jan drops 20%+ below Dec |
| 3 | End-to-end conversion rate | Funnel | Funnel chart | Below 2% overall |
| 4 | Checkout abandonment rate | Funnel | Scorecard + grouped bar | Above 50% |
| 5 | Revenue by traffic channel | Traffic | Horizontal bar chart | Organic 2x+ paid |
| 6 | Conversion rate by channel | Traffic | Scatter plot | Any channel below 1% CVR |
| 7 | Top product revenue concentration | Product | Treemap | Top 5 SKUs exceed 60% |
| 8 | Device conversion gap | Audience | Side-by-side donuts | Gap above 30 ppts |
