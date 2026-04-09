from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from datetime import datetime

# Create PDF
pdf_path = "/Users/rei/Desktop/Digital marketing/Measurement_Framework.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                        rightMargin=0.5*inch, leftMargin=0.5*inch,
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

# Container for the 'Flowable' objects
elements = []

# Define styles
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1F77B4'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#1F77B4'),
    spaceAfter=8,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

subheading_style = ParagraphStyle(
    'Subheading',
    parent=styles['Heading3'],
    fontSize=11,
    textColor=colors.HexColor('#2C3E50'),
    spaceAfter=6,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=9,
    alignment=TA_JUSTIFY,
    spaceAfter=6
)

# ====================== PAGE 1 ======================

# Title
elements.append(Paragraph("GA4 E-COMMERCE MEASUREMENT FRAMEWORK", title_style))
elements.append(Spacer(1, 0.15*inch))

# Subtitle info
subtitle_data = [
    ["Dataset:", "bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*"],
    ["Period:", "Nov 2020 – Jan 2021 (92 days)"],
    ["Audience:", "Chief Marketing Officer (CMO)"],
    ["Dashboard Tool:", "Looker Studio / Streamlit"],
]

subtitle_table = Table(subtitle_data, colWidths=[1.2*inch, 4.8*inch])
subtitle_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
elements.append(subtitle_table)
elements.append(Spacer(1, 0.2*inch))

# ====================== SECTION 1: DATASET OVERVIEW ======================

elements.append(Paragraph("1. DATASET OVERVIEW", heading_style))

dataset_text = """
<b>GA4 Sample E-Commerce Dataset:</b> This public BigQuery dataset contains anonymized Google Analytics 4 events from a real e-commerce website.
The dataset spans 92 days (Nov 2020 – Jan 2021), capturing 230K+ user sessions and 5.7K+ purchases across multiple traffic sources and devices.
Each event includes rich context: what users viewed, added to cart, abandoned carts, and completed purchases. This temporal granularity allows precise
funnel analysis and patterns by time period, device, and channel.
"""
elements.append(Paragraph(dataset_text, body_style))
elements.append(Spacer(1, 0.15*inch))

# ====================== SECTION 2: PROBLEMS DATA SOLVES ======================

elements.append(Paragraph("2. PROBLEMS THIS DATA SOLVES", heading_style))

problems_data = [
    ["Problem", "How Data Solves It", "Key Fields"],
    ["Product-Market Misalignment",
     "Pareto analysis across SKUs reveals if 3-5 hero products drive 60%+ of revenue, signaling portfolio concentration risk and informing diversification vs. double-down strategy.",
     "items.item_name, ecommerce.purchase_revenue"],

    ["Funnel Friction",
     "Event-level tracking (session_start → view_item → add_to_cart → begin_checkout → purchase) pinpoints exact stage where users drop off, enabling targeted CRO priorities.",
     "event_name, user_pseudo_id"],

    ["Traffic Source Quality Gap",
     "Revenue attribution by traffic_source.medium (not just traffic volume) reveals which channels produce buyers. Organic may send less traffic but more revenue than paid.",
     "traffic_source.medium, traffic_source.source, ecommerce.purchase_revenue"],

    ["Device Conversion Disparity",
     "Comparing device.category across sessions vs. purchases exposes mobile checkout friction — if mobile is 40% of traffic but only 10% of purchases, the gap quantifies UX investment ROI.",
     "device.category, event_name"],
]

# Style problem solving table
problem_table = Table(problems_data, colWidths=[1.4*inch, 2.4*inch, 1.7*inch])
problem_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F77B4')),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
elements.append(problem_table)
elements.append(Spacer(1, 0.2*inch))

# ====================== SECTION 3: BUSINESS OBJECTIVE ======================

elements.append(Paragraph("3. BUSINESS OBJECTIVE", heading_style))

objective_box = """
<font color="#2CA02C"><b>PRIMARY OBJECTIVE:</b></font><br/>
Understand ecommerce performance patterns across Nov 2020 – Jan 2021 to identify conversion inefficiencies,
traffic quality gaps, and funnel friction — and use these as a baseline for growth decisions.<br/><br/>

<font color="#666666"><b>Rationale:</b> With only 92 days of data, setting a target like "20% revenue increase" is unrealistic.
Instead, we establish diagnostic baselines: Where are users dropping off? Which channels deliver profitable traffic?
Which devices have UX problems? These insights drive prioritization for the next 6-month growth cycle.</font>
"""
elements.append(Paragraph(objective_box, body_style))
elements.append(Spacer(1, 0.2*inch))

