# Sample product decision note

## Observation

In the deterministic synthetic fixture, build 102 has higher Level 20 and D1
rates than build 101. The event-quality query reports unique IDs, UTC timestamps,
and no negative revenue rows.

## What is not proven

Build 102 is assigned to later install cohorts, not randomly assigned users.
The difference may reflect fixture construction, cohort timing, platform mix,
or the build. This repository does not claim causal uplift.

## Decision

Do not scale spend or declare a winner from this comparison. Preserve the
measurement contract, define a controlled exposure rule, pre-register the
primary metric and guardrails, and wait until both variants have mature cohorts.

## Next test

- Randomly assign eligible new users within the same date window.
- Use Level 20 completion as the primary progression metric.
- Use crash-free sessions and payer conversion as guardrails.
- Review data quality before reading the experiment result.
