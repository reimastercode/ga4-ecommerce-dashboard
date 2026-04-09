import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="GA4 E-Commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling - Vibrant colors & compact layout
st.markdown("""
    <style>
    /* Reduce overall spacing */
    .css-1y0tads { margin-bottom: 0.5rem !important; }

    .metric-card {
        background: linear-gradient(135deg, #0052CC 0%, #003D99 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .section-header {
        background: linear-gradient(90deg, #0052CC 0%, #00AA44 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 8px 0 10px 0;
        font-size: 16px;
        font-weight: bold;
    }
    .alert-box {
        background-color: #FF3333;
        border-left: 4px solid #CC0000;
        padding: 10px 12px;
        border-radius: 4px;
        margin: 6px 0;
        color: white;
        font-weight: 500;
        font-size: 13px;
    }
    .success-box {
        background-color: #00DD55;
        border-left: 4px solid #00AA33;
        padding: 10px 12px;
        border-radius: 4px;
        margin: 6px 0;
        color: #003300;
        font-weight: 500;
        font-size: 13px;
    }
    .warning-box {
        background-color: #FFAA00;
        border-left: 4px solid #FF8800;
        padding: 10px 12px;
        border-radius: 4px;
        margin: 6px 0;
        color: #333;
        font-weight: 500;
        font-size: 13px;
    }
    /* Compress spacing on metrics */
    [data-testid="metric-container"] {
        margin: 2px 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# KPI DATA - All values from kpi_values_tables.md
# ============================================================================

# Overview metrics
overview_data = {
    'total_revenue': 362165,
    'total_orders': 4452,
    'unique_buyers': 4419,
    'total_sessions': 267116,
}

# Revenue by month
revenue_by_month = {
    'November': {'revenue': 144260, 'orders': 1259, 'aov': 114.58},
    'December': {'revenue': 160555, 'orders': 2311, 'aov': 69.47},
    'January': {'revenue': 57350, 'orders': 895, 'aov': 64.08},
}

# Full period AOV
full_period_aov = 81.35

# Funnel stages
funnel_data = {
    'Session Start': 267116,
    'View Item': 61252,
    'Add to Cart': 12545,
    'Begin Checkout': 9715,
    'Purchase': 4419,
}

# Checkout abandonment
checkout_abandonment_rate = 54.51
checkout_users = 9715
abandoned_users = 5296

# Traffic by channel
traffic_by_channel = {
    'Organic': {'revenue': 104007, 'pct': 28.7, 'sessions': 111346, 'buyers': 1323, 'cvr': 1.19},
    'Referral': {'revenue': 83521, 'pct': 23.1, 'sessions': 54380, 'buyers': 1026, 'cvr': 1.89},
    'CPC': {'revenue': 9056, 'pct': 2.5, 'sessions': 15450, 'buyers': 152, 'cvr': 0.98},
}

# Product concentration
product_data = [
    {'name': 'Google Zip Hoodie F/C', 'revenue': 13788, 'units': 273, 'pct': 3.8},
    {'name': 'Google Crewneck Sweatshirt N', 'revenue': 10714, 'units': 236, 'pct': 3.0},
    {'name': "Google Men's Tech Fleece Grey", 'revenue': 9964, 'units': 134, 'pct': 2.7},
    {'name': 'Google Badge Heavyweight Pullover', 'revenue': 9702, 'units': 201, 'pct': 2.7},
    {'name': 'Super G Unisex Joggers', 'revenue': 9548, 'units': 308, 'pct': 2.6},
]
top5_concentration = 14.8

# Device data
device_data = {
    'Desktop': {'sessions': 157079, 'session_pct': 57.9, 'buyers': 2541, 'purchase_pct': 56.6, 'gap': -1.3},
    'Mobile': {'sessions': 107981, 'session_pct': 39.8, 'buyers': 1851, 'purchase_pct': 41.2, 'gap': 1.4},
    'Tablet': {'sessions': 6175, 'session_pct': 2.3, 'buyers': 97, 'purchase_pct': 2.2, 'gap': -0.1},
}

# ============================================================================
# DASHBOARD TITLE & OVERVIEW
# ============================================================================

st.title("📊 GA4 Dashboard")
st.markdown("**CMO View** | Google Merchandise Store | Nov 2020 – Jan 2021")
st.markdown("<style>hr { margin: 0.5rem 0; }</style>---", unsafe_allow_html=True)

# Critical alerts
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="alert-box">🚨 77% sessions never view product — 205,864 users lost</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="alert-box">⚠️ 54.5% checkout abandonment = $43K recovery potential</div>', unsafe_allow_html=True)

st.markdown("<style>hr { margin: 0.3rem 0; }</style>---", unsafe_allow_html=True)

# ============================================================================
# SECTION 1: REVENUE & TRANSACTION PERFORMANCE
# ============================================================================

st.markdown('<div class="section-header">💰 Revenue & Transaction Performance</div>', unsafe_allow_html=True)

# Overview KPIs
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.metric("Total Revenue", f"${overview_data['total_revenue']:,.0f}", "Full Period")

with kpi_col2:
    st.metric("Total Orders", f"{overview_data['total_orders']:,}", "+83% Dec vs Nov")

with kpi_col3:
    st.metric("Unique Buyers", f"{overview_data['unique_buyers']:,}", "33 repeats")

with kpi_col4:
    st.metric("Avg Order Value", f"${full_period_aov:.2f}", "Period Avg")

# Revenue and AOV visualizations
chart_col1, chart_col2 = st.columns(2)

# Chart 1: Revenue by Month
with chart_col1:
    months = list(revenue_by_month.keys())
    revenues = [revenue_by_month[m]['revenue'] for m in months]

    fig_revenue = go.Figure()
    fig_revenue.add_trace(go.Bar(
        x=months,
        y=revenues,
        marker=dict(color=['#1f77b4', '#d32f2f', '#f57c00']),
        text=[f'${r:,.0f}' for r in revenues],
        textposition='outside',
    ))
    fig_revenue.update_layout(
        title="Revenue by Month",
        yaxis_title="Revenue ($)",
        xaxis_title="Month",
        hovermode='x unified',
        showlegend=False,
        height=280,
        margin=dict(l=50, r=50, t=40, b=40)
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

# Chart 2: AOV Trend
with chart_col2:
    months = list(revenue_by_month.keys())
    aovs = [revenue_by_month[m]['aov'] for m in months]

    fig_aov = go.Figure()
    fig_aov.add_trace(go.Scatter(
        x=months,
        y=aovs,
        mode='lines+markers',
        line=dict(color='#2ca02c', width=3),
        marker=dict(size=10),
        text=[f'${a:.2f}' for a in aovs],
        textposition='top center',
    ))
    fig_aov.update_layout(
        title="Average Order Value Trend",
        yaxis_title="AOV ($)",
        xaxis_title="Month",
        hovermode='x unified',
        showlegend=False,
        height=280,
        margin=dict(l=50, r=50, t=40, b=40)
    )
    st.plotly_chart(fig_aov, use_container_width=True)

st.markdown("**Insight:** Dec volume +83% but AOV -39% vs Nov. Bundle promos needed to protect basket size.", unsafe_allow_html=True)

st.markdown("<style>hr { margin: 0.3rem 0; }</style>---", unsafe_allow_html=True)

# ============================================================================
# SECTION 2: FUNNEL & CONVERSION EFFICIENCY
# ============================================================================

st.markdown('<div class="section-header">🔄 Funnel & Conversion Efficiency</div>', unsafe_allow_html=True)

funnel_col1, funnel_col2, funnel_col3 = st.columns(3)

with funnel_col1:
    st.metric("End-to-End CVR", "1.65%", "Within benchmark")

with funnel_col2:
    st.metric("Checkout Abandonment", f"{checkout_abandonment_rate:.1f}%", "Above 50% threshold")

with funnel_col3:
    st.metric("Revenue at Risk", "$43K", "10% recovery")

# Funnel visualization
stages = list(funnel_data.keys())
users = list(funnel_data.values())

fig_funnel = go.Figure(go.Funnel(
    x=users,
    y=stages,
    marker=dict(color=['#1f77b4', '#d32f2f', '#f57c00', '#2ca02c', '#388e3c']),
    text=[f'{u:,}' for u in users],
    textposition='inside',
))
fig_funnel.update_layout(
    title="User Funnel: Session Start → Purchase",
    height=300,
    margin=dict(l=50, r=50, t=40, b=40)
)
st.plotly_chart(fig_funnel, use_container_width=True)

# Stage-by-stage analysis
st.subheader("Stage-by-Stage Conversion Rates")
funnel_df = pd.DataFrame({
    'Stage': ['Session → View Item', 'View Item → Add to Cart', 'Add to Cart → Checkout', 'Checkout → Purchase'],
    'Conversion Rate': ['22.9%', '20.5%', '77.4%', '45.5%'],
    'Status': ['🚨 Critical', '⚠️ Watch', '✓ Strong', '⚠️ Below Target'],
})
st.dataframe(funnel_df, use_container_width=True, hide_index=True)

st.markdown("""
**Critical Finding:** 205,864 visitors never see a product (77% drop-off). **Action:** Audit homepage navigation immediately.
""")

st.markdown("<style>hr { margin: 0.3rem 0; }</style>---", unsafe_allow_html=True)

# ============================================================================
# SECTION 3: TRAFFIC SOURCE QUALITY
# ============================================================================

st.markdown('<div class="section-header">🚀 Traffic Source Quality</div>', unsafe_allow_html=True)

# Revenue by channel
channels = list(traffic_by_channel.keys())
revenues_channel = [traffic_by_channel[c]['revenue'] for c in channels]
colors_map = {'Organic': '#00CC44', 'Referral': '#0052CC', 'CPC': '#FF3333'}
colors = [colors_map[c] for c in channels]

fig_revenue_channel = go.Figure(go.Bar(
    y=channels,
    x=revenues_channel,
    orientation='h',
    marker=dict(color=colors),
    text=[f'${r:,.0f}<br>({traffic_by_channel[c]["pct"]:.1f}%)' for c, r in zip(channels, revenues_channel)],
    textposition='outside',
))
fig_revenue_channel.update_layout(
    title="Revenue by Traffic Channel",
    xaxis_title="Revenue ($)",
    hovermode='y unified',
    showlegend=False,
    height=200,
    margin=dict(l=50, r=50, t=40, b=40)
)
st.plotly_chart(fig_revenue_channel, use_container_width=True)

# CVR and volume by channel
st.subheader("Channel Efficiency Matrix")
channel_df = pd.DataFrame({
    'Channel': channels,
    'Sessions': [f"{traffic_by_channel[c]['sessions']:,}" for c in channels],
    'Buyers': [f"{traffic_by_channel[c]['buyers']:,}" for c in channels],
    'CVR': [f"{traffic_by_channel[c]['cvr']:.2f}%" for c in channels],
    'Revenue': [f"${traffic_by_channel[c]['revenue']:,.0f}" for c in channels],
    'Status': ['✓ Best', '✓ Strong', '🚨 Alert'],
})
st.dataframe(channel_df, use_container_width=True, hide_index=True)

st.markdown("""
**Key Insight:**
- Organic earns **11.5× more** than CPC despite similar session investment
- Referral converts at **1.89% CVR** (best real channel) vs CPC at 0.98%

**Action:** Reallocate CPC budget to referral partner development. Each 1% CVR improvement at current volume = ~$11,441 additional revenue.
""")

st.markdown("<style>hr { margin: 0.3rem 0; }</style>---", unsafe_allow_html=True)

# ============================================================================
# SECTION 4: PRODUCT & AUDIENCE INSIGHTS
# ============================================================================

st.markdown('<div class="section-header">🎁 Product & Audience Insights</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.metric("Top 5 SKU Concentration", f"{top5_concentration:.1f}%", "Well below 60% threshold")
    st.markdown("""**Status:** Healthy portfolio — no single product dependency risk.
Top 5 products = only 14.8% of revenue. Diversified portfolio is resilient.""")

with col2:
    st.metric("Mobile Conversion Gap", "+1.4 ppts", "Mobile Over-indexes")
    st.markdown("""**Status:** Mobile strength — converts at higher rate than traffic share.
Mobile is a competitive advantage, not a problem.""")

# Top 5 products
st.subheader("Top 5 Products by Revenue")

fig_products = go.Figure(go.Bar(
    y=[p['name'] for p in product_data],
    x=[p['revenue'] for p in product_data],
    orientation='h',
    marker=dict(color='#AA00CC'),
    text=[f"${p['revenue']:,.0f}" for p in product_data],
    textposition='outside',
))
fig_products.update_layout(
    title="Top 5 Products by Revenue",
    xaxis_title="Revenue ($)",
    showlegend=False,
    height=250,
    margin=dict(l=50, r=50, t=40, b=40)
)
st.plotly_chart(fig_products, use_container_width=True)

# Device performance
st.subheader("Device Performance Analysis")

device_df_display = pd.DataFrame([
    {
        'Device': device,
        'Sessions': f"{device_data[device]['sessions']:,}",
        'Session %': f"{device_data[device]['session_pct']:.1f}%",
        'Buyers': f"{device_data[device]['buyers']:,}",
        'Purchase %': f"{device_data[device]['purchase_pct']:.1f}%",
        'Gap (ppts)': f"{device_data[device]['gap']:+.1f}",
    }
    for device in device_data.keys()
])
st.dataframe(device_df_display, use_container_width=True, hide_index=True)

st.markdown("""
**Device Insight:** Mobile (+1.4 ppts) and Desktop (-1.3 ppts) conversion gaps are negligible.
**Recommendation:** Current UX satisfies both desktop and mobile users — maintain without major changes.
""")

st.markdown("<style>hr { margin: 0.3rem 0; }</style>---", unsafe_allow_html=True)

# ============================================================================
# ACTION SUMMARY
# ============================================================================

st.markdown('<div class="section-header">📋 Recommended Actions (Prioritized)</div>', unsafe_allow_html=True)

actions_data = [
    {
        'Priority': '🚨 CRITICAL',
        'Action': 'Fix Homepage Navigation',
        'Impact': '205,864 sessions never view product',
        'Owner': 'UX/Product',
    },
    {
        'Priority': '🚨 CRITICAL',
        'Action': 'Audit Checkout Flow',
        'Impact': '~$43K revenue recovery (10% of abandoned)',
        'Owner': 'Dev/UX',
    },
    {
        'Priority': '🔴 HIGH',
        'Action': 'Reallocate CPC Budget',
        'Impact': 'Organic 11.5× better than CPC',
        'Owner': 'Performance Marketing',
    },
    {
        'Priority': '🟡 MONITOR',
        'Action': 'Protect December AOV',
        'Impact': '$45 drop vs November (39% decline)',
        'Owner': 'Merchandising',
    },
]

actions_df = pd.DataFrame(actions_data)
st.dataframe(actions_df, use_container_width=True, hide_index=True)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #999; font-size: 11px; margin-top: 10px;">
Data: Nov 2020–Jan 2021 | Source: GA4 E-Commerce | Updated: """ + datetime.now().strftime("%b %d, %Y") + """
</div>
""", unsafe_allow_html=True)