# ====================== PAGE BREAK ======================
elements.append(PageBreak())

# ====================== PAGE 2: KPIS ======================

elements.append(Paragraph("4. KEY PERFORMANCE INDICATORS (KPIs)", heading_style))
elements.append(Spacer(1, 0.1*inch))

# KPI GROUP 1: REVENUE
elements.append(Paragraph("GROUP 1: REVENUE & TRANSACTION PERFORMANCE", subheading_style))

kpi1_data = [
    ["KPI #1", "Total Purchase Revenue"],
    ["Definition", "Sum of all completed purchase transaction values (Nov – Jan full period, then monthly breakdown)"],
    ["SMART", "Specific: total $ value | Measurable: SUM(ecommerce.purchase_revenue) | Achievable: direct field | Relevant: core business metric | Time-bound: Nov-Jan period"],
    ["BigQuery Fields", "ecommerce.purchase_revenue, event_name = 'purchase', event_date"],
    ["Visualization", "Scorecard (full-period total) + Bar Chart (Nov/Dec/Jan monthly comparison)"],
    ["Action Trigger", "If December revenue <30% above November, holiday campaign underperformed. Escalate to channel mix audit."],
]

kpi1_table = Table(kpi1_data, colWidths=[1*inch, 5.5*inch])
kpi1_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#E8F4F8'), colors.white]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#1F77B4')),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(kpi1_table)
elements.append(Spacer(1, 0.12*inch))

kpi2_data = [
    ["KPI #2", "Average Order Value (AOV)"],
    ["Definition", "Revenue per completed transaction (SUM(revenue) / COUNT(DISTINCT transaction_id))"],
    ["SMART", "Specific: $ per transaction | Measurable: SUM(purchase_revenue) / COUNT(DISTINCT transaction_id) | Achievable: both fields available | Relevant: efficiency metric (margin per customer) | Time-bound: monthly trend Nov-Dec-Jan"],
    ["BigQuery Fields", "ecommerce.purchase_revenue, ecommerce.transaction_id, event_name = 'purchase'"],
    ["Visualization", "Scorecard (full-period AOV) + Line Chart (monthly trend to show seasonal direction)"],
    ["Action Trigger", "If Jan AOV drops >20% below Dec, post-holiday deflation is significant. Activate bundle promo or min-basket free-shipping to defend AOV."],
]

kpi2_table = Table(kpi2_data, colWidths=[1*inch, 5.5*inch])
kpi2_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#E8F4F8'), colors.white]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#1F77B4')),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(kpi2_table)
elements.append(Spacer(1, 0.15*inch))

# KPI GROUP 2: FUNNEL
elements.append(Paragraph("GROUP 2: FUNNEL & CONVERSION EFFICIENCY", subheading_style))

kpi3_data = [
    ["KPI #3", "End-to-End Conversion Rate"],
    ["Definition", "% of sessions that result in a purchase (sessions with ≥1 purchase event)"],
    ["SMART", "Specific: % sessions → purchases | Measurable: (purchase_users / session_users) × 100 | Achievable: both events tracked | Relevant: site efficiency independent of traffic volume | Time-bound: full-period baseline + monthly breakdown"],
    ["BigQuery Fields", "event_name IN ('session_start', 'purchase'), user_pseudo_id"],
    ["Visualization", "Funnel Chart (session_start → view_item → add_to_cart → begin_checkout → purchase) showing user counts at each stage and drop-off %"],
    ["Action Trigger", "Overall CVR <2% = CRO escalation. Funnel granularity routes fixes: view_item→add_to_cart drop >10% = product page audit; begin_checkout→purchase drop <50% = checkout UX audit."],
]

kpi3_table = Table(kpi3_data, colWidths=[1*inch, 5.5*inch])
kpi3_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#FFF4E6'), colors.white]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#FF7F0E')),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(kpi3_table)
elements.append(Spacer(1, 0.12*inch))

