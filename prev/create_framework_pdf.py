from fpdf import FPDF
from datetime import datetime

# Create PDF
pdf = FPDF(format='Letter')
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Title
pdf.set_font("Helvetica", "B", 18)
pdf.set_text_color(31, 119, 180)
pdf.cell(0, 12, "GA4 E-COMMERCE MEASUREMENT FRAMEWORK", 0, 1, "C")
pdf.set_draw_color(31, 119, 180)
pdf.set_line_width(1)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(5)

# Meta Info
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(50, 62, 80)
pdf.cell(35, 5, "Dataset:", 0, 0)
pdf.cell(165, 5, "bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*", 0, 1)
pdf.cell(35, 5, "Period:", 0, 0)
pdf.cell(165, 5, "Nov 2020 - Jan 2021 (92 days)", 0, 1)
pdf.cell(35, 5, "Audience:", 0, 0)
pdf.cell(165, 5, "Chief Marketing Officer (CMO)", 0, 1)
pdf.cell(35, 5, "Tools:", 0, 0)
pdf.cell(165, 5, "Looker Studio / Streamlit", 0, 1)
pdf.ln(3)

# Section 1: Overview
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(31, 119, 180)
pdf.cell(0, 8, "1. DATASET OVERVIEW", 0, 1)

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(0, 0, 0)
overview_text = "This GA4 sample dataset contains 230K+ user sessions and 5.7K+ purchases. Events are granular: session_start > view_item > add_to_cart > begin_checkout > purchase. Each event carries context: traffic source, device, products viewed, and revenue."
pdf.multi_cell(190, 5, overview_text)
pdf.ln(3)

# Section 2: Problems
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(31, 119, 180)
pdf.cell(0, 8, "2. PROBLEMS THIS DATA SOLVES", 0, 1)

problems = [
    ("Product-Market Misalignment", "Pareto analysis reveals if top 5 SKUs drive 60%+ revenue, flagging portfolio concentration risk."),
    ("Funnel Friction", "Event sequences pinpoint exact drop-off: View>Cart leak? Fix product page. Checkout leak? Fix form UX."),
    ("Traffic Source Quality Gap", "Revenue attribution by channel shows which produce buyers. Organic often outperforms paid despite lower volume."),
    ("Device Conversion Disparity", "If mobile is 40% traffic but 10% purchases = 30 ppt gap quantifies mobile UX investment ROI."),
]

for problem_title, problem_desc in problems:
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(255, 127, 14)
    pdf.cell(0, 5, "- " + problem_title, 0, 1)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(190, 4, problem_desc)
    pdf.ln(1)

pdf.ln(2)

# Section 3: Business Objective
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(31, 119, 180)
pdf.cell(0, 8, "3. BUSINESS OBJECTIVE", 0, 1)

pdf.set_fill_color(232, 245, 233)
pdf.set_draw_color(102, 187, 106)
pdf.set_line_width(0.5)
pdf.rect(10, pdf.get_y(), 190, 1, 'F')
pdf.ln(2)

pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(44, 160, 44)
obj_text = "Understand ecommerce patterns across Nov 2020-Jan 2021 to identify conversion inefficiencies, traffic quality gaps, and funnel friction as baseline for growth decisions."
pdf.multi_cell(190, 5, obj_text)
pdf.ln(2)

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(0, 0, 0)
rationale = "Rationale: With only 92 days of data, revenue targets are unrealistic. Instead, establish diagnostic baselines: Where do users drop off? Which channels convert? Which devices have UX problems? These insights drive prioritization."
pdf.multi_cell(190, 4, rationale)

pdf.ln(5)

# PAGE 2
pdf.add_page()

pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(31, 119, 180)
pdf.cell(0, 8, "4. KEY PERFORMANCE INDICATORS", 0, 1)
pdf.ln(2)

# Group 1
pdf.set_font("Helvetica", "B", 11)
pdf.set_fill_color(31, 119, 180)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 6, "GROUP 1: REVENUE & TRANSACTION PERFORMANCE", 0, 1, 'C', True)
pdf.ln(1)

# KPI 1
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(44, 160, 44)
pdf.cell(0, 6, "KPI #1: Total Purchase Revenue", 0, 1)

pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(0, 0, 0)
pdf.cell(25, 4, "Definition:", 0, 0)
pdf.multi_cell(165, 4, "Sum of all completed purchase values (Nov-Jan period, then monthly breakdown)")

pdf.cell(25, 4, "Measurement:", 0, 0)
pdf.multi_cell(165, 4, "SUM(ecommerce.purchase_revenue) WHERE event_name='purchase'")

pdf.cell(25, 4, "Visualization:", 0, 0)
pdf.multi_cell(165, 4, "Scorecard (full-period) + Bar Chart (Nov/Dec/Jan showing holiday spike)")

pdf.cell(25, 4, "Action:", 0, 0)
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(206, 30, 8)
pdf.multi_cell(165, 4, "Dec revenue <30% above Nov = holiday underperformed. Audit channel mix.")
pdf.ln(1)

# KPI 2
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(44, 160, 44)
pdf.cell(0, 6, "KPI #2: Average Order Value", 0, 1)

pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(0, 0, 0)
pdf.cell(25, 4, "Definition:", 0, 0)
pdf.multi_cell(165, 4, "Revenue per transaction (total revenue / distinct transaction count)")

pdf.cell(25, 4, "Measurement:", 0, 0)
pdf.multi_cell(165, 4, "SUM(purchase_revenue) / COUNT(DISTINCT transaction_id)")

pdf.cell(25, 4, "Visualization:", 0, 0)
pdf.multi_cell(165, 4, "Scorecard (full-period AOV) + Line Chart (monthly trend)")

pdf.cell(25, 4, "Action:", 0, 0)
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(206, 30, 8)
pdf.multi_cell(165, 4, "Jan >20% below Dec = activate bundle promo or min-basket free-shipping")
pdf.ln(2)

# Group 2
pdf.set_font("Helvetica", "B", 11)
pdf.set_fill_color(31, 119, 180)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 6, "GROUP 2: FUNNEL & CONVERSION EFFICIENCY", 0, 1, 'C', True)
pdf.ln(1)

# KPI 3
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(255, 127, 14)
pdf.cell(0, 6, "KPI #3: End-to-End Conversion Rate", 0, 1)

pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(0, 0, 0)
pdf.cell(25, 4, "Definition:", 0, 0)
pdf.multi_cell(165, 4, "% of sessions resulting in purchase (independent of traffic volume)")

pdf.cell(25, 4, "Measurement:", 0, 0)
pdf.multi_cell(165, 4, "COUNT(purchase users) / COUNT(session starters) x 100")

pdf.cell(25, 4, "Visualization:", 0, 0)
pdf.multi_cell(165, 4, "Funnel Chart: session_start > view_item > add_to_cart > begin_checkout > purchase")

pdf.cell(25, 4, "Action:", 0, 0)
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(206, 30, 8)
pdf.multi_cell(165, 4, "CVR <2% = CRO escalation. Funnel shows which stage to fix first.")
pdf.ln(1)

# KPI 4
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(255, 127, 14)
pdf.cell(0, 6, "KPI #4: Checkout Abandonment Rate", 0, 1)

pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(0, 0, 0)
pdf.cell(25, 4, "Definition:", 0, 0)
pdf.multi_cell(165, 4, "% of checkout starters not completing purchase (highest-intent users)")

pdf.cell(25, 4, "Measurement:", 0, 0)
pdf.multi_cell(165, 4, "((checkout users - purchase users) / checkout users) x 100")

pdf.cell(25, 4, "Visualization:", 0, 0)
pdf.multi_cell(165, 4, "Scorecard (abandonment %) + Bar Chart (monthly Nov/Dec/Jan)")

pdf.cell(25, 4, "Action:", 0, 0)
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(206, 30, 8)
pdf.multi_cell(165, 4, "Abandonment >50% = audit payment options, forms, trust badges, mobile")
pdf.ln(2)

# PAGE 3
pdf.add_page()

# Group 3
pdf.set_font("Helvetica", "B", 11)
pdf.set_fill_color(31, 119, 180)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 6, "GROUP 3: TRAFFIC SOURCE QUALITY", 0, 1, 'C', True)
pdf.ln(1)

# KPI 5
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(44, 160, 44)
pdf.cell(0, 6, "KPI #5: Revenue by Traffic Channel", 0, 1)

pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(0, 0, 0)
pdf.cell(25, 4, "Definition:", 0, 0)
pdf.multi_cell(165, 4, "Purchase revenue attributed to each traffic_source.medium")

pdf.cell(25, 4, "Measurement:", 0, 0)
pdf.multi_cell(165, 4, "SUM(purchase_revenue) GROUP BY traffic_source.medium")

pdf.cell(25, 4, "Visualization:", 0, 0)
pdf.multi_cell(165, 4, "Horizontal Bar Chart (channels ranked high-to-low revenue)")

pdf.cell(25, 4, "Action:", 0, 0)
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(206, 30, 8)
pdf.multi_cell(165, 4, "Organic 2x+ paid = over-spending on paid. Shift to content/SEO.")
pdf.ln(1)

# KPI 6
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(44, 160, 44)
pdf.cell(0, 6, "KPI #6: Conversion Rate by Channel", 0, 1)

pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(0, 0, 0)
pdf.cell(25, 4, "Definition:", 0, 0)
pdf.multi_cell(165, 4, "CVR per traffic source (reveals quality vs. volume trade-off)")

pdf.cell(25, 4, "Measurement:", 0, 0)
pdf.multi_cell(165, 4, "(purchase users / session users) x 100 by traffic_source.medium")

pdf.cell(25, 4, "Visualization:", 0, 0)
pdf.multi_cell(165, 4, "Scatter: X=volume, Y=CVR%, size=revenue. Shows efficiency trade-offs.")

pdf.cell(25, 4, "Action:", 0, 0)
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(206, 30, 8)
pdf.multi_cell(165, 4, "High volume + CVR<1% = diagnostic: wrong audience OR wrong message")
pdf.ln(2)

