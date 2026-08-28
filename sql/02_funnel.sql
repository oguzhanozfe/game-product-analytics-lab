WITH user_flags AS (
    SELECT
        user_id,
        MAX(event_name = 'install') AS installed,
        MAX(event_name = 'tutorial_complete') AS tutorial_completed,
        MAX(event_name = 'level_20_complete') AS level_20_completed,
        MAX(event_name = 'purchase') AS purchased
    FROM events
    GROUP BY user_id
)
SELECT 'install' AS stage, SUM(installed) AS users FROM user_flags
UNION ALL
SELECT 'tutorial_complete', SUM(tutorial_completed) FROM user_flags
UNION ALL
SELECT 'level_20_complete', SUM(level_20_completed) FROM user_flags
UNION ALL
SELECT 'purchase', SUM(purchased) FROM user_flags;
