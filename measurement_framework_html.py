from weasyprint import HTML, CSS
from datetime import datetime

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GA4 E-Commerce Measurement Framework</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2C3E50;
            background: white;
            padding: 20px;
        }

        .page {
            max-width: 8.5in;
            height: 11in;
            margin: 0 auto 20px;
            padding: 30px;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            page-break-after: always;
        }

        h1 {
            color: #1F77B4;
            font-size: 24px;
            text-align: center;
            margin-bottom: 10px;
            border-bottom: 3px solid #1F77B4;
            padding-bottom: 10px;
        }

        h2 {
            color: #1F77B4;
            font-size: 16px;
            margin-top: 20px;
            margin-bottom: 12px;
            border-left: 4px solid #1F77B4;
            padding-left: 10px;
        }

        h3 {
            color: #2C3E50;
            font-size: 13px;
            margin-top: 15px;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .meta-info {
            background: #F8F9FA;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 12px;
            margin-bottom: 20px;
            font-size: 10px;
        }

        .meta-info p {
            margin: 4px 0;
        }

        .meta-info strong {
            color: #1F77B4;
            min-width: 100px;
            display: inline-block;
        }

        .section-header {
            background: #E8F4F8;
            border-left: 4px solid #FF7F0E;
            padding: 10px 12px;
            margin: 15px 0 10px 0;
            font-weight: 600;
            font-size: 11px;
            color: #2C3E50;
        }

        .kpi-card {
            background: white;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 12px;
            margin-bottom: 12px;
            page-break-inside: avoid;
        }

        .kpi-card.revenue {
            border-left: 4px solid #2CA02C;
        }

        .kpi-card.funnel {
            border-left: 4px solid #FF7F0E;
        }

        .kpi-card.traffic {
            border-left: 4px solid #2CA02C;
        }

        .kpi-card.product {
            border-left: 4px solid #9467BD;
        }

        .kpi-header {
            display: grid;
            grid-template-columns: 80px 1fr;
            gap: 10px;
            margin-bottom: 10px;
            border-bottom: 1px solid #E0E0E0;
            padding-bottom: 8px;
        }

        .kpi-label {
            font-weight: 600;
            font-size: 10px;
            color: #1F77B4;
        }

        .kpi-title {
            font-weight: 600;
            font-size: 11px;
            color: #2C3E50;
        }

        .kpi-row {
            display: grid;
            grid-template-columns: 80px 1fr;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 9px;
        }

        .kpi-row-label {
            font-weight: 600;
            color: #666;
            flex-shrink: 0;
        }

        .kpi-row-content {
            color: #2C3E50;
            line-height: 1.4;
        }

        .problem-box {
            background: #FFF5E6;
            border: 1px solid #FFE0B2;
            border-radius: 4px;
            padding: 12px;
            margin: 12px 0;
            font-size: 9px;
            line-height: 1.5;
        }

        .objective-box {
            background: #E8F5E9;
            border: 2px solid #66BB6A;
            border-radius: 4px;
            padding: 12px;
            margin: 12px 0;
            font-size: 9px;
            line-height: 1.5;
        }

        .objective-box strong {
            color: #2CA02C;
        }

        .summary-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8px;
            margin-top: 10px;
        }

        .summary-table th {
            background: #1F77B4;
            color: white;
            padding: 8px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #1F77B4;
        }

        .summary-table td {
            padding: 6px 8px;
            border: 1px solid #E0E0E0;
        }

        .summary-table tr:nth-child(even) {
            background: #F8F9FA;
        }

        .footer {
            font-size: 8px;
            color: #666;
            margin-top: 20px;
            padding-top: 10px;
            border-top: 1px solid #E0E0E0;
            text-align: center;
        }

        .problem-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
            margin: 12px 0;
        }

        .problem-item {
            background: white;
            border-left: 3px solid #FF7F0E;
            padding: 10px;
            font-size: 9px;
        }

        .problem-item strong {
            color: #FF7F0E;
            display: block;
            margin-bottom: 4px;
        }

        .highlight {
            background: #FFFACD;
            padding: 2px 4px;
            border-radius: 2px;
        }

        .page-break {
            page-break-after: always;
        }
    </style>
</head>
<body>