# Group 4
pdf.set_font("Helvetica", "B", 11)
pdf.set_fill_color(31, 119, 180)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 6, "GROUP 4: PRODUCT & AUDIENCE INSIGHTS", 0, 1, 'C', True)
pdf.ln(1)

# KPI 7
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(148, 103, 189)
pdf.cell(0, 6, "KPI #7: Top Product Revenue Concentration", 0, 1)

pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(0, 0, 0)
pdf.cell(25, 4, "Definition:", 0, 0)
pdf.multi_cell(165, 4, "Share of total revenue from top 5 SKUs (portfolio fragility)")

pdf.cell(25, 4, "Measurement:", 0, 0)
pdf.multi_cell(165, 4, "Sum(top 5 SKU revenue) / Total revenue x 100")

pdf.cell(25, 4, "Visualization:", 0, 0)
pdf.multi_cell(165, 4, "Treemap (area proportional to revenue - better than pie)")

pdf.cell(25, 4, "Action:", 0, 0)
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(206, 30, 8)
pdf.multi_cell(165, 4, "Top 5 >60% = choose: Diversify to tier-2 OR Double-down on heroes")
pdf.ln(1)

# KPI 8
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(148, 103, 189)
pdf.cell(0, 6, "KPI #8: Device Conversion Gap", 0, 1)

pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(0, 0, 0)
pdf.cell(25, 4, "Definition:", 0, 0)
pdf.multi_cell(165, 4, "Gap between mobile traffic share and mobile purchase share (ppts)")

pdf.cell(25, 4, "Measurement:", 0, 0)
pdf.multi_cell(165, 4, "(mobile_sessions % of total) - (mobile_purchases % of total)")

pdf.cell(25, 4, "Visualization:", 0, 0)
pdf.multi_cell(165, 4, "Side-by-side Donuts (left=traffic, right=purchases)")

pdf.cell(25, 4, "Action:", 0, 0)
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(206, 30, 8)
pdf.multi_cell(165, 4, "Gap >30 ppts = mobile UX problem. Reallocate to development.")
pdf.ln(5)

# PAGE 4: Summary Table
pdf.add_page()

pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(31, 119, 180)
pdf.cell(0, 8, "5. KPI SUMMARY TABLE", 0, 1)
pdf.ln(2)

# Table
pdf.set_font("Helvetica", "B", 8)
pdf.set_fill_color(31, 119, 180)
pdf.set_text_color(255, 255, 255)
col_widths = [10, 30, 20, 30, 40]

headers = ["#", "KPI", "Group", "Visualization", "Action Threshold"]
for i, header in enumerate(headers):
    pdf.cell(col_widths[i], 6, header, 1, 0, 'C', True)
pdf.ln()

data = [
    ["1", "Total Purchase Revenue", "Revenue", "Scorecard + Bar", "Dec <30% above Nov"],
    ["2", "Average Order Value", "Revenue", "Scorecard + Line", "Jan >20% below Dec"],
    ["3", "End-to-End CVR", "Funnel", "Funnel Chart", "<2% overall"],
    ["4", "Checkout Abandonment", "Funnel", "Scorecard + Bar", ">50%"],
    ["5", "Revenue by Channel", "Traffic", "Horizontal Bar", "Organic 2x+ paid"],
    ["6", "CVR by Channel", "Traffic", "Scatter Plot", "Any <1% CVR"],
    ["7", "Top 5 SKU Concentration", "Product", "Treemap", "Top 5 >60%"],
    ["8", "Device Conversion Gap", "Audience", "Donut + Donut", "Gap >30 ppts"],
]

pdf.set_font("Helvetica", "", 8)
pdf.set_text_color(0, 0, 0)

for i, row in enumerate(data):
    for j, cell in enumerate(row):
        if i % 2 == 0:
            pdf.set_fill_color(245, 250, 255)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(col_widths[j], 5, cell, 1, 0, 'L', True)
    pdf.ln()

pdf.ln(5)

# Dashboard Links
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(31, 119, 180)
pdf.cell(0, 6, "6. DASHBOARD LINKS", 0, 1)
pdf.ln(2)

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(0, 0, 0)
pdf.cell(40, 5, "Looker Studio:", 0, 0)
pdf.cell(150, 5, "[Public dashboard link to be added]", 0, 1)
pdf.ln(1)

pdf.cell(40, 5, "Streamlit App:", 0, 0)
pdf.set_font("Helvetica", "", 8)
pdf.cell(150, 5, "https://ga4-ecommerce-dashboard-kcs2lctyvdwqplth7ysxbb.streamlit.app/", 0, 1)

pdf.ln(10)

# Footer
pdf.set_font("Helvetica", "I", 8)
pdf.set_text_color(128, 128, 128)
pdf.cell(0, 5, f"Document prepared: {datetime.now().strftime('%B %d, %Y')}", 0, 1, 'C')
pdf.cell(0, 5, "Measurement Framework Version 1.0 | Assignment Submission", 0, 1, 'C')

# Save PDF
pdf.output('/Users/rei/Desktop/Digital marketing/Measurement_Framework.pdf')
print("SUCCESS! PDF created with professional layout.")
print("File: /Users/rei/Desktop/Digital marketing/Measurement_Framework.pdf")
