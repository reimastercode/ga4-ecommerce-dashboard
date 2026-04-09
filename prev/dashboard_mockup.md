# GA4 E-Commerce Dashboard — Visual Mockup
## For CMO | Nov 2020 – Jan 2021

---

## **LAYOUT STRUCTURE**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  🎯 E-COMMERCE PERFORMANCE DASHBOARD                        [Filters] [Settings]│
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  GLOBAL FILTERS (Sticky at top)                                               │
│  [ Date Range: Nov 2020 - Jan 2021 ▼ ]  [ Traffic Source: All ▼ ]           │
│  [ Device: All ▼ ]  [ Reset Filters ]                                        │
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  📊 SECTION 1: REVENUE & TRANSACTION PERFORMANCE                              │
│  ────────────────────────────────────────────────────────────────────────────  │
│                                                                                 │
│  ┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────┐│
│  │   Total Revenue        │  │  Avg Order Value       │  │   Total Orders     ││
│  │                        │  │                        │  │                    ││
│  │  $651,422              │  │  $114.28               │  │  5,704             ││
│  │  Full Period          │  │  Full Period          │  │  Full Period       ││
│  │                        │  │                        │  │                    ││
│  └────────────────────────┘  └────────────────────────┘  └────────────────────┘│
│                                                                                 │
│  ┌──────────────────────────────────────┐  ┌──────────────────────────────────┐│
│  │ Revenue by Month (Full-Period View)  │  │  AOV Trend (Oct → Feb)            ││
│  │                                      │  │  [LINE CHART]                     ││
│  │ [BAR CHART]                          │  │  $140 ──────┐                     ││
│  │            ┌─────────────────────────┤  │            │   ┌─ higher         ││
│  │    $300K   │                         │  │ $120       ├──┘                   ││
│  │            │   ┌──────────────┐      │  │            │ ┌─ seasonal dip    ││
│  │    $200K   │   │ DEC (Holiday)│      │  │ $100 ──────┘─┬─────────         ││
│  │    $100K   │───┘──────┬───────┴──────┤  │    Nov  Dec  Jan  Feb            ││
│  │      $0 ───┴─ Nov Dec Jan           │  │                                  ││
│  └──────────────────────────────────────┘  └──────────────────────────────────┘│
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  🔄 SECTION 2: FUNNEL & CONVERSION EFFICIENCY                                 │
│  ────────────────────────────────────────────────────────────────────────────  │
│                                                                                 │
│  ┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────┐│
│  │ End-to-End CVR         │  │ Checkout Abandonment   │  │   Session Starters │
│  │                        │  │                        │  │                    ││
│  │  2.48%                 │  │  67.3%                 │  │  229,927           ││
│  │  Full Period          │  │  Full Period          │  │  Full Period       ││
│  │  (Target: 2%+)        │  │  (Alert if >50%)       │  │                    ││
│  │                        │  │                        │  │                    ││
│  └────────────────────────┘  └────────────────────────┘  └────────────────────┘│
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │  Funnel Breakdown: Session Start → Purchase (Full Period)                 │ │
│  │                                                                           │ │
│  │  ┌────────────────────────────────────────────────────────────────────┐  │ │
│  │  │ 229,927 sessions                                                   │  │ │
│  │  └────────────────────────────────────────────────────────────────────┘  │ │
│  │           ↓ (88% continue)                                              │ │
│  │  ┌────────────────────────────────────────────────────────────────────┐  │ │
│  │  │ 201,952 viewed items                                               │  │ │
│  │  └────────────────────────────────────────────────────────────────────┘  │ │
│  │           ↓ (12% add to cart)                                           │ │
│  │  ┌────────────────────────────────────────────────────────────────────┐  │ │
│  │  │ 24,234 added to cart                                               │  │ │
│  │  └────────────────────────────────────────────────────────────────────┘  │ │
│  │           ↓ (78% begin checkout)                                        │ │
│  │  ┌────────────────────────────────────────────────────────────────────┐  │ │
│  │  │ 18,903 began checkout                                              │  │ │
│  │  └────────────────────────────────────────────────────────────────────┘  │ │
│  │           ↓ (30% complete)                                              │ │
│  │  ┌────────────────────────────────────────────────────────────────────┐  │ │
│  │  │ 5,704 completed purchases                                           │  │ │
│  │  └────────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                           │ │
│  │  Biggest friction: View Item → Add to Cart (88% drop-off)               │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌───────────────────────────────────────────┐  ┌───────────────────────────┐ │
│  │ CVR & Abandonment Rate by Month           │  │ Checkout Abandonment      │ │
│  │                                           │  │ by Month                  │ │
│  │ [GROUPED BAR CHART]                       │  │ [LINE CHART]              │ │
│  │  Nov    Dec    Jan                        │  │  70% ──┐                  │ │
│  │  ▐▌▐▌  ▐▌▐▌  ▐▌▐▌  CVR (blue)            │  │        │ Dec (higher)   │ │
│  │        Abandon (orange)                   │  │ 65% ──┼──┐              │ │
│  │                                           │  │        │  └─ Nov, Jan   │ │
│  │                                           │  │ 60% ───┘                  │ │
│  └───────────────────────────────────────────┘  └───────────────────────────┘ │
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  🚀 SECTION 3: TRAFFIC SOURCE QUALITY                                         │
│  ────────────────────────────────────────────────────────────────────────────  │
│                                                                                 │
│  ┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────┐│
│  │ Organic (Search)       │  │ Direct                 │  │ Paid Search (CPC)  ││
│  │                        │  │                        │  │                    ││
│  │  $284,322 revenue      │  │  $187,562 revenue      │  │  $156,891 revenue  ││
│  │  2.89% CVR             │  │  3.14% CVR             │  │  1.42% CVR         ││
│  │  ✓ Best quality        │  │  ✓ High quality        │  │  ⚠ Low efficiency │
│  │                        │  │                        │  │                    ││
│  └────────────────────────┘  └────────────────────────┘  └────────────────────┘│
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ Revenue by Traffic Channel (Full Period)                                 │ │
│  │                                                                          │ │
│  │ [HORIZONTAL BAR CHART]                                                  │ │
│  │                                                                          │ │
│  │ Organic Search ─────────────────────────────────────────────── $284K    │ │
│  │ Direct          ─────────────────────────────────────── $187K           │ │
│  │ Paid Search     ──────────────────────────────────── $156K             │ │
│  │ Social Media    ──────────────────────────────── $18K                  │ │
│  │ Referral        ──────────────────────── $5K                           │ │
│  │                                                                          │ │
│  │ [Dark/light coloring by channel importance]                             │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ Conversion Efficiency by Channel (Full Period)                           │ │
│  │                                                                          │ │
│  │ [SCATTER PLOT: X=Session Volume, Y=CVR, Size=Revenue]                  │ │
│  │                                                                          │ │
│  │  CVR                                                                     │ │
│  │  3.5% ──────────────────────────────────        ● Direct (small vol)    │ │
│  │        ●Organic (high vol, high CVR) ✓          [large circle]          │ │
│  │  2.5% ─────────────────────────────────────                             │ │
│  │                                                     ● Paid (high vol)    │ │
│  │  1.5% ──────────────────────────────────────────  low CVR ⚠             │ │
│  │        ●Social (low vol, low CVR)                 [medium circle]       │ │
│  │  0.5% ──────────────────────────────────────────                        │ │
│  │       0       50K      100K     150K    200K   Session Volume           │ │
│  │                                                                          │ │
│  │ Insight: Scale organic (high vol + CVR).                                │ │
│  │          Investigate paid (high vol but low CVR).                       │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ Channel Performance by Month                                            │ │
│  │                                                                          │ │
│  │ [STACKED BAR CHART: Revenue share by channel, Nov/Dec/Jan]             │ │
│  │   100% ┌──────┬──────┬──────┐                                           │ │
│  │        │Ref.$5│Soc.$│$9│Ref│ Referral                                   │ │
│  │        ├──────┼──────┼──────┤                                           │ │
│  │     75%│          CPC $156K│ Paid Search                                │ │
│  │        ├──────┼──────┼──────┤                                           │ │
│  │     50%│      Direct $187K │ Direct                                     │ │
│  │        ├──────┼──────┼──────┤                                           │ │
│  │     25%│    Organic $284K   │ Organic                                   │ │
│  │        ├──────┼──────┼──────┤                                           │ │
│  │      0%└──────┴──────┴──────┘                                           │ │
│  │        Nov    Dec    Jan                                                │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  🎁 SECTION 4: PRODUCT & AUDIENCE INSIGHTS                                   │
│  ────────────────────────────────────────────────────────────────────────────  │
│                                                                                 │
│  ┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────┐│
│  │ Top 5 SKUs Revenue     │  │ Desktop               │  │ Mobile             ││
│  │ Concentration          │  │                       │  │                    ││
│  │                        │  │ 58% of traffic        │  │ 42% of traffic     ││
│  │  62% of Total          │  │ 72% of purchases      │  │ 28% of purchases   ││
│  │  ⚠ HIGH RISK          │  │                       │  │ ⚠ Gap: 44 ppts     ││
│  │  (Recommend diversify) │  │ 4.51% CVR             │  │ 1.05% CVR          ││
│  │                        │  │                       │  │ 4.3x worse         ││
│  └────────────────────────┘  └────────────────────────┘  └────────────────────┘│
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ Top 5 Products by Revenue (Treemap View)                                │ │
│  │                                                                          │ │
│  │ ┌─────────────────────────────────────────────────────────────────────┐ │ │
│  │ │                                                                     │ │ │
│  │ │  ┌──────────────────────────────────┐  ┌───────────────────────┐  │ │ │
│  │ │  │                                  │  │                       │  │ │ │
│  │ │  │    Product_A                     │  │    Product_B          │  │ │ │
│  │ │  │    $187,832 (28.8%)             │  │    $134,221 (20.6%)   │  │ │ │
│  │ │  │                                  │  │                       │  │ │ │
│  │ │  └──────────────────────────────────┘  └───────────────────────┘  │ │ │
│  │ │                                                                     │ │ │
│  │ │  ┌──────────────────────────────────┐  ┌───────────────────────┐  │ │ │
│  │ │  │    Product_C                     │  │   Product_D │Product_E│  │ │ │
│  │ │  │    $98,456 (15.1%)              │  │   $45K│$32K (combined) │  │ │ │
│  │ │  │                                  │  │                       │  │ │ │
│  │ │  └──────────────────────────────────┘  └───────────────────────┘  │ │ │
│  │ │               [Remaining products: 12.9%]                           │ │ │
│  │ │                                                                     │ │ │
│  │ └─────────────────────────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ Mobile vs Desktop: Traffic & Purchase Distribution                     │ │
│  │                                                                          │ │
│  │  Traffic Distribution              Purchase Distribution                │ │
│  │  (Sessions by Device)              (Orders by Device)                   │ │
│  │                                                                          │ │
│  │    Mobile 42%                         Mobile 28%                         │ │
│  │  ╱─────────╲                        ╱────────╲                          │ │
│  │ │           │                      │          │                         │ │
│  │ │   42% M   │                      │   28% M  │  ← 14 point gap         │ │
│  │ │           │                      │          │     shows mobile         │ │
│  │ │           │                      │          │     checkout friction    │ │
│  │  ╲─────────╱                        ╲────────╱                          │ │
│  │    Desktop 58%                        Desktop 72%                        │ │
│  │                                                                          │ │
│  │ ⚠️ ACTION: Audit mobile checkout UX                                     │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ Mobile vs Desktop Performance by Month                                  │ │
│  │                                                                          │ │
│  │ [GROUPED BAR CHART: CVR by device across Nov/Dec/Jan]                  │ │
│  │                                                                          │ │
│  │  CVR                                                                     │ │
│  │  5% ┌──┬──┬──┐                                                          │ │
│  │     │  │  │  │  Desktop (blue)    ■ Mobile (orange)                    │ │
│  │ 4.5%│  │  │  │  ▲ Consistently better                                  │ │
│  │     ├──┼──┼──┤                                                          │ │
│  │ 4.0%│  │  │  │                                                          │ │
│  │     ├──┼──┼──┤                                                          │ │
│  │ 1.5%│  │  │  │ Mobile always below desktop                             │ │
│  │     └──┴──┴──┘                                                          │ │
│  │    Nov  Dec  Jan                                                        │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘


```

---

## **NAVIGATION & INTERACTIVITY**

### **Global Filters (Sticky Header)**
```
[📅 Date Range]  [🌐 Traffic Source]  [📱 Device]  [Reset All]
```
- **Date Range**: Pick custom dates, pre-set to Nov 2020 – Jan 2021
  - Also offers monthly views: "Nov Only", "Dec Only", "Jan Only"
- **Traffic Source**: All, Organic, Direct, Paid Search, Social, Referral
- **Device**: All, Mobile, Desktop, Tablet
- All charts cascade — change filters and all visualizations update instantly

### **Section-Level Tabs (Optional)**
If dashboard gets too long, add collapsible tabs:
```
[Revenue] [Funnel] [Traffic Sources] [Product & Device] [Full View]
```

---

## **COLOR SCHEME & DESIGN**

### **Color Palette**
- **Brand Primary**: #1F77B4 (Blue) — Trust, professional
- **Revenue/Success**: #2CA02C (Green) — Positive metrics
- **Alert/Warning**: #FF7F0E (Orange) — Needs attention (low CVR, high abandon)
- **Neutral**: #808080 (Gray) — Supporting info
- **Accent**: #D62728 (Red) — Critical issues (>30% gap)

### **Typography**
- **Headline**: Large, bold (24-28pt), brand color
- **Section Headers**: Medium (16-18pt), bold, gray
- **Metric Labels**: Small (12pt), caps, gray
- **Numbers**: Large (32-48pt for scorecard), sans-serif, bold

### **Spacing & Layout**
- **Margins**: 20-30px between sections
- **Card padding**: 15px
- **Scorecard height**: Fixed 150px (consistent visual rhythm)
- **Visual grid**: 2-3 columns on desktop, 1 on mobile

---

## **INTERACTIVE BEHAVIORS**

### **Hover States**
- Hover over any bar/point in chart → Show exact value in tooltip
- Hover over scorecard → Highlight related chart (e.g., hover "Avg Order Value" → highlight trend line)

### **Drill-Down Capabilities**
- Click "Organic Search" in revenue bar chart → Funnel + device breakdown for organic only
- Click "Mobile" device card → Show all metrics filtered to mobile
- Click a month in a chart → Focus that month's data (option to compare)

### **Linked Insights**
- If checkout abandonment >50%, highlight in red with link: *"View mobile checkout audit"*
- If mobile gap >30%, link to device breakdown section
- If organic 2x paid revenue, suggest budget shift with interactive "What-if" slider

---

## **INFORMATION HIERARCHY**

### **What the CMO Sees First (Top Priority)**
1. **3 headline scorecards**: Total Revenue | AOV | CVR (full period)
2. **Revenue trend**: Bar chart showing Dec spike (holiday context)
3. **Funnel**: Biggest friction point identified visually

### **What They Explore Next (If Digging In)**
4. **Traffic source breakdown**: Revenue rank + CVR quality check
5. **Device/Mobile gap**: If gap is large, immediately actionable

### **Deep Dives (If Needed)**
6. **Product concentration**: Strategic risk assessment
7. **Seasonal patterns**: Nov vs Dec vs Jan trends
8. **Monthly comparisons**: How each channel/device shifts by month

---

## **RECOMMENDED TOOL: LOOKER STUDIO**

This dashboard works best in **Looker Studio** because:
- ✓ Free (part of Google Cloud free tier)
- ✓ Native BigQuery integration (no ETL needed)
- ✓ Filters cascade automatically
- ✓ Drill-down enabled natively
- ✓ Scorecards, bar charts, scatter plots all available
- ✓ Mobile-responsive automatically
- ✓ Shares as public link easily

---

## **IMPLEMENTATION CHECKLIST**

- [ ] Create 4 data sources in BigQuery (one per KPI group)
- [ ] Build scorecard + chart combos in Looker Studio for each section
- [ ] Set up filter connections (date, source, device cascade)
- [ ] Add drilldown filters to bar charts
- [ ] Apply color scheme consistently
- [ ] Test mobile responsiveness
- [ ] Add written descriptions under each section (layman's language for CMO)
- [ ] Create public shareable link
- [ ] Embed link in measurement framework PDF