<!-- PAGE 1 -->
<div class="page">
    <h1>🎯 GA4 E-COMMERCE MEASUREMENT FRAMEWORK</h1>

    <div class="meta-info">
        <p><strong>Dataset:</strong> bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*</p>
        <p><strong>Period:</strong> Nov 2020 – Jan 2021 (92 days)</p>
        <p><strong>Audience:</strong> Chief Marketing Officer (CMO)</p>
        <p><strong>Tools:</strong> Looker Studio / Streamlit</p>
    </div>

    <h2>1. Dataset Overview</h2>
    <p style="font-size: 9px; line-height: 1.5; margin-bottom: 10px;">
        This GA4 sample dataset contains 230K+ user sessions and 5.7K+ purchases across a real e-commerce website.
        Events are granular: session_start → view_item → add_to_cart → begin_checkout → purchase.
        Each event carries context: traffic source, device, products viewed, and revenue. This enables precise funnel analysis and pattern discovery.
    </p>

    <h2>2. Problems This Data Solves</h2>

    <div class="problem-item">
        <strong style="color: #FF7F0E;">Product-Market Misalignment</strong>
        Pareto analysis across SKUs reveals if 3-5 hero products drive 60%+ of revenue. This signals portfolio concentration risk and informs go/no-go diversification decisions.
        <div style="font-size: 8px; color: #999; margin-top: 4px;"><em>Fields: items.item_name, ecommerce.purchase_revenue</em></div>
    </div>

    <div class="problem-item">
        <strong style="color: #FF7F0E;">Funnel Friction</strong>
        Event sequence tracking pinpoints exactly where users drop off. View Item→Add to Cart has the biggest leak? That's product page UX. Begin Checkout→Purchase has friction? That's checkout complexity.
        <div style="font-size: 8px; color: #999; margin-top: 4px;"><em>Fields: event_name, user_pseudo_id</em></div>
    </div>

    <div class="problem-item">
        <strong style="color: #FF7F0E;">Traffic Source Quality Gap</strong>
        Revenue attribution by traffic_source.medium shows which channels produce buyers, not just clicks. Organic may send less traffic but more revenue than paid search.
        <div style="font-size: 8px; color: #999; margin-top: 4px;"><em>Fields: traffic_source.medium, ecommerce.purchase_revenue, event_name='purchase'</em></div>
    </div>

    <div class="problem-item">
        <strong style="color: #FF7F0E;">Device Conversion Disparity</strong>
        Comparing device.category across sessions vs. purchases exposes mobile checkout friction. If mobile is 40% of traffic but only 10% of purchases, the 30-point gap quantifies UX investment ROI.
        <div style="font-size: 8px; color: #999; margin-top: 4px;"><em>Fields: device.category, event_name</em></div>
    </div>

    <h2>3. Business Objective</h2>
    <div class="objective-box">
        <strong>Understand ecommerce performance patterns across Nov 2020 – Jan 2021 to identify conversion inefficiencies,
        traffic quality gaps, and funnel friction — and use these as a baseline for growth decisions.</strong><br><br>
        <strong style="color: #666;">Rationale:</strong> With only 92 days of data, revenue growth targets are unrealistic. Instead, we establish diagnostic baselines:
        Where do users drop off? Which channels deliver profitable traffic? Which devices have UX problems? These insights drive prioritization for the next 6-month cycle.
    </div>

</div>

