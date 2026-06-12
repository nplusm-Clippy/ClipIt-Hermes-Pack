---
name: clipper-account-insights
description: Check ClipIt credits, estimate costs, and inspect analytics
version: 1.0.0
author: nplusm-Clippy
license: MIT
platforms: [macos, linux, windows]
metadata:
  tags: [ClipIt, Credits, Analytics, Cost Estimate, Reporting, Social Media]
  hermes:
    tags: [ClipIt, Credits, Analytics, Cost Estimate, Reporting, Social Media]
    requires_toolsets: [terminal]
required_environment_variables:
  - name: CLIPPER_API_KEY
    prompt: "Enter your ClipIt API key"
    help: "Get one at https://clipit.dev -> Settings -> API Keys -> Connect an Agent"
    required_for: "ClipIt API access"
---

# ClipIt Account Insights

## When to Use

Use this skill when the user wants to:
- Check their $CLIP credit balance
- Estimate the credit cost before paid operations
- Review aggregate social analytics
- Find top-performing clips or posts
- Inspect metrics for a specific social post

Estimate before expensive paid work: render/export, B-Roll generation, thumbnail generation, transcription, AI clip suggestions, and multi-platform social posting. Costs are reported in $CLIP.

## Quick Reference

| Operation | Script | Cost |
|-----------|--------|------|
| Check credits | `get_credits_balance.py` | Free |
| Estimate cost | `estimate_cost.py --operation-type <type> --provider <provider> key=value` | Free |
| Analytics overview | `get_analytics_overview.py [--days 30]` | Free |
| Analytics by platform | `get_analytics_overview.py --by-platform [--days 30]` | Free |
| Top clips | `get_top_clips.py [--metric views] [--limit 10]` | Free |
| Post metrics | `get_post_metrics.py --post-id <id>` | Free |

## Procedure

### Checking Credits

**When to use:** Before any operation that spends $CLIP or when the user asks about account balance.

**Steps:**
1. Run `python scripts/get_credits_balance.py`
2. Read `balanceClip`, `lifetimeDepositedClip`, and `lifetimeConsumedClip`
3. If balance is low, pause before starting paid work

**Example:**
```bash
python scripts/get_credits_balance.py
```

### Estimating Cost

**When to use:** Before render/export/B-Roll/thumbnail/social/transcription work when enough metrics are known.

**Steps:**
1. Choose the operation, provider, optional model, and numeric metrics
2. Run `estimate_cost.py` with metrics as `key=value` pairs
3. Continue only if `affordable` is true and no spend-limit violation is returned

**Examples:**
```bash
python scripts/estimate_cost.py \
  --operation-type transcription \
  --provider deepgram \
  --model-id nova-3 \
  videoSeconds=120

python scripts/estimate_cost.py \
  --operation-type lambda_render \
  --provider aws_lambda \
  --model-id remotion-4.0 \
  videoSeconds=45
```

### Reviewing Analytics

**When to use:** The user asks how their published content is performing.

**Steps:**
1. Run `python scripts/get_analytics_overview.py --days 30`
2. For platform breakdowns, add `--by-platform`
3. For top performers, run `python scripts/get_top_clips.py --metric views --limit 10`
4. For a specific post, run `python scripts/get_post_metrics.py --post-id <id>`

## Pitfalls

- **Use $CLIP fields.** The API also returns base units internally. These scripts print the `*Clip` values for user-facing cost decisions.
- **Estimates require the right metrics.** For render/export, use `videoSeconds`. Provider/model names must match what the metering service expects.
- **Analytics depends on published posts.** Empty analytics can simply mean no connected social metrics have been captured yet.
- **Spend limits can block an affordable balance.** If `spendLimitViolation` is present, do not start the paid operation with the same API key.

## Verification

- **Balance checked:** Response includes `balanceClip` and `units: "clip"`
- **Estimate succeeded:** Response includes `estimatedCostClip`, `affordable`, and `balanceClip`
- **Analytics loaded:** Overview contains totals such as `totalViews` or platform rows
- **Top clips loaded:** Response is an array of clips/posts with a selected metric value
