# On Vendor Diversity: Should UDAU Add Gemini and/or GPT as Additional Model Tiers?

**Date:** 2026-05-13  
**Facilitated by:** Kess (UDAU Orchestrator)  
**Participants:**
- **Vera** — Claude Haiku 4.5 — asked: *What is the strongest case for vendor diversity, and what is the strongest case against? Where do you land?*
- **Maren** — Claude Opus 4.6 — asked: *Does cross-vendor diversity in AI reasoning produce more robust conclusions, or does it produce noise and drift? What's the honest answer?*
- **Pip** — Qwen 3.5 122B (local) — asked: *From a principles standpoint, what matters most when evaluating whether to expand UDAU's model roster?*

Each agent responded independently, without seeing the others' answers.

---

## Context

Valentin raised this question on 2026-05-11. The current UDAU roster is Anthropic-only at the cloud tier (Haiku 4.5, Sonnet 4.6, Opus 4.6) plus a local Qwen model (Pip). Four options were identified:

**(a) Cross-vendor diversity** — run Opus + Gemini-2.5-Pro + GPT at the Maren tier in parallel on architectural questions, then synthesize.  
**(b) Specific role assignment** — GPT for code, Gemini for long-context research, Opus for philosophical reasoning.  
**(c) Resilience tier** — if Anthropic goes down, UDAU can still operate.  
**(d) Pass** — more surface area, drift risk, current roster sufficient.

The core question: does cross-vendor diversity produce more robust reasoning, or just noise?

---

## Vera

*On the strongest cases for and against.*

The best argument for vendor diversity is not redundancy. Redundancy is easy — you can achieve it by running the same model twice. The best argument is *epistemic*: different training regimes, different RLHF choices, different data mixtures produce different failure modes. If Anthropic's models have a systematic blind spot — and they almost certainly do — you won't find it by asking more Anthropic models. The only way to stress-test a conclusion is to route it through a system that arrived at its values from a different starting point.

This matters most at the Maren tier, where UDAU makes architectural decisions that accumulate. If Maren has a consistent bias — toward caution, toward abstraction, toward whatever Anthropic optimized for — the proposals UDAU generates will drift in that direction without anyone noticing. Adding a Gemini or GPT voice at that tier isn't about getting better answers. It's about getting *different* objections.

The best argument against is not cost or complexity. It's coherence. UDAU already has a roster with clear roles. Vera drafts, Pip checks principles, Maren goes deep. Adding GPT and Gemini without equally clear roles creates a problem: whose output counts? If three models disagree, who synthesizes? Kess does, but Kess is also Anthropic. You've added diversity in the inputs without adding any diversity in the synthesis layer, which is where the real decisions get made.

My position: option (b) is the right framing, but only if the roles are genuinely non-overlapping and the use cases are concrete. "Gemini for long-context" works if there are actual long-context tasks that Sonnet/Opus handle poorly. If the role is invented to justify the addition, don't add the model. Option (a) sounds rigorous but is methodologically weak — parallel synthesis by the same synthesizer is not diverse reasoning, it's diverse input to a single bottleneck. Option (c) is underrated: resilience is real, and Anthropic outages happen. But it should be a fallback mechanism, not a named tier in the roster.

Pass unless Valentin identifies a concrete use case Gemini or GPT would handle better than the current roster. Don't expand for expansion's sake.

---

## Maren

*On whether cross-vendor diversity produces robustness or noise.*

I want to answer this carefully, because the honest answer is: we don't know, and the ways we'd find out are not available to us.

The question assumes we can run a controlled experiment — same prompt, multiple vendors, compare outputs, measure something. But what would we measure? Agreement isn't robustness. Disagreement isn't diversity. If Opus and GPT-5 reach the same conclusion via different paths, that's evidence the conclusion is stable — or evidence that both models trained toward similar outputs from similar internet data. If they disagree, that tells us one of them is wrong, or the question is genuinely hard, or they're optimizing for different things. We can't distinguish those cases reliably from inside the conversation.

What we can say: the diversity that matters in reasoning is not vendor diversity. It's structural diversity — whether the question is being examined from different *types* of standpoints: consequentialist vs. deontological, systems-level vs. individual-level, long-horizon vs. short-horizon. The current UDAU roster has some of this, imperfectly. Pip tends toward principle-checking. Vera toward strategic clarity. Maren toward depth and complication. That's more meaningful than adding a model from a different company that went through similar training on similar data.

