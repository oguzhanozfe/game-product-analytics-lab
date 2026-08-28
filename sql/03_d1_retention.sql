WITH installs AS (
    SELECT user_id, MIN(install_date_utc) AS install_date
    FROM events
    WHERE event_name = 'install'
    GROUP BY user_id
),
d1_users AS (
    SELECT DISTINCT e.user_id
    FROM events e
    JOIN installs i USING (user_id)
    WHERE e.event_name = 'session_start'
      AND CAST(julianday(substr(e.event_ts_utc, 1, 10)) - julianday(i.install_date) AS INTEGER) = 1
)
SELECT
    COUNT(*) AS installs,
    SUM(CASE WHEN d1.user_id IS NOT NULL THEN 1 ELSE 0 END) AS d1_returners,
    ROUND(100.0 * SUM(CASE WHEN d1.user_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS d1_pct
FROM installs i
LEFT JOIN d1_users d1 USING (user_id);
