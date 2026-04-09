import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# Configure Streamlit page
st.set_page_config(
    page_title="GA4 E-Commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #1f77b4 0%, #0d47a1 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .section-header {
        background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 20px 0 15px 0;
        font-size: 18px;
        font-weight: bold;
    }
    .alert-box {
        background-color: #ffebee;
        border-left: 4px solid #d32f2f;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #388e3c;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('/Users/rei/Desktop/Digital marketing/dashboard_kpi_values.csv')
    return df

df = load_data()

# Title and overview
st.title("📊 GA4 E-Commerce Dashboard")
st.markdown("**CMO View** | Google Merchandise Store | Nov 2020 – Jan 2021 (92 days)")
st.markdown("---")

# Critical alerts
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="alert-box"><strong>⚠️ CRITICAL:</strong> 77% of 267,116 sessions end without viewing a product — homepage navigation failing. Fix before scaling.</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="success-box"><strong>✅ STRENGTH:</strong> Mobile converts at 41.2% of purchases vs 39.8% traffic share — unusually strong mobile parity.</div>', unsafe_allow_html=True)

st.markdown("---")

# SECTION 1: OVERVIEW & REVENUE
st.markdown('<div class="section-header">1️⃣ OVERVIEW & KEY METRICS</div>', unsafe_allow_html=True)

overview_data = df[df['category'] == 'OVERVIEW']
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = overview_data[overview_data['metric_name'] == 'Total Purchase Revenue']['value'].values[0]
    st.metric("Total Revenue", f"${total_revenue:,.0f}", "Nov - Jan Period")

with col2:
    total_orders = overview_data[overview_data['metric_name'] == 'Total Orders']['value'].values[0]
    st.metric("Total Orders", f"{int(total_orders):,}", "4,419 unique buyers")

with col3:
    unique_buyers = overview_data[overview_data['metric_name'] == 'Unique Buyers']['value'].values[0]
    st.metric("Unique Buyers", f"{int(unique_buyers):,}", "Full period")

with col4:
    total_sessions = overview_data[overview_data['metric_name'] == 'Total Sessions']['value'].values[0]
    st.metric("Total Sessions", f"{int(total_sessions):,}", "Full funnel baseline")

st.markdown("---")

# SECTION 2: REVENUE & TRANSACTION PERFORMANCE (KPIs 1 & 2)
st.markdown('<div class="section-header">💰 REVENUE & TRANSACTION PERFORMANCE (KPIs 1 & 2)</div>', unsafe_allow_html=True)

revenue_data = df[df['category'] == 'REVENUE']

col1, col2, col3, col4 = st.columns(4)
with col1:
    nov_revenue = revenue_data[revenue_data['metric_name'] == 'Total Purchase Revenue'].iloc[1]['value']
    nov_aov = revenue_data[revenue_data['metric_name'] == 'Average Order Value'].iloc[0]['value']
    st.metric("November Revenue", f"${nov_revenue:,.0f}", f"AOV: ${nov_aov:.2f} ⭐ Highest")

with col2:
    dec_revenue = revenue_data[revenue_data['metric_name'] == 'Total Purchase Revenue'].iloc[2]['value']
    dec_aov = revenue_data[revenue_data['metric_name'] == 'Average Order Value'].iloc[1]['value']
    st.metric("December Revenue", f"${dec_revenue:,.0f}", f"AOV: ${dec_aov:.2f} (-39%)")

with col3:
    jan_revenue = revenue_data[revenue_data['metric_name'] == 'Total Purchase Revenue'].iloc[3]['value']
    jan_aov = revenue_data[revenue_data['metric_name'] == 'Average Order Value'].iloc[2]['value']
    st.metric("January Revenue", f"${jan_revenue:,.0f}", f"AOV: ${jan_aov:.2f} Baseline")

with col4:
    full_aov = revenue_data[revenue_data['metric_name'] == 'Average Order Value'].iloc[3]['value']
    st.metric("Full Period AOV", f"${full_aov:.2f}", "Above $80 target ✓")

# Revenue charts
col1, col2 = st.columns(2)

with col1:
    # Revenue by month bar chart
    months = ['November', 'December', 'January']
    revenues = [nov_revenue, dec_revenue, jan_revenue]

    fig_revenue = go.Figure(data=[
        go.Bar(x=months, y=revenues, marker_color=['#1f77b4', '#d32f2f', '#2ca02c'])
    ])
    fig_revenue.update_layout(
        title="Revenue by Month",
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        hovermode='x unified',
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

with col2:
    # AOV trend line chart
    aov_values = [nov_aov, dec_aov, jan_aov]

    fig_aov = go.Figure(data=[
        go.Scatter(x=months, y=aov_values, mode='lines+markers',
                   line=dict(color='#1f77b4', width=3),
                   marker=dict(size=10),
                   fill='tozeroy')
    ])
    fig_aov.update_layout(
        title="AOV Trend by Month",
        xaxis_title="Month",
        yaxis_title="AOV ($)",
        hovermode='x unified',
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_aov, use_container_width=True)

st.markdown("**Interpretation:** Dec AOV dropped 39% vs Nov ($115 → $69) despite peak volume. Holiday volume  came at cost of basket size. Introduce bundle promos and min-basket free shipping in Nov to protect Dec AOV.")

st.markdown("---")

# SECTION 3: FUNNEL & CONVERSION EFFICIENCY (KPIs 3 & 4)
st.markdown('<div class="section-header">🔄 FUNNEL & CONVERSION EFFICIENCY (KPIs 3 & 4)</div>', unsafe_allow_html=True)

funnel_data = df[df['category'] == 'FUNNEL']

col1, col2, col3 = st.columns(3)
with col1:
    cvr = funnel_data[funnel_data['metric_name'] == 'End-to-End Conversion Rate']['value'].values[0]
    st.metric("End-to-End CVR", f"{cvr:.2f}%", "Within benchmark (1-3%) ✓")

with col2:
    checkout_abandon = funnel_data[funnel_data['metric_name'] == 'Checkout Abandonment Rate']['value'].values[0]
    status_color = "🔴" if checkout_abandon > 50 else "🟢"
    st.metric("Checkout Abandonment", f"{checkout_abandon:.2f}%", f"{status_color} Above 50% threshold")

with col3:
    total_sessions_f = funnel_data[funnel_data['metric_name'] == 'Total Sessions']['value'].values[0]
    st.metric("Total Sessions", f"{int(total_sessions_f):,}", "Funnel baseline")

# Funnel visualization
col1, col2 = st.columns([2, 1])

with col1:
    session_start = funnel_data[funnel_data['metric_name'] == 'Funnel Stage - Session Start']['value'].values[0]
    view_item = funnel_data[funnel_data['metric_name'] == 'Funnel Stage - View Item']['value'].values[0]
    add_to_cart = funnel_data[funnel_data['metric_name'] == 'Funnel Stage - Add to Cart']['value'].values[0]
    begin_checkout = funnel_data[funnel_data['metric_name'] == 'Funnel Stage - Begin Checkout']['value'].values[0]
    purchase = funnel_data[funnel_data['metric_name'] == 'Funnel Stage - Purchase']['value'].values[0]

    funnel_stages = ['Session Start', 'View Item', 'Add to Cart', 'Begin Checkout', 'Purchase']
    funnel_values = [session_start, view_item, add_to_cart, begin_checkout, purchase]
    funnel_colors = ['#2ca02c', '#d32f2f', '#ff7f0e', '#ff7f0e', '#1f77b4']

    fig_funnel = go.Figure(go.Funnel(
        y=funnel_stages,
        x=funnel_values,
        marker=dict(color=funnel_colors)
    ))
    fig_funnel.update_layout(
        title="Funnel Breakdown: Session Start to Purchase",
        height=400,
        font=dict(size=12)
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

with col1:
    # Stage details table
    stage_cvr_session_view = funnel_data[funnel_data['metric_name'] == 'Stage CVR - Session to View Item']['value'].values[0]
    stage_cvr_view_cart = funnel_data[funnel_data['metric_name'] == 'Stage CVR - View Item to Add to Cart']['value'].values[0]
    stage_cvr_cart_checkout = funnel_data[funnel_data['metric_name'] == 'Stage CVR - Add to Cart to Checkout']['value'].values[0]
    stage_cvr_checkout_purchase = funnel_data[funnel_data['metric_name'] == 'Stage CVR - Checkout to Purchase']['value'].values[0]

    stage_data = {
        'Stage Transition': [
            'Session → View Item',
            'View Item → Add to Cart',
            'Add to Cart → Checkout',
            'Checkout → Purchase'
        ],
        'Users In → Out': [
            f'{int(session_start):,} → {int(view_item):,}',
            f'{int(view_item):,} → {int(add_to_cart):,}',
            f'{int(add_to_cart):,} → {int(begin_checkout):,}',
            f'{int(begin_checkout):,} → {int(purchase):,}'
        ],
        'CVR': [
            f'{stage_cvr_session_view:.1f}% 🔴',
            f'{stage_cvr_view_cart:.1f}% ⚠️',
            f'{stage_cvr_cart_checkout:.1f}% ✅',
            f'{stage_cvr_checkout_purchase:.1f}% ⚠️'
        ]
    }
    st.dataframe(pd.DataFrame(stage_data), use_container_width=True, hide_index=True)

st.markdown("""
**Key Findings:**
- **CRITICAL:** Session → View Item conversion is only 22.9% — 77.1% of visitors never see a product. This is the largest leak.
- ✅ **STRONG:** 77.4% of users who add to cart proceed to checkout — excellent intent signal
- ⚠️ **WATCH:** 45.5% checkout completion rate — 5,296 high-intent users lost at final stage
""")

st.markdown("---")

# SECTION 4: TRAFFIC SOURCE QUALITY (KPIs 5 & 6)
st.markdown('<div class="section-header">🚀 TRAFFIC SOURCE QUALITY (KPIs 5 & 6)</div>', unsafe_allow_html=True)

traffic_data = df[df['category'] == 'TRAFFIC']

col1, col2, col3 = st.columns(3)
with col1:
    organic_revenue = traffic_data[traffic_data['metric_name'] == 'Revenue by Traffic Channel'].iloc[0]['value']
    organic_cvr = traffic_data[traffic_data['metric_name'] == 'Conversion Rate by Channel'].iloc[0]['value']
    st.metric("Organic Search", f"${organic_revenue:,.0f}", f"CVR: {organic_cvr:.2f}% ⭐ Top Channel")

with col2:
    referral_revenue = traffic_data[traffic_data['metric_name'] == 'Revenue by Traffic Channel'].iloc[2]['value']
    referral_cvr = traffic_data[traffic_data['metric_name'] == 'Conversion Rate by Channel'].iloc[2]['value']
    st.metric("Referral", f"${referral_revenue:,.0f}", f"CVR: {referral_cvr:.2f}% ✅ Best Quality")

with col3:
    cpc_revenue = traffic_data[traffic_data['metric_name'] == 'Revenue by Traffic Channel'].iloc[4]['value']
    cpc_cvr = traffic_data[traffic_data['metric_name'] == 'Conversion Rate by Channel'].iloc[4]['value']
    st.metric("Paid Search (CPC)", f"${cpc_revenue:,.0f}", f"CVR: {cpc_cvr:.2f}% 🔴 Reallocate")

# Channel charts
col1, col2 = st.columns(2)

with col1:
    channels = ['Organic', 'Referral', 'CPC']
    revenues = [organic_revenue, referral_revenue, cpc_revenue]

    fig_channel = go.Figure(data=[
        go.Bar(y=channels, x=revenues, orientation='h', marker_color=['#2ca02c', '#1f77b4', '#d32f2f'])
    ])
    fig_channel.update_layout(
        title="Revenue by Traffic Channel",
        xaxis_title="Revenue ($)",
        yaxis_title="Channel",
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_channel, use_container_width=True)

with col2:
    organic_sessions = traffic_data[traffic_data['metric_name'] == 'Conversion Rate by Channel'].iloc[1]['value']
    referral_sessions = traffic_data[traffic_data['metric_name'] == 'Conversion Rate by Channel'].iloc[3]['value']
    cpc_sessions = traffic_data[traffic_data['metric_name'] == 'Conversion Rate by Channel'].iloc[5]['value']

    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(
        x=[organic_sessions], y=[organic_cvr], mode='markers',
        marker=dict(size=15, color='#2ca02c'),
        text=['Organic'], textposition='top center',
        name='Organic'
    ))
    fig_scatter.add_trace(go.Scatter(
        x=[referral_sessions], y=[referral_cvr], mode='markers',
        marker=dict(size=12, color='#1f77b4'),
        text=['Referral'], textposition='top center',
        name='Referral'
    ))
    fig_scatter.add_trace(go.Scatter(
        x=[cpc_sessions], y=[cpc_cvr], mode='markers',
        marker=dict(size=10, color='#d32f2f'),
        text=['CPC'], textposition='top center',
        name='CPC'
    ))

    fig_scatter.update_layout(
        title="Channel Efficiency: Volume vs CVR",
        xaxis_title="Session Volume",
        yaxis_title="Conversion Rate (%)",
        height=400,
        hovermode='closest'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("""
**Key Insights:**
- 🟢 **Organic** earns 11.5x more revenue than CPC despite similar investment
- 🟡 **Referral** has highest CVR at 1.89% — nearly 2x organic — scale partnerships
- 🔴 **CPC** underperforms at 0.98% CVR — reallocate budget immediately
""")

st.markdown("---")

# SECTION 5: PRODUCT & AUDIENCE INSIGHTS (KPIs 7 & 8)
st.markdown('<div class="section-header">🎁 PRODUCT & AUDIENCE INSIGHTS (KPIs 7 & 8)</div>', unsafe_allow_html=True)

product_data = df[df['category'] == 'PRODUCT']
device_data = df[df['category'] == 'DEVICE']

col1, col2, col3 = st.columns(3)
with col1:
    top5_pct = product_data[product_data['metric_name'] == 'Top Product Revenue Concentration']['value'].values[0]
    st.metric("Top 5 SKU Concentration", f"{top5_pct:.1f}%", "Well below 60% threshold ✓ Healthy")

with col2:
    desktop_gap = device_data[device_data['metric_name'] == 'Device Conversion Gap'].iloc[2]['value']
    st.metric("Desktop Gap", f"{desktop_gap:.1f} ppts", "Neutral (-1.3)")

with col3:
    mobile_gap = device_data[device_data['metric_name'] == 'Device Conversion Gap'].iloc[4]['value']
    st.metric("Mobile Gap", f"{mobile_gap:.1f} ppts", "Strength (+1.4 over-indexes)")

# Product and Device tables
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 5 Products by Revenue")
    products = ['Google Zip Hoodie F/C', 'Google Crewneck Sweatshirt N', "Google Men's Tech Fleece",
                'Google Badge Heavyweight', 'Super G Unisex Joggers']
    pcts = [3.8, 3.0, 2.7, 2.7, 2.6]
    product_df = pd.DataFrame({'Product': products, 'Revenue Share': [f'{p}%' for p in pcts]})
    st.dataframe(product_df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Device: Traffic vs Purchase Distribution")
    devices = ['Desktop', 'Mobile', 'Tablet']
    traffic_pcts = [57.9, 39.8, 2.3]
    purchase_pcts = [56.6, 41.2, 2.2]
    gaps = [-1.3, 1.4, -0.1]
    device_df = pd.DataFrame({
        'Device': devices,
        'Traffic %': traffic_pcts,
        'Purchase %': purchase_pcts,
        'Gap (ppts)': gaps
    })
    st.dataframe(device_df, use_container_width=True, hide_index=True)

st.markdown("""
**Key Findings:**
- ✅ **No concentration risk:** Top 5 SKUs = only 14.8% of revenue. Portfolio is resilient.
- 💪 **Mobile strength:** Mobile over-indexes on purchases (+1.4 ppts) — rare advantage. No UX fix needed.
- 📱 **Desktop baseline:** 57.9% traffic → 56.6% purchases. Proportional conversion.
""")

st.markdown("---")

# SECTION 6: ACTION TRIGGERS & RECOMMENDATIONS
st.markdown('<div class="section-header">⚡ ACTION TRIGGERS & RECOMMENDATIONS</div>', unsafe_allow_html=True)

action_data = df[df['category'] == 'ACTION_TRIGGERS']

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔴 CRITICAL - Fix Homepage Navigation
    **Impact:** 77.1% of 267,116 sessions never view a product = 205,864 lost visitors

    **Issue:** Largest volume leak in funnel

    **Action:** Route to UX + Product team
    - Audit homepage layout and navigation structure
    - Review primary CTAs and product routing
    - Test alternative navigation flows

    **ROI:** Even improving to 30% view rate = ~19,000 additional product viewers
    """)

    st.markdown("""
    ### 🔴 CRITICAL - Audit Checkout Flow
    **Impact:** 54.51% abandonment = 5,296 high-intent users lost

    **Issue:** Above 50% threshold

    **Recovery Potential:** ~$43,083 (10% recovery × AOV)

    **Action:** Route to UX + Dev team
    - Review payment options and form length
    - Improve trust signals and security badges
    - Optimize mobile checkout
    """)

with col2:
    st.markdown("""
    ### 🟡 HIGH PRIORITY - Reallocate CPC Budget
    **Issue:** CPC CVR at 0.98% (below 1% threshold)

    **Data:** 15,450 sessions, only 152 buyers, $9,056 revenue

    **Comparison:** Organic earns 11.5x more than CPC

    **Action:** Route to Performance Marketing team
    - Reduce CPC spend immediately
    - Increase referral partnerships (1.89% CVR)
    - Reallocate freed budget to high-ROI channels
    """)

    st.markdown("""
    ### 🟠 MONITOR - Protect December AOV
    **Issue:** AOV dropped 39% Nov→Dec ($115 → $69)

    **Risk:** Each Dec order worth $45 less than Nov

    **Revenue at Risk:** 2,311 Dec orders × $45 = $103,995 if trend continues

    **Action:** Route to Merchandising + CRM
    - Introduce bundle promotions in early November
    - Minimum-basket free shipping threshold
    - Protect basket size during peak season
    """)

st.markdown("---")

# Footer
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px;'>
    <p>GA4 E-Commerce Dashboard | Nov 2020 – Jan 2021 (92 days)</p>
    <p>Data: bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*</p>
    <p>Last Updated: """ + datetime.now().strftime('%B %d, %Y') + """</p>
    </div>
    """, unsafe_allow_html=True)