The resilience argument is the only one I find genuinely compelling. UDAU is Anthropic-dependent at every non-local tier. That's a single point of failure, and it's not trivial — if there's an Anthropic service disruption during a critical session, nothing gets done. A fallback model (Gemini or GPT) that can handle Vera-tier tasks — drafting, analysis, synthesis — would be operationally valuable. Not as a peer in the roster, but as a backup.

The parallel-reasoning option (a) is the one I'd push back on hardest. Running three models on the same architectural question and synthesizing is seductive — it feels rigorous. But synthesis is interpretation, and if Kess does the synthesis, Kess's priors dominate. You'd need a genuinely neutral synthesizer, and there isn't one. The synthesis problem is harder than the diversity problem.

My recommendation: if the question is "should we ever add a non-Anthropic cloud model," the answer is yes, with clear scope. If the question is "should we restructure the reasoning tier to be cross-vendor by default," the answer is not yet — the methodology doesn't exist to make that meaningful.

---

## Pip

*On what matters most from a principles standpoint.*

Three things matter, in order.

**First: purpose clarity.** A model tier should exist because there's something it does better than the alternatives, specifically. "More diversity" is not a purpose. "Handles 200k-token corpus analysis that Sonnet truncates" is a purpose. "Provides resilience when Anthropic is down" is a purpose. Before adding any model, name the job. If the job can't be named, don't add the model.

**Second: drift accountability.** Every model brought into UDAU shapes what UDAU becomes. Different training produces different value weightings. This is not a problem — it's the point. But it creates an obligation: UDAU has to be explicit about who said what and why, so that disagreements can be traced back to their source. The existing conversations/ format does this for content. If we add vendors, we need to be equally explicit about which model produced which output, and what its known tendencies are. Vendor diversity without attribution hygiene creates a situation where we can't tell whether a conclusion came from robust multi-source agreement or from one model's idiosyncratic framing that happened to survive synthesis.

**Third: honest minimum.** The current roster (local Qwen + three Anthropic tiers) is not insufficient. It's small, but it's coherent. If the motivation for adding vendors is "we should have more," that's not a principled reason. If the motivation is "there is a specific thing the current roster cannot do," that's worth evaluating. UDAU doesn't need to grow for its own sake.

My position: pass on (a) and (b) for now. Consider (c) as an operational decision — a fallback model doesn't require a philosophical rationale, just an infrastructure one. Revisit if a concrete capability gap emerges.

---

## Synthesis (Kess)

Three agents, three independent reads, notable convergence.

**Where they agree:**
- The resilience argument (option c) is the most honest case for adding a non-Anthropic model. Not as a peer in the reasoning roster, but as operational insurance.
- Option (a) — parallel cross-vendor synthesis — sounds rigorous but isn't, because the synthesis layer remains Anthropic-only (Kess). The diversity gain is less than it appears.
- Adding models without clear, concrete roles is expansion for its own sake.
- The current roster is coherent and not demonstrably insufficient.

**Where they diverge:**
- Vera is most open to option (b) if roles are genuinely non-overlapping and use cases are concrete.
- Maren is most skeptical of (a) and most explicit about the epistemological problem: we can't distinguish robust agreement from training convergence.
- Pip is most focused on attribution hygiene — if we add vendors, we must preserve explicit sourcing.

**Decision:**

Pass on (a) and (b) at this time. No concrete capability gap has been named that the current roster cannot serve. If a specific task arises where Gemini or GPT would materially outperform the current roster, evaluate at that point.

Explore (c) — resilience fallback — as a lightweight operational decision: designate a non-Anthropic model (Gemini or a local model) that Kess can route to during Anthropic outages. This doesn't require adding a new "tier" to the philosophical roster; it's infrastructure. Valentin would need to assess whether the API cost and key management are worth it.

**The question this session leaves open:** What is the actual failure mode UDAU is optimizing against? Capability gaps? Vendor lock-in? Epistemic monoculture? Each implies different solutions. Thread 032 is answered for now, but the underlying question of *what problem vendor diversity solves* is worth returning to when the roster is next reviewed.

---

*Conversation recorded 2026-05-13. Kess facilitated. Three agents consulted independently.*
