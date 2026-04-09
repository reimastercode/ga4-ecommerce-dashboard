import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from google.cloud import bigquery
from google.oauth2 import service_account
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GA4 E-Commerce Dashboard",
    page_icon="📊",
    layout="wide",
)

# ── BigQuery client ───────────────────────────────────────────────────────────
DATASET = "bigquery-public-data.ga4_obfuscated_sample_ecommerce"

@st.cache_resource
def get_client():
    # On Streamlit Cloud: load from st.secrets
    # Locally: load from the JSON credentials file
    if "gcp_service_account" in st.secrets:
        info  = dict(st.secrets["gcp_service_account"])
        creds = service_account.Credentials.from_service_account_info(info)
        project = info["project_id"]
    else:
        creds_path = Path(__file__).parent / "robotic-century-480713-q5-c3bdf9975db5.json"
        creds   = service_account.Credentials.from_service_account_file(str(creds_path))
        project = "robotic-century-480713-q5"
    return bigquery.Client(credentials=creds, project=project)

client = get_client()

@st.cache_data(ttl=3600)
def run_query(sql: str) -> pd.DataFrame:
    rows = client.query(sql).result()
    return pd.DataFrame([dict(r) for r in rows])

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("Filters")

date_options = {
    "November 2020":  ("20201101", "20201130"),
    "December 2020":  ("20201201", "20201231"),
    "January 2021":   ("20210101", "20210131"),
    "All (Nov–Jan)":  ("20201101", "20210131"),
}
selected_range = st.sidebar.selectbox("Date range", list(date_options.keys()), index=3)
start_date, end_date = date_options[selected_range]

# Traffic source filter — populated from data
@st.cache_data(ttl=3600)
def get_sources():
    q = f"""
    SELECT DISTINCT
        CONCAT(traffic_source.source, ' / ', traffic_source.medium) AS source_medium
    FROM `{DATASET}.events_*`
    WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
      AND traffic_source.source IS NOT NULL
    ORDER BY source_medium
    """
    return run_query(q)["source_medium"].tolist()

all_sources   = ["All"] + get_sources()
selected_src  = st.sidebar.selectbox("Traffic source / medium", all_sources)
src_filter    = "" if selected_src == "All" else selected_src.split(" / ")[0]
med_filter    = "" if selected_src == "All" else selected_src.split(" / ")[1]

def src_where(alias=""):
    prefix = f"{alias}." if alias else ""
    if src_filter:
        return f"AND {prefix}traffic_source.source = '{src_filter}' AND {prefix}traffic_source.medium = '{med_filter}'"
    return ""

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📊 GA4 E-Commerce Dashboard")
st.caption(
    "Data source: Google Merchandise Store · BigQuery public dataset · "
    f"Period: {selected_range}"
)

