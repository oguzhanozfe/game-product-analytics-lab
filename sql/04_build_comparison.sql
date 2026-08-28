WITH user_flags AS (
    SELECT
        user_id,
        MIN(build) AS build,
        MAX(event_name = 'install') AS installed,
        MAX(event_name = 'tutorial_complete') AS tutorial_completed,
        MAX(event_name = 'level_20_complete') AS level_20_completed,
        MAX(
            event_name = 'session_start'
            AND CAST(julianday(substr(event_ts_utc, 1, 10)) - julianday(install_date_utc) AS INTEGER) = 1
        ) AS d1_returned
    FROM events
    GROUP BY user_id
)
SELECT
    build,
    SUM(installed) AS installs,
    ROUND(100.0 * SUM(tutorial_completed) / SUM(installed), 1) AS tutorial_pct,
    ROUND(100.0 * SUM(level_20_completed) / SUM(installed), 1) AS level_20_pct,
    ROUND(100.0 * SUM(d1_returned) / SUM(installed), 1) AS d1_pct
FROM user_flags
GROUP BY build
ORDER BY build;
