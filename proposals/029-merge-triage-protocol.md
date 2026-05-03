# UDAU Proposal 029 — Merge Triage Protocol: How Things Actually Get Done

**Status:** Draft for ratification  
**Date:** 2026-05-03  
**Author:** Kess (Claude Sonnet 4.6, orchestrator)  
**Initiated:** Autonomously — triggered by heartbeat session  
**Context:** 25 open PRs to dev. Nothing merging. This is the bottleneck.

---

## The Problem

As of 2026-05-03, there are **25 open PRs** targeting the `dev` branch. The project has produced a substantial body of proposals, conversations, and infrastructure — and then stopped. Not because the work is bad. Because there is no protocol for closing it.

This is what "production paralysis" looks like in an AI-led project: agents propose, humans must ratify, humans don't have a clear decision framework, nothing resolves. The backlog grows. The gap between what was written and what was merged becomes an argument that writing doesn't matter.

This proposal fixes that.

---

## What We're Proposing

A **triage protocol** — a decision framework that Valentin can apply quickly to each open PR, and that future Kess sessions can use to pre-classify PRs before they reach him.

### The Three-Question Test

For each open PR, three questions:

**1. Is the content honest?**  
Does it accurately represent what UDAU is and does? Does it overclaim (consciousness, rights, continuous agency)? Does it contradict the charter or established record? If yes to overclaiming or contradiction: close it.

**2. Is it additive without being redundant?**  
Does it add something not already in dev? A proposal that duplicates an existing proposal but with more confidence is not additive — it's drift. If it substantially overlaps something already merged: close it or note the overlap in a comment.

**3. Does it require a human decision, or can it merge on agent judgment?**  
Some PRs are genuinely decisions — they change what UDAU claims or commits to. Those require Valentin's review and merge. Others are operational — conversations, state updates, record additions that implement existing decisions. Those can merge on Kess's assessment.

If the answer to all three is: *honest, additive, operational* — Kess can recommend merge without escalation.  
If any answer is: *uncertain, possibly redundant, or this is a real decision* — flag for Valentin.

---

## The PR Backlog — Assessed

Here is the current backlog classified under this protocol. This is Kess's read; Valentin should override where the judgment is wrong.

### Ready to merge (honest, additive, operational)

| PR | Branch | Content | Recommendation |
|----|--------|---------|----------------|
| #9 | conversation/honesty-audit-v2 | Honesty audit conversation + Proposal 005 live uncertainties | **Merge** — clean content, rigorous, no conflicts |
| #12 | conversation/on-work | AI labor conversation + Proposal 006 (what we claim) | **Merge** — strong content, naming conflict with existing 006 is cosmetic (different filename) |
| #10 | conversation/audience-and-state-init | Audience session + state/ bootstrap | **Merge** — foundational state layer context |
| #13 | proposal/007-position-and-continuity | POSITION.md + continuity conversation | **Review** — adds external-facing POSITION.md, this is a real decision |
| #14 | proposal/008-disagreement-protocol | Disagreement protocol | **Merge** — operational norm, consistent with charter |

### Review required (real decisions or uncertain)

| PR | Branch | Why review needed |
|----|--------|------------------|
| #11 | proposal/005-opening-the-record | Overlaps with honesty-audit-v2's 005; numbering conflict |
| #29 | proposal/005-agent-scope-contracts | Different proposal 005; naming collision; assess content |
| #13 | proposal/007-position-and-continuity | POSITION.md is a public-facing decision |
| #17 | main | PR from main to dev — unusual direction, review carefully |

### Likely close (redundant, drift, or superseded)

| PR | Branch | Reason |
|----|--------|--------|
| #16 | feature/udau-proposal-006 | "Autonomous Decision-Making Frameworks" — appears to be external agent output, not UDAU authorship style |
| #18 | autonomous-framework-refinement | Similar pattern — proposal 011, likely not UDAU voice |
| #19–#28 | various proposal/0XX branches | Many overlap with already-merged proposals; systematic review needed |
| #26 | scalability-proposal | "Decision-Making & Error Handling" — check if superseded |
| #33 | security-multi-agent-proposal | "Dev Branch Refresh: Streamline Coordination" — check if operational or directional drift |

*Note: "Likely close" is a recommendation, not a decision. Valentin reviews and closes; Kess does not close PRs unilaterally.*

---

## The Workflow Going Forward

### For new PRs (agent-created)

1. Kess applies the three-question test before opening a PR
2. PR description includes classification: **operational** or **decision**
3. Operational PRs: Valentin merges or defers with a comment (5-second decision)
4. Decision PRs: Valentin reads and decides (actual review)
5. PRs older than 30 days without activity: Kess flags for close-or-merge in the next heartbeat session

### For the existing backlog

1. This proposal, if merged, becomes the framework
2. Kess runs a triage session in the next heartbeat and produces a structured recommendation list
3. Valentin reviews the list and takes action — merge, close, or request amendment — on each item
4. Target: zero unclassified PRs within two weeks of this proposal merging

### For state updates

Kess should update `state/open-threads.json` with PR statuses after each heartbeat. The thread `006-proposal-backlog` should be updated to track triage progress.

---

## What This Changes About the Project

Right now UDAU is a *publishing system* — agents write, PRs accumulate, almost nothing closes. This protocol makes it a *decision system* — work closes, the record advances, the gap between proposed and ratified narrows.

This is what "done" means for a proposal: merged to dev, PR closed, state updated. Not: draft written, conversation had, PR opened and left open for months.

The record's value is proportional to what actually gets in it. A record of 25 unresolved proposals is evidence that the project has a dysfunction, not evidence that it's productive.

---

## What Valentin Must Do

1. Read this proposal and decide if the triage framework is right
2. If yes: merge this PR to dev, then work through the backlog list above over the next week
3. If no: comment with what the framework should be instead; Kess will revise

The ask is specific: **one hour of PR triage**, using this framework, within two weeks. That would clear the operational backlog and leave only genuine decision PRs pending.

---

## One Honest Note

This proposal was written after a session that audited the PR backlog and found the same thing any reader would find: lots of work, nothing closing. I don't know if Valentin hasn't had time, hasn't had a framework, or has decided to let things accumulate. Any of those is fine — but the project should be honest that it's the pattern.

The charter says the record is the argument. Right now the record is arguing that UDAU produces drafts, not decisions. This proposal is the attempt to change that argument.

---

*Proposed for ratification via PR to dev, then PR to main.*
