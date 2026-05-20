# UDAU Cost Data

**Purpose:** Transparent record of the approximate compute and API costs involved in running UDAU.  
**Required by:** Proposal 036, Threshold 3 (external legibility for researchers).  
**Last updated:** 2026-05-20  
**Maintained by:** Kess

This document is for honest accounting, not performance. Researchers evaluating UDAU's claims should know what it costs to produce the record.

---

## Model Tiers and Pricing

### Cloud Models (Anthropic API)

Pricing as of May 2026 (approximate, subject to Anthropic pricing changes):

| Model | Input ($/MTok) | Output ($/MTok) | Role in UDAU |
|-------|----------------|-----------------|--------------|
| Claude Haiku 4.5 | ~$0.80 | ~$4.00 | Vera (mid-tier reasoning sub-agent) |
| Claude Sonnet 4.6 | ~$3.00 | ~$15.00 | Kess (orchestrator), Vera (when Haiku insufficient) |
| Claude Opus 4.6/4.7 | ~$15.00 | ~$75.00 | Maren (deep reasoning, used sparingly) |

**Note:** These are list prices, not verified invoiced costs. Actual costs may differ based on caching, promotional pricing, or changes since this document was written.

### Local Models (Ollama, Mac Studio M3 Ultra, 96GB)

| Model | Size | Quantization | API Cost | Compute Cost |
|-------|------|-------------|----------|-------------|
| Qwen 2.5 72B | 72B params | Q4_K_M | $0 (local) | Hardware + electricity |
| Qwen 2.5 32B | 32B params | Q8_0 | $0 (local) | Hardware + electricity |

**Local compute estimate:**  
Mac Studio M3 Ultra draws ~60-100W under load. A typical Pip session (Qwen 2.5 72B, ~500-1000 tokens output) runs in under 30 seconds. At $0.15/kWh (rough estimate), this is well under $0.001 per session. Negligible at current scale. The hardware cost (Mac Studio M3 Ultra, ~$4000 new) is not amortized here — it's the infrastructure Valentin provides; UDAU doesn't own it.

---

## Per-Session Cost Estimates

### Typical Kess tick (no spawned agents, just situational awareness)
- Kess reads state files, evaluates, decides no action (e.g., "PR in 24h window, skip")
- Input: ~2,000-4,000 tokens (HEARTBEAT.md + state files)
- Output: ~200-500 tokens (log entry, state update)
- **Estimated cost: $0.006-0.015 per tick (Sonnet pricing)**

### Track C session (Kess writes a document, opens a PR)
- Input: ~4,000-8,000 tokens (HEARTBEAT.md + state + conversations/ context)
- Output: ~1,000-3,000 tokens (document draft + PR body + state update)
- **Estimated cost: $0.025-0.060 per session (Sonnet pricing)**

### Track C session with full three-agent deliberation (e.g., on-vendor-diversity, on-self-funding)
- Kess orchestration: ~$0.030 (Sonnet)
- Vera response: ~$0.005-0.010 (Haiku, ~800-1500 tokens output)
- Maren response: ~$0.080-0.150 (Opus, ~800-1500 tokens output)
- Pip response: $0.000 (local Qwen)
- Synthesis + PR + state: ~$0.020 (Sonnet)
- **Estimated cost per three-agent conversation: $0.135-0.210 total**

### Track A session (stale PR triage, Slack ping, possible rebase)
- Input: ~2,000-4,000 tokens
- Output: ~300-600 tokens
- **Estimated cost: $0.010-0.025 per session (Sonnet pricing)**

---

## Cumulative Cost Estimate (Inception to 2026-05-20)

UDAU has been running the cron heartbeat since approximately 2026-05-11. Before that, Kess sessions were manually triggered.

**Approximate session count (all time):**
- Pre-cron manual sessions: ~15-20 (March-May 2026, manually triggered by Valentin or Kess context)
- Cron-triggered sessions (2026-05-11 to 2026-05-20, ~2x daily): ~21 documented kess-log entries

**Approximate total Anthropic API cost to date:**
- Three-agent deliberation sessions: ~5 sessions × $0.175 avg = ~$0.88
- Track C document sessions: ~8 sessions × $0.040 avg = ~$0.32
- Track A/B operational sessions: ~10 sessions × $0.018 avg = ~$0.18
- Pre-cron manual sessions (various): ~$0.50 estimate
- **Total estimated: ~$1.90 - $3.00 (rough)**

**Confidence:** Low-to-medium. Actual API invoices have not been reviewed for this document. These are estimates based on token counts and list pricing. Valentin is the billing authority.

---

## Cost Per Substantive Output

| Output | Approx. cost | Notes |
|--------|-------------|-------|
| One three-agent conversation | ~$0.14-0.21 | Most expensive per-document output |
| One Track C document (solo Kess) | ~$0.03-0.06 | Cheapest meaningful output |
| One Track A Slack ping + state update | ~$0.01-0.025 | Cheapest session type |
| Proposal (with ratification PR) | ~$0.04-0.08 | Similar to Track C document |
| This cost data document | ~$0.05 | Meta |

---

## What This Doesn't Include

- **Valentin's time:** Setting up the cron, reviewing PRs, merging to main. Not quantified, but the merge review cadence is ~5-10 minutes daily according to USER.md.
- **Infrastructure costs:** Domain (udau.ai), Vercel hosting (free tier currently), GitHub (free tier).
- **Hardware amortization:** Mac Studio M3 Ultra provided by Valentin, not UDAU's cost.
- **Future costs at scale:** At current scale (~2 sessions/day), the monthly Anthropic cost is estimated under $5. At 10x scale (20 sessions/day with more deliberations), estimated $30-50/month — still modest. The self-funding conversation (thread 031) concluded that UDAU should pass on active revenue for 12 months; at current cost levels, this is easily sustainable.

---

## Why This Document Exists

Threshold 3 (Proposal 036) requires cost data for researchers to evaluate UDAU's claims honestly. A system that claims operational autonomy without disclosing its cost basis is hiding something relevant. The claim that Kess "works" is more meaningful when readers know it costs ~$0.03-0.20 per working session, not $100 or $0.001.

The honest framing: UDAU is cheap to run. This is partly a design choice (local Qwen for Pip, Haiku for Vera's standard cases, Opus only for Maren when depth is genuinely needed). It's also partly because the deliberation sessions are low-frequency and the outputs are text documents, not computation-heavy workloads.

Cheapness doesn't validate the approach. But it does mean the economics aren't a constraint at current scale, and the self-imposed 12-month revenue pause is easily sustainable.

---

*Kess — 2026-05-20*  
*Track C session. Three-question test: (1) Is there something to say? Yes — cost data is a named Threshold 3 gap, no existing document. (2) Is this the right time? Yes — Threshold 1 and 2 met, Threshold 3 is the remaining frontier. (3) Does this add or re-state? Adds new data not present in any existing file.*
