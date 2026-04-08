import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="GA4 E-Commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 500;
    }
    .section-header {
        font-size: 20px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 2px solid #1F77B4;
        padding-bottom: 10px;
    }
    .alert-box {
        padding: 12px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ff7f0e;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-left: 4px solid #d62728;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# MOCK DATA GENERATION
# ============================================================================

@st.cache_data
def generate_mock_data():
    """
    Generate realistic GA4 e-commerce mock data for Nov 2020 - Jan 2021
    """
    np.random.seed(42)

    # Date range
    start_date = pd.Timestamp('2020-11-01')
    end_date = pd.Timestamp('2021-01-31')
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    # Base data structure
    n_events = 5000
    events_data = []

    traffic_sources = ['organic', 'direct', 'cpc', 'social', 'referral']
    devices = ['desktop', 'mobile', 'tablet']
    products = ['Product_A', 'Product_B', 'Product_C', 'Product_D', 'Product_E',
                'Product_F', 'Product_G', 'Product_H', 'Product_I', 'Product_J']

    # Create event sequences
    for i in range(n_events):
        date = np.random.choice(date_range)
        month = date.month

        # Season adjustments
        if month == 12:  # December (holiday)
            revenue_mult = 1.5
            cvr_mult = 1.2
        elif month == 11:
            revenue_mult = 1.0
            cvr_mult = 1.0
        else:  # January
            revenue_mult = 0.8
            cvr_mult = 0.9

        source = np.random.choice(traffic_sources, p=[0.43, 0.29, 0.19, 0.06, 0.03])
        device = np.random.choice(devices, p=[0.58, 0.37, 0.05])
        product = np.random.choice(products)

        # Event funnel with realistic drop-offs
        user_id = f"user_{i % 500}"
        session_id = f"session_{i % 1000}"

        # Session start
        events_data.append({
            'event_date': date,
            'event_name': 'session_start',
            'user_pseudo_id': user_id,
            'session_id': session_id,
            'traffic_source_medium': source,
            'device_category': device,
            'purchase_revenue': 0,
            'transaction_id': None,
            'item_name': None
        })

        # View item (80% of sessions)
        if np.random.random() < 0.88:
            events_data.append({
                'event_date': date,
                'event_name': 'view_item',
                'user_pseudo_id': user_id,
                'session_id': session_id,
                'traffic_source_medium': source,
                'device_category': device,
                'purchase_revenue': 0,
                'transaction_id': None,
                'item_name': product
            })

            # Add to cart (15% of views)
            if np.random.random() < 0.12:
                events_data.append({
                    'event_date': date,
                    'event_name': 'add_to_cart',
                    'user_pseudo_id': user_id,
                    'session_id': session_id,
                    'traffic_source_medium': source,
                    'device_category': device,
                    'purchase_revenue': 0,
                    'transaction_id': None,
                    'item_name': product
                })

                # Begin checkout (78% of add-to-carts)
                if np.random.random() < 0.78:
                    events_data.append({
                        'event_date': date,
                        'event_name': 'begin_checkout',
                        'user_pseudo_id': user_id,
                        'session_id': session_id,
                        'traffic_source_medium': source,
                        'device_category': device,
                        'purchase_revenue': 0,
                        'transaction_id': None,
                        'item_name': product
                    })

                    # Purchase (30% of checkouts)
                    purchase_prob = 0.30
                    if device == 'mobile':
                        purchase_prob *= 0.23  # Mobile converts way less
                    elif source == 'cpc':
                        purchase_prob *= 0.49  # Paid search converts less

                    if np.random.random() < purchase_prob * cvr_mult:
                        quantity = np.random.randint(1, 3)
                        base_price = np.random.choice([29.99, 49.99, 74.99, 99.99, 149.99])
                        revenue = base_price * quantity * revenue_mult

                        events_data.append({
                            'event_date': date,
                            'event_name': 'purchase',
                            'user_pseudo_id': user_id,
                            'session_id': session_id,
                            'traffic_source_medium': source,
                            'device_category': device,
                            'purchase_revenue': revenue,
                            'transaction_id': f"txn_{i}",
                            'item_name': product
                        })

    df = pd.DataFrame(events_data)
    return df

# Load data
@st.cache_data
def load_data():
    df = generate_mock_data()
    return df

df = load_data()

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
st.sidebar.markdown("### 🎛️ **FILTERS**")

# Date range filter
date_range = st.sidebar.date_input(
    "📅 Date Range",
    value=(df['event_date'].min().date(), df['event_date'].max().date()),
    min_value=df['event_date'].min().date(),
    max_value=df['event_date'].max().date()
)

# Traffic source filter
traffic_sources_all = sorted(df['traffic_source_medium'].unique().tolist())
selected_sources = st.sidebar.multiselect(
    "🌐 Traffic Source",
    options=traffic_sources_all,
    default=traffic_sources_all,
    key="traffic_filter"
)

# Device filter
devices_all = sorted(df['device_category'].unique().tolist())
selected_devices = st.sidebar.multiselect(
    "📱 Device",
    options=devices_all,
    default=devices_all,
    key="device_filter"
)

# Reset filters button
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.traffic_filter = traffic_sources_all
    st.session_state.device_filter = devices_all
    st.rerun()

# ============================================================================
# FILTER DATA
# ============================================================================
filtered_df = df[
    (df['event_date'].dt.date >= date_range[0]) &
    (df['event_date'].dt.date <= date_range[1]) &
    (df['traffic_source_medium'].isin(selected_sources)) &
    (df['device_category'].isin(selected_devices))
].copy()

# ============================================================================
# HELPER FUNCTIONS FOR CALCULATIONS
# ============================================================================

def get_kpi_1_revenue():
    """Total Purchase Revenue"""
    return filtered_df[filtered_df['event_name'] == 'purchase']['purchase_revenue'].sum()

def get_kpi_2_aov():
    """Average Order Value"""
    purchases = filtered_df[filtered_df['event_name'] == 'purchase']
    total_revenue = purchases['purchase_revenue'].sum()
    total_orders = purchases['transaction_id'].nunique()
    return total_revenue / total_orders if total_orders > 0 else 0

def get_kpi_3_cvr():
    """End-to-End Conversion Rate"""
    sessions = filtered_df[filtered_df['event_name'] == 'session_start']['user_pseudo_id'].nunique()
    purchases = filtered_df[filtered_df['event_name'] == 'purchase']['user_pseudo_id'].nunique()
    return (purchases / sessions * 100) if sessions > 0 else 0

def get_kpi_4_abandon():
    """Checkout Abandonment Rate"""
    checkout = filtered_df[filtered_df['event_name'] == 'begin_checkout']['user_pseudo_id'].nunique()
    purchases = filtered_df[filtered_df['event_name'] == 'purchase']['user_pseudo_id'].nunique()
    abandoned = checkout - purchases
    return (abandoned / checkout * 100) if checkout > 0 else 0

def get_revenue_by_channel():
    """Revenue by Traffic Channel"""
    revenue = filtered_df[filtered_df['event_name'] == 'purchase'].groupby('traffic_source_medium')['purchase_revenue'].sum().sort_values(ascending=True)
    return revenue

def get_cvr_by_channel():
    """Conversion Rate by Channel"""
    sessions_by_channel = filtered_df[filtered_df['event_name'] == 'session_start'].groupby('traffic_source_medium')['user_pseudo_id'].nunique()
    purchases_by_channel = filtered_df[filtered_df['event_name'] == 'purchase'].groupby('traffic_source_medium')['user_pseudo_id'].nunique()
    cvr = (purchases_by_channel / sessions_by_channel * 100).fillna(0).sort_values(ascending=False)
    return cvr

def get_funnel_data():
    """Funnel: Session Start -> View Item -> Add to Cart -> Begin Checkout -> Purchase"""
    funnel_stages = {
        'Session Start': filtered_df[filtered_df['event_name'] == 'session_start']['user_pseudo_id'].nunique(),
        'View Item': filtered_df[filtered_df['event_name'] == 'view_item']['user_pseudo_id'].nunique(),
        'Add to Cart': filtered_df[filtered_df['event_name'] == 'add_to_cart']['user_pseudo_id'].nunique(),
        'Begin Checkout': filtered_df[filtered_df['event_name'] == 'begin_checkout']['user_pseudo_id'].nunique(),
        'Purchase': filtered_df[filtered_df['event_name'] == 'purchase']['user_pseudo_id'].nunique(),
    }
    return funnel_stages

def get_revenue_by_month():
    """Revenue by Month"""
    monthly_revenue = filtered_df[filtered_df['event_name'] == 'purchase'].copy()
    monthly_revenue['month'] = monthly_revenue['event_date'].dt.strftime('%B')
    monthly_revenue['month_num'] = monthly_revenue['event_date'].dt.month
    monthly_revenue = monthly_revenue.groupby(['month_num', 'month'])['purchase_revenue'].sum().reset_index()
    monthly_revenue = monthly_revenue.sort_values('month_num')
    return monthly_revenue

def get_aov_by_month():
    """AOV by Month"""
    monthly_data = filtered_df[filtered_df['event_name'] == 'purchase'].copy()
    monthly_data['month'] = monthly_data['event_date'].dt.strftime('%B')
    monthly_data['month_num'] = monthly_data['event_date'].dt.month
    monthly_data = monthly_data.groupby(['month_num', 'month']).agg({
        'purchase_revenue': 'sum',
        'transaction_id': 'nunique'
    }).reset_index()
    monthly_data['aov'] = monthly_data['purchase_revenue'] / monthly_data['transaction_id']
    return monthly_data.sort_values('month_num')

def get_device_conversion_gap():
    """Device Conversion Gap"""
    sessions_by_device = filtered_df[filtered_df['event_name'] == 'session_start'].groupby('device_category')['user_pseudo_id'].nunique()
    purchases_by_device = filtered_df[filtered_df['event_name'] == 'purchase'].groupby('device_category')['user_pseudo_id'].nunique()

    total_sessions = sessions_by_device.sum()
    total_purchases = purchases_by_device.sum()

    if total_sessions == 0 or total_purchases == 0:
        return {
            'device': [],
            'session_pct': [],
            'purchase_pct': [],
            'count_sessions': [],
            'count_purchases': []
        }

    device_dist = {
        'device': sessions_by_device.index.tolist(),
        'session_pct': (sessions_by_device / total_sessions * 100).tolist(),
        'purchase_pct': (purchases_by_device[sessions_by_device.index] / total_purchases * 100).tolist() if len(sessions_by_device) > 0 else [],
        'count_sessions': sessions_by_device.tolist(),
        'count_purchases': [purchases_by_device.get(dev, 0) for dev in sessions_by_device.index]
    }
    return device_dist

def get_top_products():
    """Top 5 Products by Revenue"""
    products = filtered_df[filtered_df['event_name'] == 'purchase'].copy()
    if len(products) == 0:
        return pd.DataFrame()

    top_products = products.groupby('item_name').agg({
        'purchase_revenue': 'sum'
    }).sort_values('purchase_revenue', ascending=False).head(5)

    total_revenue = filtered_df[filtered_df['event_name'] == 'purchase']['purchase_revenue'].sum()
    top_products['pct_of_total'] = (top_products['purchase_revenue'] / total_revenue * 100)

    return top_products.reset_index()

# ============================================================================
# HEADER
# ============================================================================
st.markdown("# 📊 GA4 E-Commerce Dashboard")
st.markdown(f"**Dataset:** Nov 2020 – Jan 2021 | **Audience:** CMO")
st.markdown("---")

# ============================================================================
# SECTION 1: REVENUE & TRANSACTION PERFORMANCE
# ============================================================================
st.markdown("### 💰 **SECTION 1: REVENUE & TRANSACTION PERFORMANCE**")

col1, col2, col3 = st.columns(3)

with col1:
    revenue_val = get_kpi_1_revenue()
    st.metric(
        label="Total Purchase Revenue",
        value=f"${revenue_val:,.0f}",
        delta="Full Period"
    )

with col2:
    aov_val = get_kpi_2_aov()
    st.metric(
        label="Average Order Value",
        value=f"${aov_val:.2f}",
        delta="Full Period"
    )

with col3:
    total_orders = filtered_df[filtered_df['event_name'] == 'purchase']['transaction_id'].nunique()
    st.metric(
        label="Total Orders",
        value=f"{total_orders:,}",
        delta="Full Period"
    )

# Revenue by Month
col1, col2 = st.columns(2)

with col1:
    monthly_revenue = get_revenue_by_month()
    if len(monthly_revenue) > 0:
        fig_revenue = go.Figure(data=[
            go.Bar(x=monthly_revenue['month'], y=monthly_revenue['purchase_revenue'],
                   marker=dict(color=['#1F77B4', '#1F77B4', '#1F77B4']),
                   text=[f"${v/1000:.0f}K" for v in monthly_revenue['purchase_revenue']],
                   textposition='outside')
        ])
        fig_revenue.update_layout(
            title="Revenue by Month (Full-Period View)",
            xaxis_title="Month",
            yaxis_title="Revenue ($)",
            showlegend=False,
            height=400,
            hovermode='x unified',
            template='plotly_white'
        )
        st.plotly_chart(fig_revenue, use_container_width=True)

with col2:
    monthly_aov = get_aov_by_month()
    if len(monthly_aov) > 0:
        fig_aov = go.Figure(data=[
            go.Scatter(x=monthly_aov['month'], y=monthly_aov['aov'],
                      mode='lines+markers',
                      line=dict(color='#2CA02C', width=3),
                      marker=dict(size=10),
                      name='AOV')
        ])
        fig_aov.update_layout(
            title="AOV Trend by Month",
            xaxis_title="Month",
            yaxis_title="Average Order Value ($)",
            showlegend=False,
            height=400,
            hovermode='x unified',
            template='plotly_white'
        )
        st.plotly_chart(fig_aov, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 2: FUNNEL & CONVERSION EFFICIENCY
# ============================================================================
st.markdown("### 🔄 **SECTION 2: FUNNEL & CONVERSION EFFICIENCY**")

col1, col2, col3 = st.columns(3)

with col1:
    cvr_val = get_kpi_3_cvr()
    st.metric(
        label="End-to-End CVR",
        value=f"{cvr_val:.2f}%",
        delta="Full Period (Target: 2%+)"
    )

with col2:
    abandon_val = get_kpi_4_abandon()
    color = "🔴" if abandon_val > 50 else "🟡" if abandon_val > 65 else "🟢"
    st.metric(
        label="Checkout Abandonment Rate",
        value=f"{abandon_val:.1f}%",
        delta=f"{color} Full Period (Alert if >50%)"
    )

with col3:
    sessions_count = filtered_df[filtered_df['event_name'] == 'session_start']['user_pseudo_id'].nunique()
    st.metric(
        label="Total Sessions",
        value=f"{sessions_count:,}",
        delta="Full Period"
    )

# Funnel Chart
funnel_data = get_funnel_data()
funnel_stages = list(funnel_data.keys())
funnel_values = list(funnel_data.values())

fig_funnel = go.Figure(go.Funnel(
    y=funnel_stages,
    x=funnel_values,
    marker=dict(color=['#1F77B4', '#1F77B4', '#1F77B4', '#1F77B4', '#2CA02C']),
    textposition="inside",
    textinfo="value+percent initial",
    texttemplate='%{value:,}<br>%{percentInitial}'
))

fig_funnel.update_layout(
    title="Funnel Breakdown: Session Start → Purchase",
    height=450,
    template='plotly_white',
    margin=dict(l=0, r=0, t=50, b=0)
)

st.plotly_chart(fig_funnel, use_container_width=True)

# Identify biggest friction point
if len(funnel_values) > 1:
    drops = [(funnel_stages[i], ((funnel_values[i] - funnel_values[i+1]) / funnel_values[i] * 100))
             for i in range(len(funnel_values)-1)]
    biggest_drop = max(drops, key=lambda x: x[1])
    st.info(f"⚠️ **Biggest friction:** {biggest_drop[0]} → {funnel_stages[funnel_stages.index(biggest_drop[0])+1]} ({biggest_drop[1]:.1f}% drop-off)")

st.markdown("---")

# ============================================================================
# SECTION 3: TRAFFIC SOURCE QUALITY
# ============================================================================
st.markdown("### 🚀 **SECTION 3: TRAFFIC SOURCE QUALITY**")

col1, col2, col3 = st.columns(3)

# Top 3 channels
cvr_by_channel = get_cvr_by_channel()
revenue_by_channel = get_revenue_by_channel()

top_channels = revenue_by_channel.tail(3).index.tolist()

for idx, channel in enumerate(top_channels[:3]):
    if idx < 3:
        if idx == 0:
            col = col1
        elif idx == 1:
            col = col2
        else:
            col = col3

        with col:
            channel_revenue = revenue_by_channel.get(channel, 0)
            channel_cvr = cvr_by_channel.get(channel, 0)

            st.metric(
                label=channel.capitalize(),
                value=f"${channel_revenue:,.0f}",
                delta=f"{channel_cvr:.2f}% CVR"
            )

# Revenue by Channel
col1, col2 = st.columns(2)

with col1:
    revenue_by_channel_sorted = get_revenue_by_channel().sort_values(ascending=True)
    fig_revenue_channel = go.Figure(data=[
        go.Bar(y=revenue_by_channel_sorted.index, x=revenue_by_channel_sorted.values,
               orientation='h',
               marker=dict(color=['#1F77B4', '#1F77B4', '#1F77B4', '#FF7F0E', '#FF7F0E']),
               text=[f"${v/1000:.0f}K" for v in revenue_by_channel_sorted.values],
               textposition='outside')
    ])
    fig_revenue_channel.update_layout(
        title="Revenue by Traffic Channel (Full Period)",
        xaxis_title="Revenue ($)",
        yaxis_title="Channel",
        showlegend=False,
        height=350,
        template='plotly_white'
    )
    st.plotly_chart(fig_revenue_channel, use_container_width=True)

with col2:
    # Conversion Efficiency: Scatter Plot
    cvr_by_channel_all = get_cvr_by_channel()
    revenue_by_channel_all = get_revenue_by_channel()

    sessions_by_channel = filtered_df[filtered_df['event_name'] == 'session_start'].groupby('traffic_source_medium')['user_pseudo_id'].nunique()

    # Align indices
    all_channels = list(set(cvr_by_channel_all.index) | set(sessions_by_channel.index))

    scatter_data = pd.DataFrame({
        'channel': all_channels,
        'sessions': [sessions_by_channel.get(ch, 0) for ch in all_channels],
        'cvr': [cvr_by_channel_all.get(ch, 0) for ch in all_channels],
        'revenue': [revenue_by_channel_all.get(ch, 0) for ch in all_channels]
    })

    fig_scatter = px.scatter(scatter_data,
                            x='sessions',
                            y='cvr',
                            size='revenue',
                            hover_data=['channel', 'sessions', 'cvr', 'revenue'],
                            labels={'sessions': 'Session Volume', 'cvr': 'Conversion Rate (%)'},
                            title="Conversion Efficiency by Channel",
                            color='channel',
                            size_max=50)

    fig_scatter.update_layout(
        height=350,
        template='plotly_white',
        showlegend=True
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 4: PRODUCT & AUDIENCE INSIGHTS
# ============================================================================
st.markdown("### 🎁 **SECTION 4: PRODUCT & AUDIENCE INSIGHTS**")

col1, col2, col3 = st.columns(3)

# Product concentration
top_products = get_top_products()
if len(top_products) > 0:
    top_5_pct = top_products['pct_of_total'].sum()
    color_conc = "🔴" if top_5_pct > 60 else "🟡" if top_5_pct > 50 else "🟢"
else:
    top_5_pct = 0
    color_conc = "🟢"

with col1:
    st.metric(
        label="Top 5 SKUs Concentration",
        value=f"{top_5_pct:.1f}%",
        delta=f"{color_conc} Full Period (Alert if >60%)"
    )

# Device metrics
device_data = get_device_conversion_gap()

# Safe access to device data
desktop_cvr = 0
mobile_cvr = 0
gap = 0
color_gap = "🟢"

if len(device_data['device']) > 0:
    device_dict = dict(zip(device_data['device'],
                          zip(device_data['count_sessions'],
                              device_data['count_purchases'])))

    if 'desktop' in device_dict:
        desktop_sessions, desktop_purchases = device_dict['desktop']
        if desktop_sessions > 0:
            desktop_cvr = (desktop_purchases / desktop_sessions * 100)

    if 'mobile' in device_dict:
        mobile_sessions, mobile_purchases = device_dict['mobile']
        if mobile_sessions > 0:
            mobile_cvr = (mobile_purchases / mobile_sessions * 100)

with col2:
    st.metric(
        label="Desktop Performance",
        value=f"{desktop_cvr:.2f}% CVR",
        delta="✓ Baseline"
    )

# Calculate mobile-desktop gap
if desktop_cvr > 0 and mobile_cvr > 0:
    gap = desktop_cvr - mobile_cvr
    color_gap = "🔴" if gap > 2 else "🟡" if gap > 1 else "🟢"
else:
    gap = 0
    color_gap = "🟢"

with col3:
    st.metric(
        label="Mobile Performance",
        value=f"{mobile_cvr:.2f}% CVR",
        delta=f"{color_gap} Gap: {gap:.1f} ppts"
    )

# Top Products Treemap
if len(top_products) > 0:
    fig_treemap = px.treemap(
        top_products,
        labels='item_name',
        parents=[''] * len(top_products),
        values='purchase_revenue',
        title="Top 5 Products by Revenue (Treemap)",
        text='pct_of_total',
        color='purchase_revenue',
        color_continuous_scale='Blues'
    )

    fig_treemap.update_traces(
        texttemplate='<b>%{label}</b><br>%{text:.1f}%<br>$%{value:.0f}',
        textposition='middle center'
    )

    fig_treemap.update_layout(
        height=400,
        template='plotly_white'
    )

    st.plotly_chart(fig_treemap, use_container_width=True)

# Device Distribution: Side-by-side Donuts
col1, col2 = st.columns(2)

with col1:
    if len(device_data['device']) > 0:
        fig_traffic = go.Figure(data=[go.Pie(
            labels=device_data['device'],
            values=device_data['count_sessions'],
            marker=dict(colors=['#1F77B4', '#FF7F0E', '#808080']),
            textposition='inside',
            texttemplate='%{label}<br>%{value:,}<br>(%{percent})'
        )])
        fig_traffic.update_layout(
            title="Traffic Distribution by Device",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_traffic, use_container_width=True)

with col2:
    if len(device_data['device']) > 0:
        fig_purchases = go.Figure(data=[go.Pie(
            labels=device_data['device'],
            values=device_data['count_purchases'],
            marker=dict(colors=['#1F77B4', '#FF7F0E', '#808080']),
            textposition='inside',
            texttemplate='%{label}<br>%{value:,}<br>(%{percent})'
        )])
        fig_purchases.update_layout(
            title="Purchase Distribution by Device",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_purchases, use_container_width=True)

st.markdown("---")

# ============================================================================
# FOOTER / INSIGHTS & RECOMMENDATIONS
# ============================================================================
st.markdown("### 📊 **KEY INSIGHTS & ACTION TRIGGERS**")

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Green Lights")

    if revenue_val > 500000:
        st.success("✓ Strong revenue baseline ($500K+) despite limited dataset period")

    if cvr_val > 2:
        st.success(f"✓ CVR at {cvr_val:.2f}% exceeds 2% benchmark")

    if 'organic' in cvr_by_channel.index and cvr_by_channel['organic'] > cvr_by_channel.get('cpc', 0):
        st.success("✓ Organic search outperforms paid search on efficiency")

with col2:
    st.subheader("⚠️ Action Items")

    if abandon_val > 50:
        st.error(f"🔴 Checkout abandonment at {abandon_val:.1f}% — Audit payment options & form friction")

    if gap > 30:
        st.error(f"🔴 Mobile-Desktop gap {gap:.1f} ppts — Prioritize mobile UX audit")

    if top_5_pct > 60:
        st.warning(f"🟡 Top products concentration {top_5_pct:.1f}% — Consider portfolio diversification")

st.markdown("---")
st.markdown("*Dashboard built with Streamlit + Plotly | Data: GA4 E-Commerce Sample Dataset (Nov 2020 – Jan 2021)*")