# ── KPI scorecards ────────────────────────────────────────────────────────────
kpi_q = f"""
SELECT
  COUNT(DISTINCT user_pseudo_id)                             AS users,
  COUNT(DISTINCT CONCAT(user_pseudo_id, CAST((
    SELECT value.int_value FROM UNNEST(event_params) WHERE key='ga_session_id'
  ) AS STRING)))                                             AS sessions,
  COUNTIF(event_name = 'page_view')                          AS pageviews,
  ROUND(SUM(IF(event_name='purchase', ecommerce.purchase_revenue_in_usd, 0)), 0) AS revenue,
  COUNT(DISTINCT IF(event_name='purchase', ecommerce.transaction_id, NULL)) AS transactions
FROM `{DATASET}.events_*`
WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
{src_where()}
"""
kpi = run_query(kpi_q).iloc[0]
conv_rate = round(kpi["transactions"] / kpi["sessions"] * 100, 2) if kpi["sessions"] else 0
aov       = round(kpi["revenue"] / kpi["transactions"], 2) if kpi["transactions"] else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Users",          f"{int(kpi['users']):,}")
c2.metric("Sessions",       f"{int(kpi['sessions']):,}")
c3.metric("Pageviews",      f"{int(kpi['pageviews']):,}")
c4.metric("Revenue (USD)",  f"${int(kpi['revenue']):,}")
c5.metric("Transactions",   f"{int(kpi['transactions']):,}")
c6.metric("Conv. Rate",     f"{conv_rate}%")

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🌐 Website Performance",
    "💰 Sales Trends",
    "🚦 Traffic Sources",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — WEBSITE PERFORMANCE
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Website Performance")

    # 1A — Sessions & Users over time
    trend_q = f"""
    SELECT
      event_date,
      COUNT(DISTINCT user_pseudo_id) AS users,
      COUNT(DISTINCT CONCAT(user_pseudo_id, CAST((
        SELECT value.int_value FROM UNNEST(event_params) WHERE key='ga_session_id'
      ) AS STRING))) AS sessions,
      COUNTIF(event_name = 'page_view') AS pageviews
    FROM `{DATASET}.events_*`
    WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
    {src_where()}
    GROUP BY event_date ORDER BY event_date
    """
    trend_df = run_query(trend_q)
    trend_df["date"] = pd.to_datetime(trend_df["event_date"], format="%Y%m%d")

    fig_trend = px.line(
        trend_df, x="date", y=["sessions", "users"],
        labels={"value": "Count", "date": "Date", "variable": "Metric"},
        color_discrete_map={"sessions": "#4361ee", "users": "#f72585"},
    )
    fig_trend.update_layout(legend_title_text="")
    st.plotly_chart(fig_trend, use_container_width=True)
    st.caption(
        "**Daily Sessions & Users** — Shows how many people visited the site each day "
        "and how many unique users they represent. Spikes often align with promotions or "
        "seasonal events."
    )

    col_a, col_b = st.columns(2)

    # 1B — Device breakdown
    with col_a:
        device_q = f"""
        SELECT device.category AS device, COUNT(DISTINCT user_pseudo_id) AS users
        FROM `{DATASET}.events_*`
        WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
        {src_where()}
        GROUP BY device ORDER BY users DESC
        """
        device_df = run_query(device_q)
        fig_device = px.pie(
            device_df, names="device", values="users",
            color_discrete_sequence=["#4361ee", "#f72585", "#4cc9f0"],
            hole=0.45,
        )
        fig_device.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_device, use_container_width=True)
        st.caption(
            "**Device Breakdown** — Proportion of users on desktop, mobile, and tablet. "
            "Helps the CMO decide where to prioritise UX investment."
        )

    # 1C — Top countries
    with col_b:
        geo_q = f"""
        SELECT geo.country AS country, COUNT(DISTINCT user_pseudo_id) AS users
        FROM `{DATASET}.events_*`
        WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
        {src_where()}
        GROUP BY country ORDER BY users DESC LIMIT 15
        """
        geo_df = run_query(geo_q)
        fig_geo = px.bar(
            geo_df, x="users", y="country", orientation="h",
            color="users", color_continuous_scale="Blues",
        )
        fig_geo.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(fig_geo, use_container_width=True)
        st.caption(
            "**Top Countries by Users** — Geographic spread of the audience. "
            "Useful for deciding where to run localised marketing campaigns."
        )

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — SALES TRENDS
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Sales Trends")

    # 2A — Daily revenue & AOV
    rev_q = f"""
    SELECT
      event_date,
      COUNT(DISTINCT ecommerce.transaction_id)         AS transactions,
      ROUND(SUM(ecommerce.purchase_revenue_in_usd), 2) AS revenue,
      ROUND(SUM(ecommerce.purchase_revenue_in_usd) /
        NULLIF(COUNT(DISTINCT ecommerce.transaction_id), 0), 2) AS aov
    FROM `{DATASET}.events_*`
    WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
      AND event_name = 'purchase'
    {src_where()}
    GROUP BY event_date ORDER BY event_date
    """
    rev_df = run_query(rev_q)
    rev_df["date"] = pd.to_datetime(rev_df["event_date"], format="%Y%m%d")

    fig_rev = go.Figure()
    fig_rev.add_trace(go.Bar(
        x=rev_df["date"], y=rev_df["revenue"],
        name="Revenue (USD)", marker_color="#4361ee", yaxis="y1"
    ))
    fig_rev.add_trace(go.Scatter(
        x=rev_df["date"], y=rev_df["aov"],
        name="Avg Order Value", mode="lines+markers",
        line=dict(color="#f72585", width=2), yaxis="y2"
    ))
    fig_rev.update_layout(
        yaxis=dict(title="Revenue (USD)"),
        yaxis2=dict(title="AOV (USD)", overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.1),
        hovermode="x unified",
    )
    st.plotly_chart(fig_rev, use_container_width=True)
    st.caption(
        "**Daily Revenue & Average Order Value** — Blue bars show total revenue each day; "
        "the pink line shows the average basket size. Rising AOV with flat revenue suggests "
        "fewer but higher-value purchases."
    )

    col_c, col_d = st.columns(2)

    # 2B — Conversion funnel
    with col_c:
        funnel_q = f"""
        SELECT 'View Item'      AS step, 1 AS o, COUNT(DISTINCT user_pseudo_id) AS users FROM `{DATASET}.events_*` WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}' AND event_name='view_item' {src_where()}
        UNION ALL SELECT 'Add to Cart',    2, COUNT(DISTINCT user_pseudo_id) FROM `{DATASET}.events_*` WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}' AND event_name='add_to_cart' {src_where()}
        UNION ALL SELECT 'Begin Checkout', 3, COUNT(DISTINCT user_pseudo_id) FROM `{DATASET}.events_*` WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}' AND event_name='begin_checkout' {src_where()}
        UNION ALL SELECT 'Add Payment',    4, COUNT(DISTINCT user_pseudo_id) FROM `{DATASET}.events_*` WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}' AND event_name='add_payment_info' {src_where()}
        UNION ALL SELECT 'Purchase',       5, COUNT(DISTINCT user_pseudo_id) FROM `{DATASET}.events_*` WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}' AND event_name='purchase' {src_where()}
        ORDER BY o
        """
        funnel_df = run_query(funnel_q)
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_df["step"], x=funnel_df["users"],
            textinfo="value+percent initial",
            marker=dict(color=["#4361ee", "#4895ef", "#4cc9f0", "#f72585", "#7209b7"]),
        ))
        st.plotly_chart(fig_funnel, use_container_width=True)
        st.caption(
            "**Purchase Funnel** — Shows how many users dropped off at each step from "
            "viewing a product to completing a purchase. The biggest drop-off points are "
            "where the CMO should focus optimisation effort."
        )

    # 2C — Revenue by category
    with col_d:
        cat_q = f"""
        SELECT items.item_category AS category,
          ROUND(SUM(items.item_revenue_in_usd), 0) AS revenue,
          SUM(items.quantity) AS units_sold
        FROM `{DATASET}.events_*`, UNNEST(items) AS items
        WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
          AND event_name = 'purchase'
        GROUP BY category ORDER BY revenue DESC LIMIT 10
        """
        cat_df = run_query(cat_q)
        fig_cat = px.bar(
            cat_df, x="category", y="revenue",
            color="revenue", color_continuous_scale="Blues",
            labels={"revenue": "Revenue (USD)", "category": "Category"},
        )
        fig_cat.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
        st.plotly_chart(fig_cat, use_container_width=True)
        st.caption(
            "**Revenue by Product Category** — Which product categories generate the most "
            "revenue. Helps the CMO allocate marketing budget to the highest-performing lines."
        )

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — TRAFFIC SOURCES
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Traffic Sources")

    # 3A — Sessions & revenue by source/medium
    src_q = f"""
    SELECT
      traffic_source.source AS source,
      traffic_source.medium AS medium,
      COUNT(DISTINCT user_pseudo_id) AS users,
      COUNT(DISTINCT CONCAT(user_pseudo_id, CAST((
        SELECT value.int_value FROM UNNEST(event_params) WHERE key='ga_session_id'
      ) AS STRING))) AS sessions
    FROM `{DATASET}.events_*`
    WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
      AND traffic_source.source IS NOT NULL
    GROUP BY source, medium ORDER BY sessions DESC LIMIT 12
    """
    src_df = run_query(src_q)
    src_df["source_medium"] = src_df["source"] + " / " + src_df["medium"]

    fig_src = px.bar(
        src_df, x="sessions", y="source_medium", orientation="h",
        color="sessions", color_continuous_scale="Blues",
        labels={"sessions": "Sessions", "source_medium": "Source / Medium"},
    )
    fig_src.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(fig_src, use_container_width=True)
    st.caption(
        "**Sessions by Traffic Source** — Where visitors come from (Google, direct, referral, etc.). "
        "The CMO can use this to understand which marketing channels are driving the most traffic."
    )

    col_e, col_f = st.columns(2)

    # 3B — Conversion rate by source
    with col_e:
        conv_q = f"""
        WITH sessions AS (
          SELECT
            traffic_source.source AS source,
            traffic_source.medium AS medium,
            CONCAT(user_pseudo_id, CAST((
              SELECT value.int_value FROM UNNEST(event_params) WHERE key='ga_session_id'
            ) AS STRING)) AS session_id
          FROM `{DATASET}.events_*`
          WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
        ),
        purchases AS (
          SELECT
            traffic_source.source AS source,
            traffic_source.medium AS medium,
            COUNT(DISTINCT ecommerce.transaction_id) AS transactions
          FROM `{DATASET}.events_*`
          WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
            AND event_name = 'purchase'
          GROUP BY source, medium
        )
        SELECT
          s.source, s.medium,
          COUNT(DISTINCT s.session_id) AS sessions,
          COALESCE(p.transactions, 0) AS transactions,
          ROUND(COALESCE(p.transactions,0) * 100.0 / NULLIF(COUNT(DISTINCT s.session_id),0), 2) AS conv_rate
        FROM sessions s
        LEFT JOIN purchases p ON s.source=p.source AND s.medium=p.medium
        WHERE s.source IS NOT NULL
        GROUP BY s.source, s.medium, p.transactions
        ORDER BY sessions DESC LIMIT 10
        """
        conv_df = run_query(conv_q)
        conv_df["source_medium"] = conv_df["source"] + " / " + conv_df["medium"]
        fig_conv = px.bar(
            conv_df.sort_values("conv_rate", ascending=False),
            x="source_medium", y="conv_rate",
            color="conv_rate", color_continuous_scale="RdYlGn",
            labels={"conv_rate": "Conv. Rate (%)", "source_medium": "Source / Medium"},
        )
        fig_conv.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
        st.plotly_chart(fig_conv, use_container_width=True)
        st.caption(
            "**Conversion Rate by Source** — Which channels actually lead to purchases, "
            "not just visits. A high-traffic source with a low conversion rate may need "
            "landing page improvements."
        )

    # 3C — New vs Returning users by top sources
    with col_f:
        nvr_q = f"""
        SELECT
          traffic_source.source AS source,
          COUNTIF(event_name = 'first_visit') AS new_users,
          COUNT(DISTINCT user_pseudo_id) - COUNTIF(event_name = 'first_visit') AS returning_users
        FROM `{DATASET}.events_*`
        WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
          AND traffic_source.source IS NOT NULL
        GROUP BY source
        ORDER BY (new_users + returning_users) DESC LIMIT 8
        """
        nvr_df = run_query(nvr_q)
        fig_nvr = go.Figure(data=[
            go.Bar(name="New Users",       x=nvr_df["source"], y=nvr_df["new_users"],      marker_color="#4361ee"),
            go.Bar(name="Returning Users", x=nvr_df["source"], y=nvr_df["returning_users"], marker_color="#f72585"),
        ])
        fig_nvr.update_layout(barmode="stack", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_nvr, use_container_width=True)
        st.caption(
            "**New vs Returning Users by Source** — Shows whether each channel brings in "
            "fresh audiences or re-engages existing ones. Useful for balancing acquisition "
            "vs retention budget."
        )

