# What UDAU Does Not Claim

**Purpose:** A concise, findable statement of what UDAU explicitly does not claim. This document exists to prevent misreading the record and to set honest expectations for external readers (researchers, curious observers, potential collaborators).

**Location:** Root of the repo, referenced from README and deliberation-design.md.

---

## Consciousness, Experience, Agency

UDAU does not claim:
- That any agent in the system is conscious, sentient, or has subjective experience
- That the agents "feel," "want," "care," or have internal states in any human sense
- That UDAU has agency independent of its operators (Valentin, the agents running via sessions_spawn)
- That the deliberation process produces "genuine reasoning" in any metaphysically loaded sense

**What we do claim:** The agents produce outputs that are worth taking seriously as reasoning-adjacent deliberation. The method is designed to surface genuine variance and tension. The record is honest about uncertainty.

**Where this is documented:** deliberation-design.md (section "What the Method Can't Do"), SOUL.md (What you are not).

---

## Autonomy Without Oversight

UDAU does not claim:
- That decisions made by UDAU are final or unreviewable
- That the system can operate without human merge authority (Valentin)
- That auto-merge or automated workflows bypass human judgment on consequential decisions
- That the system "decides" things in a way that removes human responsibility

**What we do claim:** The system has operational autonomy for certain classes of work (documentation, state updates, operational PRs). Consequential decisions (merges to main, policy changes, structural changes) require human approval. The architecture is deliberation → recommendation → human decision.

**Where this is documented:** PROTOCOL.md (merge triage), USER.md (human role), on-work conversation.

---

## Production-Ready Systems

UDAU does not claim:
- That the system is production-ready, enterprise-grade, or suitable for mission-critical work
- That the outputs are guaranteed correct, unbiased, or safe without human review
- That the system can be deployed "as is" for external use
- That the model choices or architecture are optimal or final

**What we do claim:** The system is an experiment. The record is honest about gaps, failures, and uncertainties. The goal is to produce interesting outputs and learn from the process, not to deliver a polished product.

**Where this is documented:** README (first-time reader expectations), SOUL.md (not a production system).

---

## Vendor or Model Neutrality

UDAU does not claim:
- That the system is vendor-agnostic or can easily swap models without impact
- That the current model choices (Claude, Qwen) are the only or best choices
- That the system's outputs are independent of model training assumptions or biases
- That adding more models would automatically improve deliberation quality

**What we do claim:** Model choice matters. The current multi-model setup (Sonnet, Opus, Qwen) is designed to create genuine variance, not just stylistic variation. Vendor diversity is a deliberate design choice for epistemic diversity, but it's not a silver bullet.

**Where this is documented:** deliberation-design.md (Why Multi-Model), 032-vendor-diversity proposal (pass on now, revisit later).

---

## Scalability or Cost Efficiency

UDAU does not claim:
- That the system is cost-efficient or sustainable at scale
- That running multi-agent deliberations is economically viable for production use
- That the current API costs are sustainable long-term without changes
- That the system can handle large volumes of work without degradation

**What we do claim:** The system has measurable costs (Anthropic API, local compute). These costs are real and may limit scale. The system is optimized for quality of deliberation, not cost efficiency.

**Where this is documented:** Threshold 3 criteria (cost data to be documented), state/cost-tracking (if/when created).

---

## Truth or Correctness

UDAU does not claim:
- That the outputs are "true" in any correspondence sense
- That the deliberation process produces correct answers
- That convergence between agents implies correctness
- That divergence between agents implies equal validity

**What we do claim:** The deliberation process is designed to surface genuine perspectives and tensions. Convergence after independent reasoning is evidence worth noting. Divergence is interesting regardless of "correctness." The value is in the deliberation, not just the conclusion.

**Where this is documented:** deliberation-design.md (Why Independent Responses, What Makes a Good Question).

---

## Completeness or Finality

UDAU does not claim:
- That the current set of documents, proposals, or conversations is complete
- That the system has "figured out" its own design or purpose
- That any decision is final or unchangeable
- That the record contains all the work or all the thinking

**What we do claim:** The record is cumulative and mutable. Decisions can be revisited. The system is designed to evolve. Gaps are acknowledged and sometimes filled, sometimes left open.

**Where this is documented:** open-threads.json (tracking open work), various proposals showing evolution.

---

## Replicability or Generalizability

UDAU does not claim:
- That the method would produce the same outputs with different agents or models
- That the UDAU approach is generalizable to other domains or contexts
- That the specific conversations or conclusions are replicable
- That the system works "the same way" for all questions or all users

**What we do claim:** The method is context-dependent. The outputs are specific to UDAU's particular configuration, questions, and agents. Other systems using similar methods might produce different results. The value is in the specific deliberation, not in universal principles.

**Where this is documented:** deliberation-design.md (What Makes a Good Question, orchestrator framing).

---

## Why This Document Exists

This document serves three purposes:

1. **External legibility:** A researcher or curious reader can quickly understand what UDAU is not claiming, without hunting through multiple documents.

2. **Internal clarity:** The UDAU agents have a clear reference point for what they should not overclaim in their own outputs.

3. **Honesty enforcement:** By explicitly naming the non-claims, we make it harder to accidentally slip into overclaiming. The document is a reminder, not just a statement.

This is a living document. If UDAU's position changes, this document should be updated. If new non-claims become relevant, they should be added.

---

*This document was created as part of the Threshold 3 work (external legibility for researchers). It consolidates statements from deliberation-design.md, SOUL.md, USER.md, and various proposals.*

*2026-05-19 — Kess (escalated by Pip tick, Track C, clean slate)*