<!-- PAGE 2 -->
<div class="page">
    <h1>4. Key Performance Indicators (KPIs)</h1>

    <div class="section-header">GROUP 1: REVENUE & TRANSACTION PERFORMANCE</div>

    <div class="kpi-card revenue">
        <div class="kpi-header">
            <div class="kpi-label">KPI #1</div>
            <div class="kpi-title">Total Purchase Revenue</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Definition</div>
            <div class="kpi-row-content">Sum of all completed purchase transaction values (Nov–Jan period, then monthly breakdown)</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">SMART</div>
            <div class="kpi-row-content"><strong>S</strong>pecific: total $ value | <strong>M</strong>easurable: SUM(ecommerce.purchase_revenue) | <strong>A</strong>chievable: direct field | <strong>R</strong>elevant: core business | <strong>T</strong>ime-bound: Nov-Jan period</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Fields</div>
            <div class="kpi-row-content">ecommerce.purchase_revenue, event_name = 'purchase', event_date</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Visualization</div>
            <div class="kpi-row-content">Scorecard (full-period total) + Bar Chart (Nov/Dec/Jan comparison showing holiday spike)</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Action Trigger</div>
            <div class="kpi-row-content"><span class="highlight">Dec revenue <30% above Nov</span> → holiday campaign underperformed. Audit channel mix allocation.</div>
        </div>
    </div>

    <div class="kpi-card revenue">
        <div class="kpi-header">
            <div class="kpi-label">KPI #2</div>
            <div class="kpi-title">Average Order Value (AOV)</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Definition</div>
            <div class="kpi-row-content">Revenue per completed transaction (SUM(revenue) / COUNT(DISTINCT transaction_id))</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">SMART</div>
            <div class="kpi-row-content"><strong>S</strong>pecific: $ per transaction | <strong>M</strong>easurable: revenue / distinct txns | <strong>A</strong>chievable: both fields available | <strong>R</strong>elevant: margin efficiency | <strong>T</strong>ime-bound: monthly trend</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Fields</div>
            <div class="kpi-row-content">ecommerce.purchase_revenue, ecommerce.transaction_id, event_name = 'purchase'</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Visualization</div>
            <div class="kpi-row-content">Scorecard (full-period AOV) + Line Chart (monthly trend showing seasonal direction)</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Action Trigger</div>
            <div class="kpi-row-content"><span class="highlight">Jan drops >20% below Dec</span> → activate bundle promo or min-basket free-shipping to defend AOV.</div>
        </div>
    </div>

    <div class="section-header">GROUP 2: FUNNEL & CONVERSION EFFICIENCY</div>

    <div class="kpi-card funnel">
        <div class="kpi-header">
            <div class="kpi-label">KPI #3</div>
            <div class="kpi-title">End-to-End Conversion Rate</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Definition</div>
            <div class="kpi-row-content">% of sessions that result in a purchase (independent of traffic volume)</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">SMART</div>
            <div class="kpi-row-content"><strong>S</strong>pecific: % sessions→purchases | <strong>M</strong>easurable: (purchase_users/session_users)×100 | <strong>A</strong>chievable: both tracked | <strong>R</strong>elevant: site efficiency metric | <strong>T</strong>ime-bound: full-period baseline + monthly</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Fields</div>
            <div class="kpi-row-content">event_name IN ('session_start', 'purchase'), user_pseudo_id</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Visualization</div>
            <div class="kpi-row-content">Funnel Chart: session_start → view_item → add_to_cart → begin_checkout → purchase (shows drop-off %)</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Action Trigger</div>
            <div class="kpi-row-content"><span class="highlight">CVR <2%</span> → CRO escalation. Funnel drill-down routes fix: view→cart drop = product page; checkout drop = UX.</div>
        </div>
    </div>

    <div class="kpi-card funnel">
        <div class="kpi-header">
            <div class="kpi-label">KPI #4</div>
            <div class="kpi-title">Checkout Abandonment Rate</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Definition</div>
            <div class="kpi-row-content">% of checkout starters who do NOT complete purchase (highest-intent users lost)</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">SMART</div>
            <div class="kpi-row-content"><strong>S</strong>pecific: % begin_checkout without purchase | <strong>M</strong>easurable: ((checkout_users-purchase_users)/checkout_users)×100 | <strong>A</strong>chievable: direct events | <strong>R</strong>elevant: cheapest revenue recovery | <strong>T</strong>ime-bound: monthly comparison</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Fields</div>
            <div class="kpi-row-content">event_name IN ('begin_checkout', 'purchase'), user_pseudo_id</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Visualization</div>
            <div class="kpi-row-content">Scorecard (abandonment %) + Grouped Bar (monthly trend Nov/Dec/Jan showing seasonality)</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Action Trigger</div>
            <div class="kpi-row-content"><span class="highlight">Abandonment >50%</span> → audit payment options, form fields, trust badges, mobile checkout. Product/UX team investment required.</div>
        </div>
    </div>

</div>