kpi4_data = [
    ["KPI #4", "Checkout Abandonment Rate"],
    ["Definition", "% of checkout starters who do NOT complete purchase (highest-intent funnel stage loss)"],
    ["SMART", "Specific: % begin_checkout without purchase | Measurable: ((checkout_users - purchase_users) / checkout_users) × 100 | Achievable: direct events | Relevant: cheapest revenue recovery (no acquisition spend required) | Time-bound: full-period rate + Nov/Dec/Jan monthly comparison"],
    ["BigQuery Fields", "event_name IN ('begin_checkout', 'purchase'), user_pseudo_id"],
    ["Visualization", "Large Scorecard (abandonment %) + Grouped Bar Chart (monthly trend Nov/Dec/Jan) to show seasonality in checkout friction"],
    ["Action Trigger", "Abandonment >50%  = immediate UX audit: payment option variety, form field count, trust badges, mobile checkout. Requires product/UX team investment, not marketing."],
]

kpi4_table = Table(kpi4_data, colWidths=[1*inch, 5.5*inch])
kpi4_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#FFF4E6'), colors.white]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#FF7F0E')),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(kpi4_table)

elements.append(PageBreak())

# ====================== PAGE 3: KPIS CONTINUED ======================

# KPI GROUP 3: TRAFFIC
elements.append(Paragraph("GROUP 3: TRAFFIC SOURCE QUALITY", heading_style))

kpi5_data = [
    ["KPI #5", "Revenue by Traffic Channel"],
    ["Definition", "Total purchase revenue attributed to each traffic source medium (organic, cpc, email, direct, referral)"],
    ["SMART", "Specific: $ revenue per traffic_source.medium | Measurable: SUM(purchase_revenue) GROUP BY traffic_source.medium | Achievable: direct fields | Relevant: primary input for budget reallocation decisions | Time-bound: full-period total + monthly drill-down"],
    ["BigQuery Fields", "traffic_source.medium, traffic_source.source, ecommerce.purchase_revenue, event_name = 'purchase'"],
    ["Visualization", "Horizontal Bar Chart (channels ranked high→low revenue). Horizontal labels render cleanly and list is read as priority ranking."],
    ["Action Trigger", "If organic 2x+ paid: CMO likely over-spending on paid. Shift budget to content/SEO. If paid >organic: justify scaling with KPI #6 quality check first."],
]

kpi5_table = Table(kpi5_data, colWidths=[1*inch, 5.5*inch])
kpi5_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#E6F5E6'), colors.white]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#2CA02C')),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(kpi5_table)
elements.append(Spacer(1, 0.12*inch))

kpi6_data = [
    ["KPI #6", "Conversion Rate by Channel"],
    ["Definition", "Purchase conversion rate calculated separately for each traffic_source.medium; reveals quality vs. volume trade-off"],
    ["SMART", "Specific: % CVR per channel | Measurable: (purchase_users / session_users) by medium | Achievable: requires CTE joining both event types per medium | Relevant: identifies budget waste (high volume, low CVR) vs. efficiency (low volume, high CVR) | Time-bound: full-period rate; flag any channel <1% as structural issue"],
    ["BigQuery Fields", "traffic_source.medium, event_name IN ('session_start', 'purchase'), user_pseudo_id"],
    ["Visualization", "Scatter Plot: X-axis = session volume, Y-axis = CVR %, size = revenue. 2D plot reveals volume-quality trade-off (top-right=scale; bottom-right=waste; top-left=opportunity)."],
    ["Action Trigger", "High volume + CVR <1% = immediate diagnostic: targeting wrong (audience issue) or landing page wrong (creative/messaging issue). Different fixes, different teams."],
]

kpi6_table = Table(kpi6_data, colWidths=[1*inch, 5.5*inch])
kpi6_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#E6F5E6'), colors.white]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#2CA02C')),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(kpi6_table)
elements.append(Spacer(1, 0.15*inch))

# KPI GROUP 4: PRODUCT & AUDIENCE
elements.append(Paragraph("GROUP 4: PRODUCT & AUDIENCE INSIGHTS", subheading_style))

