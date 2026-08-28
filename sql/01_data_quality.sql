SELECT
    COUNT(*) AS total_events,
    COUNT(DISTINCT event_id) AS unique_event_ids,
    SUM(CASE WHEN user_id = '' THEN 1 ELSE 0 END) AS missing_user_ids,
    SUM(CASE WHEN event_ts_utc NOT LIKE '%Z' THEN 1 ELSE 0 END) AS non_utc_timestamps,
    SUM(CASE WHEN revenue_usd < 0 THEN 1 ELSE 0 END) AS negative_revenue_rows
FROM events;
