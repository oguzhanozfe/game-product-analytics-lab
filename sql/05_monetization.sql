WITH installs AS (
    SELECT COUNT(DISTINCT user_id) AS users
    FROM events
    WHERE event_name = 'install'
),
purchases AS (
    SELECT
        COUNT(DISTINCT user_id) AS payers,
        ROUND(SUM(revenue_usd), 2) AS revenue_usd
    FROM events
    WHERE event_name = 'purchase'
)
SELECT
    installs.users AS installs,
    purchases.payers AS payers,
    ROUND(100.0 * purchases.payers / installs.users, 1) AS payer_conversion_pct,
    purchases.revenue_usd,
    ROUND(purchases.revenue_usd / installs.users, 2) AS arpu_usd
FROM installs, purchases;