kpi7_data = [
    ["KPI #7", "Top Product Revenue Concentration"],
    ["Definition", "Share of total revenue generated by top 5 SKUs; measures portfolio fragility and strategic risk"],
    ["SMART", "Specific: % revenue from top 5 by name | Measurable: top_5_sku_revenue / total_revenue × 100 | Achievable: requires UNNEST(items) then aggregation by item_name | Relevant: flags portfolio concentration risk invisible without data | Time-bound: full-period concentration figure; flag if top 5 >60%"],
    ["BigQuery Fields", "UNNEST(items), items.item_name, items.price, items.quantity, event_name = 'purchase'"],
    ["Visualization", "Treemap where rectangle area ∝ revenue. Treemap chosen over pie: human eye reads area accurately, concentration problem is visually immediate without arithmetic."],
    ["Action Trigger", "Top 5 SKUs >60% revenue = binary decision: (A) Diversify: reallocate marketing spend to tier-2 products; OR (B) Double-down: maximize margin on hero products + inventory buffer. Both valid; choice must be conscious."],
]

kpi7_table = Table(kpi7_data, colWidths=[1*inch, 5.5*inch])
kpi7_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#F0E6FF'), colors.white]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#9467BD')),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(kpi7_table)
elements.append(Spacer(1, 0.12*inch))

kpi8_data = [
    ["KPI #8", "Device Conversion Gap"],
    ["Definition", "Percentage-point difference between mobile's share of traffic and mobile's share of purchases; quantifies mobile UX friction"],
    ["SMART", "Specific: gap in ppts between traffic% and purchase% mobile | Measurable: (mobile_sessions% - mobile_purchases%) in ppts | Achievable: device.category available on all events | Relevant: quantifies mobile investment ROI; justifies UX budget reallocation | Time-bound: full-period gap; flag if >30 ppts"],
    ["BigQuery Fields", "device.category IN ('mobile', 'desktop', 'tablet'), event_name IN ('session_start', 'purchase'), user_pseudo_id"],
    ["Visualization", "Side-by-side Donut Charts: left=traffic split by device, right=purchase split by device. Visual gap between mobile's slice left vs. right immediately shows conversion disparity without arithmetic."],
    ["Action Trigger", "Gap >30 ppts = mobile checkout problem, not traffic problem. Reallocate budget from paid campaigns to mobile UX development. Cross-functional: CMO briefs marketing & product teams with same data."],
]

kpi8_table = Table(kpi8_data, colWidths=[1*inch, 5.5*inch])
kpi8_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#F0E6FF'), colors.white]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#9467BD')),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(kpi8_table)

elements.append(Spacer(1, 0.2*inch))

# Summary table
elements.append(Paragraph("5. KPI SUMMARY TABLE", heading_style))

summary_data = [
    ["#", "KPI", "Group", "Visualization", "Action Threshold"],
    ["1", "Total Purchase Revenue", "Revenue", "Scorecard + Bar", "Dec <30% above Nov"],
    ["2", "Average Order Value", "Revenue", "Scorecard + Line", "Jan drops >20% below Dec"],
    ["3", "End-to-End CVR", "Funnel", "Funnel Chart", "<2% overall"],
    ["4", "Checkout Abandonment", "Funnel", "Scorecard + Bar", ">50%"],
    ["5", "Revenue by Channel", "Traffic", "Horizontal Bar", "Organic 2x+ paid"],
    ["6", "CVR by Channel", "Traffic", "Scatter Plot", "Any channel <1%"],
    ["7", "Top 5 SKU Concentration", "Product", "Treemap", "Top 5 >60%"],
    ["8", "Device Conversion Gap", "Audience", "Side-by-side Donuts", "Gap >30 ppts"],
]

summary_table = Table(summary_data, colWidths=[0.4*inch, 1.8*inch, 1*inch, 1.5*inch, 1.2*inch])
summary_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F77B4')),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#1F77B4')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
elements.append(summary_table)

elements.append(Spacer(1, 0.3*inch))

# Footer
footer_text = f"""
<b>Dashboard Links:</b><br/>
Looker Studio: [Public link to be inserted]<br/>
Streamlit: https://ga4-ecommerce-dashboard-kcs2lctyvdwqplth7ysxbb.streamlit.app/<br/><br/>

<b>Document prepared:</b> {datetime.now().strftime('%B %d, %Y')}<br/>
<b>Measurement Framework Version:</b> 1.0
"""

elements.append(Paragraph(footer_text, ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=8,
    textColor=colors.HexColor('#666666'),
    alignment=TA_LEFT
)))

# Build PDF
doc.build(elements)
print(f"✅ PDF created successfully: {pdf_path}")
