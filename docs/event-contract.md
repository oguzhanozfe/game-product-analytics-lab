# Synthetic event contract

| Field | Type | Rule |
|---|---|---|
| `event_id` | string | Unique, deterministic fixture identifier |
| `user_id` | string | Synthetic only; must begin with `SYN-` |
| `event_name` | string | Controlled event vocabulary |
| `event_ts_utc` | ISO-8601 | UTC timestamp ending in `Z` |
| `install_date_utc` | date | UTC install cohort date |
| `build` | string | Synthetic release identifier |
| `platform` | string | `ios` or `android` in this fixture |
| `level` | integer/null | Present only for level-related events |
| `revenue_usd` | decimal | Zero except synthetic purchase events |

Event vocabulary: `install`, `level_start`, `tutorial_complete`,
`level_20_complete`, `session_start`, and `purchase`.

The dataset contains no production player, device, advertising, or purchase data.