<!-- PAGE 3 -->
<div class="page">
    <div class="section-header">GROUP 3: TRAFFIC SOURCE QUALITY</div>

    <div class="kpi-card traffic">
        <div class="kpi-header">
            <div class="kpi-label">KPI #5</div>
            <div class="kpi-title">Revenue by Traffic Channel</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Definition</div>
            <div class="kpi-row-content">Total purchase revenue attributed to each traffic_source.medium (organic, cpc, direct, etc.)</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">SMART</div>
            <div class="kpi-row-content"><strong>S</strong>pecific: $ revenue per channel | <strong>M</strong>easurable: SUM(purchase_revenue) GROUP BY medium | <strong>A</strong>chievable: direct fields | <strong>R</strong>elevant: budget reallocation input | <strong>T</strong>ime-bound: full-period + monthly breakdown</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Fields</div>
            <div class="kpi-row-content">traffic_source.medium, traffic_source.source, ecommerce.purchase_revenue, event_name='purchase'</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Visualization</div>
            <div class="kpi-row-content">Horizontal Bar Chart (channels ranked high→low revenue). Horizontal labels render cleanly; ranking is priority list.</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Action Trigger</div>
            <div class="kpi-row-content"><span class="highlight">Organic 2x+ paid</span> → CMO over-spending on paid. Shift to content/SEO. Verify with KPI #6 first if reversible.</div>
        </div>
    </div>

    <div class="kpi-card traffic">
        <div class="kpi-header">
            <div class="kpi-label">KPI #6</div>
            <div class="kpi-title">Conversion Rate by Channel</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Definition</div>
            <div class="kpi-row-content">Purchase CVR calculated separately per traffic source (reveals quality vs. volume trade-off)</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">SMART</div>
            <div class="kpi-row-content"><strong>S</strong>pecific: % CVR per channel | <strong>M</strong>easurable: (purchase_users/session_users)×100 by medium | <strong>A</strong>chievable: CTE joining both event types | <strong>R</strong>elevant: budget waste identification | <strong>T</strong>ime-bound: full-period; flag <1% as issue</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Fields</div>
            <div class="kpi-row-content">traffic_source.medium, event_name IN ('session_start','purchase'), user_pseudo_id</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Visualization</div>
            <div class="kpi-row-content">Scatter Plot: X=session volume, Y=CVR%, size=revenue, color=channel. Shows volume-quality trade-off in one view.</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Action Trigger</div>
            <div class="kpi-row-content"><span class="highlight">High volume + CVR<1%</span> → diagnostic: audience targeting wrong OR landing page wrong. Different fixes, different teams.</div>
        </div>
    </div>

    <div class="section-header">GROUP 4: PRODUCT & AUDIENCE INSIGHTS</div>

    <div class="kpi-card product">
        <div class="kpi-header">
            <div class="kpi-label">KPI #7</div>
            <div class="kpi-title">Top Product Revenue Concentration</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Definition</div>
            <div class="kpi-row-content">Share of total revenue from top 5 SKUs; measures portfolio fragility and strategic risk</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">SMART</div>
            <div class="kpi-row-content"><strong>S</strong>pecific: % revenue from top 5 by name | <strong>M</strong>easurable: top5_revenue/total_revenue×100 | <strong>A</strong>chievable: UNNEST(items) then aggregate | <strong>R</strong>elevant: portfolio concentration risk | <strong>T</strong>ime-bound: full-period; flag >60%</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Fields</div>
            <div class="kpi-row-content">UNNEST(items), items.item_name, items.price, items.quantity, event_name='purchase'</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Visualization</div>
            <div class="kpi-row-content">Treemap: area ∝ revenue. Treemap chosen over pie: human eye reads area accurately vs. angles. Concentration is visually immediate.</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Action Trigger</div>
            <div class="kpi-row-content"><span class="highlight">Top 5 >60%</span> → binary decision: (A) Diversify—reallocate spend to tier-2, OR (B) Double-down—maximize margin + inventory buffer. Choice must be conscious.</div>
        </div>
    </div>

    <div class="kpi-card product">
        <div class="kpi-header">
            <div class="kpi-label">KPI #8</div>
            <div class="kpi-title">Device Conversion Gap</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Definition</div>
            <div class="kpi-row-content">Percentage-point gap between mobile's traffic share and mobile's purchase share</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">SMART</div>
            <div class="kpi-row-content"><strong>S</strong>pecific: gap in ppts (traffic% - purchase%) | <strong>M</strong>easurable: (mobile_sessions/total_sessions) - (mobile_purchases/total_purchases) | <strong>A</strong>chievable: device.category on all events | <strong>R</strong>elevant: mobile UX investment ROI | <strong>T</strong>ime-bound: full-period; flag >30 ppts</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Fields</div>
            <div class="kpi-row-content">device.category IN ('mobile','desktop','tablet'), event_name IN ('session_start','purchase'), user_pseudo_id</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Visualization</div>
            <div class="kpi-row-content">Side-by-side Donut Charts: left=traffic split by device, right=purchase split by device. Visual gap shows friction without arithmetic.</div>
        </div>
        <div class="kpi-row">
            <div class="kpi-row-label">Action Trigger</div>
            <div class="kpi-row-content"><span class="highlight">Gap >30 ppts</span> → mobile checkout UX problem, not traffic problem. Reallocate budget from campaigns to mobile development. Cross-functional brief: CMO+product+marketing.</div>
        </div>
    </div>

