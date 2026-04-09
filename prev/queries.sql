-- ============================================================
-- Assignment 1 — GA4 BigQuery Starter Queries
-- Dataset: bigquery-public-data.ga4_obfuscated_sample_ecommerce
-- Date range: 2020-11-01 to 2021-01-31
-- ============================================================


-- ============================================================
-- SECTION 1: GENERAL WEBSITE PERFORMANCE
-- ============================================================

-- 1A. Daily Sessions, Users & Pageviews
--     Use case: Trend line / time series chart showing overall traffic over time
SELECT
  event_date,
  COUNT(DISTINCT user_pseudo_id)                                      AS users,
  COUNT(DISTINCT CONCAT(user_pseudo_id, (
    SELECT value.int_value
    FROM UNNEST(event_params)
    WHERE key = 'ga_session_id'
  )))                                                                  AS sessions,
  COUNTIF(event_name = 'page_view')                                   AS pageviews
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
GROUP BY event_date
ORDER BY event_date;


-- 1B. Bounce Rate by Day
--     A "bounce" = session with only 1 page_view and no engagement
--     Use case: Scorecard or line chart
WITH session_stats AS (
  SELECT
    event_date,
    CONCAT(user_pseudo_id, (
      SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id'
    )) AS session_id,
    COUNTIF(event_name = 'page_view')    AS pageviews,
    COUNTIF(event_name = 'user_engagement') AS engagements
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  GROUP BY event_date, session_id
)
SELECT
  event_date,
  COUNT(session_id)                                             AS total_sessions,
  COUNTIF(pageviews = 1 AND engagements = 0)                   AS bounced_sessions,
  ROUND(COUNTIF(pageviews = 1 AND engagements = 0) * 100.0 / COUNT(session_id), 2) AS bounce_rate_pct
FROM session_stats
GROUP BY event_date
ORDER BY event_date;


-- 1C. Device Category Breakdown
--     Use case: Pie or donut chart (desktop / mobile / tablet)
SELECT
  device.category                        AS device_category,
  COUNT(DISTINCT user_pseudo_id)         AS users,
  COUNT(DISTINCT CONCAT(user_pseudo_id, (
    SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id'
  )))                                    AS sessions
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
GROUP BY device_category
ORDER BY sessions DESC;


-- 1D. Top Countries by Users
--     Use case: Geo map or bar chart
SELECT
  geo.country                            AS country,
  COUNT(DISTINCT user_pseudo_id)         AS users,
  COUNT(DISTINCT CONCAT(user_pseudo_id, (
    SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id'
  )))                                    AS sessions
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
GROUP BY country
ORDER BY users DESC
LIMIT 20;


-- ============================================================
-- SECTION 2: SALES TRENDS
-- ============================================================

-- 2A. Daily Revenue, Transactions & Average Order Value
--     Use case: Dual-axis line chart (revenue + AOV over time)
SELECT
  event_date,
  COUNT(DISTINCT ecommerce.transaction_id)          AS transactions,
  ROUND(SUM(ecommerce.purchase_revenue_in_usd), 2)  AS revenue_usd,
  ROUND(
    SUM(ecommerce.purchase_revenue_in_usd) /
    NULLIF(COUNT(DISTINCT ecommerce.transaction_id), 0)
  , 2)                                              AS avg_order_value_usd
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE event_name = 'purchase'
GROUP BY event_date
ORDER BY event_date;


-- 2B. E-commerce Conversion Funnel
--     Use case: Funnel chart showing drop-off at each stage
SELECT
  'view_item'       AS funnel_step, 1 AS step_order, COUNT(DISTINCT user_pseudo_id) AS users FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE event_name = 'view_item'
UNION ALL
SELECT 'add_to_cart',     2, COUNT(DISTINCT user_pseudo_id) FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE event_name = 'add_to_cart'
UNION ALL
SELECT 'begin_checkout',  3, COUNT(DISTINCT user_pseudo_id) FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE event_name = 'begin_checkout'
UNION ALL
SELECT 'add_payment_info',4, COUNT(DISTINCT user_pseudo_id) FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE event_name = 'add_payment_info'
UNION ALL
SELECT 'purchase',        5, COUNT(DISTINCT user_pseudo_id) FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE event_name = 'purchase'
ORDER BY step_order;


-- 2C. Top Selling Products by Revenue
--     Use case: Horizontal bar chart
SELECT
  items.item_name,
  items.item_category,
  SUM(items.quantity)                               AS units_sold,
  ROUND(SUM(items.item_revenue_in_usd), 2)          AS revenue_usd
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`,
  UNNEST(items) AS items
WHERE event_name = 'purchase'
GROUP BY items.item_name, items.item_category
ORDER BY revenue_usd DESC
LIMIT 20;


-- 2D. Revenue by Product Category
--     Use case: Bar or treemap chart
SELECT
  items.item_category                               AS category,
  SUM(items.quantity)                               AS units_sold,
  ROUND(SUM(items.item_revenue_in_usd), 2)          AS revenue_usd
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`,
  UNNEST(items) AS items
WHERE event_name = 'purchase'
GROUP BY category
ORDER BY revenue_usd DESC;


-- ============================================================
-- SECTION 3: TRAFFIC SOURCES
-- ============================================================

-- 3A. Sessions & Revenue by Traffic Source / Medium
--     Use case: Bar chart or table — which channels drive the most traffic AND revenue
SELECT
  traffic_source.source                             AS source,
  traffic_source.medium                             AS medium,
  COUNT(DISTINCT user_pseudo_id)                    AS users,
  COUNT(DISTINCT CONCAT(user_pseudo_id, (
    SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id'
  )))                                               AS sessions
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
GROUP BY source, medium
ORDER BY sessions DESC
LIMIT 20;


-- 3B. Conversion Rate by Traffic Source
--     Use case: Bar chart — which sources convert best
WITH sessions AS (
  SELECT
    traffic_source.source                           AS source,
    traffic_source.medium                           AS medium,
    CONCAT(user_pseudo_id, (
      SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id'
    ))                                              AS session_id
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
),
purchases AS (
  SELECT
    traffic_source.source                           AS source,
    traffic_source.medium                           AS medium,
    COUNT(DISTINCT ecommerce.transaction_id)        AS transactions,
    ROUND(SUM(ecommerce.purchase_revenue_in_usd),2) AS revenue_usd
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  WHERE event_name = 'purchase'
  GROUP BY source, medium
)
SELECT
  s.source,
  s.medium,
  COUNT(DISTINCT s.session_id)                      AS sessions,
  COALESCE(p.transactions, 0)                       AS transactions,
  COALESCE(p.revenue_usd, 0)                        AS revenue_usd,
  ROUND(COALESCE(p.transactions, 0) * 100.0 / NULLIF(COUNT(DISTINCT s.session_id), 0), 2) AS conversion_rate_pct
FROM sessions s
LEFT JOIN purchases p ON s.source = p.source AND s.medium = p.medium
GROUP BY s.source, s.medium, p.transactions, p.revenue_usd
ORDER BY sessions DESC
LIMIT 20;


-- 3C. New vs Returning Users by Source
--     Use case: Stacked bar chart
SELECT
  traffic_source.source                             AS source,
  traffic_source.medium                             AS medium,
  COUNTIF(event_name = 'first_visit')               AS new_users,
  COUNT(DISTINCT user_pseudo_id) - COUNTIF(event_name = 'first_visit') AS returning_users
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
GROUP BY source, medium
ORDER BY new_users DESC
LIMIT 15;
