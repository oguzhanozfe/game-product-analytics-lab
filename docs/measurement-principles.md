# Measurement principles

1. Validate identity, timestamps, duplicates, and event semantics before reading
   product outcomes.
2. Keep install-cohort dates and raw UTC timestamps explicit.
3. Do not convert an immature cohort into a zero-retention result.
4. Treat a build comparison as observational unless assignment and exposure are
   controlled.
5. Separate a metric movement from a causal claim and from a product decision.
6. Record the next test needed to reduce uncertainty.

The synthetic fixture deliberately assigns later cohorts to build 102. Its
higher metrics are therefore a correlation in a toy dataset, not proof that the
build caused the difference.