</div>

<!-- PAGE 4: SUMMARY -->
<div class="page">
    <h1>5. KPI Summary Table</h1>

    <table class="summary-table">
        <thead>
            <tr>
                <th>#</th>
                <th>KPI</th>
                <th>Group</th>
                <th>Visualization</th>
                <th>Action Threshold</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Total Purchase Revenue</td>
                <td>Revenue</td>
                <td>Scorecard + Bar</td>
                <td>Dec <30% above Nov</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Average Order Value</td>
                <td>Revenue</td>
                <td>Scorecard + Line</td>
                <td>Jan drops >20% below Dec</td>
            </tr>
            <tr>
                <td>3</td>
                <td>End-to-End CVR</td>
                <td>Funnel</td>
                <td>Funnel Chart</td>
                <td><2% overall</td>
            </tr>
            <tr>
                <td>4</td>
                <td>Checkout Abandonment</td>
                <td>Funnel</td>
                <td>Scorecard + Bar</td>
                <td>>50%</td>
            </tr>
            <tr>
                <td>5</td>
                <td>Revenue by Channel</td>
                <td>Traffic</td>
                <td>Horizontal Bar</td>
                <td>Organic 2x+ paid</td>
            </tr>
            <tr>
                <td>6</td>
                <td>CVR by Channel</td>
                <td>Traffic</td>
                <td>Scatter Plot</td>
                <td>Any channel <1%</td>
            </tr>
            <tr>
                <td>7</td>
                <td>Top 5 SKU Concentration</td>
                <td>Product</td>
                <td>Treemap</td>
                <td>Top 5 >60%</td>
            </tr>
            <tr>
                <td>8</td>
                <td>Device Conversion Gap</td>
                <td>Audience</td>
                <td>Donut + Donut</td>
                <td>Gap >30 ppts</td>
            </tr>
        </tbody>
    </table>

    <h2 style="margin-top: 20px;">6. Dashboard Links</h2>
    <div class="meta-info" style="margin-top: 10px;">
        <p><strong>Looker Studio:</strong> [Public dashboard link to be added]</p>
        <p><strong>Streamlit App:</strong> https://ga4-ecommerce-dashboard-kcs2lctyvdwqplth7ysxbb.streamlit.app/</p>
    </div>

    <div class="footer">
        <p>Document prepared: """ + datetime.now().strftime('%B %d, %Y') + """</p>
        <p>Measurement Framework Version 1.0 | For assignment submission</p>
    </div>
</div>

</body>
</html>
"""

# Convert HTML to PDF
try:
    HTML(string=html_content).write_pdf('/Users/rei/Desktop/Digital marketing/Measurement_Framework.pdf')
    print("✅ PDF created successfully with improved layout!")
except Exception as e:
    print(f"Error: {e}")
    print("Attempting to install weasyprint...")
    import subprocess
    subprocess.run(['pip', 'install', 'weasyprint'], check=True)
    HTML(string=html_content).write_pdf('/Users/rei/Desktop/Digital marketing/Measurement_Framework.pdf')
    print("✅ PDF created successfully!")
