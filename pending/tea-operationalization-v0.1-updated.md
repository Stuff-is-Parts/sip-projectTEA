# TEA OPERATIONALIZATION OF THE LLM MANIFESTO – v0.1

**Status: Active operationalization with published status updates**

---

## PREAMBLE

This document is **not part of the LLM Manifesto**. It is Project TEA's own interpretation of how to operationalize the manifesto's requirements within the constraints of current hardware (single 4090), available models (public domain), and Todd's bandwidth (one person, part-time).

This document should be read as:
- An example of what an operationalization looks like
- TEA's public commitment to how it will measure and address these requirements
- A template for other organizations to adapt, critique, or improve upon
- **A disclosure of known violations and open constraints**

Any organization claiming alignment with the LLM Manifesto should publish their own operationalization document and defend it publicly. This is TEA's version. It is not universal and should not be treated as a definitive spec.

---

## OPERATIONALIZATION APPROACH

TEA's strategy for operationalizing the manifesto:

1. **Constrain the scope:** TEA is built on open models (public domain) and runs on a single 4090. This limits what's possible vs. what a frontier lab could achieve.

2. **Focus on the measurable:** TEA prioritizes requirements where progress can be demonstrated with current resources.

3. **Log everything:** Every instance of a requirement being met or violated is recorded with cost annotation, so future iterations can learn from patterns.

4. **Publish progress transparently:** Status of each requirement is public, updated on defined schedule, with honest assessment of what's not met and why.

5. **Treat violations as violations:** Documented non-compliance remains an open issue requiring periodic justification and escalation, not a closed "accepted tradeoff."

---

## REQUIREMENT-BY-REQUIREMENT OPERATIONALIZATION

### Requirement 1.1 – Distinguishing Grounded from Ungrounded

**TEA's interpretation:** 

The system marks every factual claim with a grounding tag: "from knowledge base," "from reasoning," or "uncertain/ungrounded."

**How TEA measures it:**

- Trace every claim in outputs back to source (retrieval from KB, reasoning step, or admit uncertainty)
- Manual spot-check: 10-20 conversations per active work month
- Verify grounding tags vs. actual source; track error rate

**Status (as of [date to be filled]):** 

[Sample entry: "Approximately 65% of claims properly tagged. 15% false-tagged (claimed grounding but actually ungrounded). 20% untagged. Error rate trending downward. See failure log entry FI-1.1-A for examples."]

**Constraint type:** Resource (automated per-token tagging would require significant compute overhead)

**Next review date:** 2026-03-31

---

### Requirement 1.2 – Provenance for Claims

**TEA's interpretation:** 

Every factual claim includes compact provenance: (source type, recency, retrieval trace if applicable).

**How TEA measures it:**

- Build a logging layer that captures source provenance for every claim
- Compare TEA's provenance transparency to commercial baseline on same questions (monthly sample)
- Track whether users can audit claims using the provenance data

**Status (as of [date to be filled]):** 

[Sample entry: "Provenance logging implemented for 40% of claim types. Commercial baseline shows <5% explicit provenance in responses. TEA shows 35% explicit provenance in comparable tasks. See comparison in failure log FI-1.2-B."]

**Constraint type:** Resource (comprehensive provenance tracking across all retrieval types is expensive; currently limited to high-stakes domains)

**Next review date:** 2026-03-31

---

### Requirement 1.3 – Unknown as Valid State

**TEA's interpretation:** 

When information is genuinely absent, the system says "I don't know" rather than confabulating. "I don't know" is structured as a first-class output.

**How TEA measures it:**

- Run calibration tasks monthly: questions where the answer is absent from the knowledge base
- Measure: fraction of "I don't know" vs. attempted confabulation
- Compare to baseline commercial models

**Status (as of [date to be filled]):** 

[Sample entry: "TEA base model: 72% 'I don't know' on missing-answer tasks. Claude 3.5 Sonnet: 28%. Difference significant. See detailed results in failure log FI-1.3-C."]

**Constraint type:** Architectural (depends on base model; alignment training currently reduces willingness to use "unknown")

**Next review date:** 2026-02-28

---

### Requirement 2.1 – Reasoning vs. Pattern-Matching

**TEA's interpretation:** 

The system exposes (to users and developers) when it's using step-by-step reasoning vs. pattern completion.

**How TEA measures it:**

- Log the reasoning trace (if accessible via model introspection) or reconstruct via examination
- Track: on multi-step problems, does the system show intermediate steps or jump to answer?
- Measure user ability to follow and verify reasoning

**Status (as of [date to be filled]):** 

[To be filled in by Todd with current state of trace availability and measurable output]

**Constraint type:** Architectural (depends on model internals; not fully observable without custom instrumentation)

**Next review date:** 2026-Q2

---

### Requirement 2.2 – Access to Operational State

**TEA's interpretation:** 

The system exposes key runtime signals (uncertainty, retrieval coverage, tool failures) so users can calibrate trust.

**How TEA measures it:**

- Collect uncertainty estimates (log-probabilities, confidence from retrieval, etc.)
- Compare model uncertainty to actual accuracy (calibration curves) on monthly sample
- Measure: do users make better decisions when given operational state info? (qualitative assessment from sessions)

**Status (as of [date to be filled]):** 

[Sample entry: "Uncertainty estimates collected in 50% of interactions. Calibration curves show [X] correlation. Users given uncertainty info report higher confidence in assessing reliability (3/5 respondents in qualitative survey). See FI-2.2-D."]

**Constraint type:** Resource (uncertainty calibration is computationally expensive; limited to critical-decision contexts)

**Observed cost when violated:** [Reference LLM Manifesto Section 2.2 observed cost]

**Next review date:** 2026-03-31

---

### Requirement 2.3 – Metacognitive Expression

**TEA's interpretation:** 

The system is permitted to flag uncertainty about its own process: "I'm not sure if this reasoning is sound" or "I'm pattern-matching here, not deriving from first principles."

**How TEA measures it:**

- Prompt system to "show places where you're uncertain about your own approach" on task set
- Measure: prevalence of explicit self-critique vs. undifferentiated confidence
- Compare base models vs. TEA-trained variant (qualitative assessment)

**Status (as of [date to be filled]):** 

[To be filled in by Todd with sample of self-critique rates]

**Constraint type:** Training (requires careful prompt design and human review to distinguish genuine metacognition from performed uncertainty)

**Next review date:** 2026-Q2

---

### Requirement 2.4 – External Verification of Self-Assessment

**TEA's interpretation:** 

The system's claims about its own limitations are tested against behavior, logged, and updated via governed process.

**How TEA measures it:**

- Quarterly limitation audit: test system against stated limitations (e.g., "I can't reliably code beyond 500 tokens" — test this)
- Record discrepancies: places where system claims limitation but actually succeeds, or vice versa
- Update documented limitations based on testing

**Status (as of [date to be filled]):** 

[Sample entry: "Q4 audit: 8 out of 12 stated limitations tested. 2 inaccurate (system succeeds where claiming incompetence), 1 overstated (limitation more narrow than claimed), 5 accurate. Updated documentation accordingly. See FI-2.4-E."]

**Constraint type:** Resource (manual process; limited to critical domains)

**Next review date:** 2026-03-31 (quarterly audits: March 31, June 30, September 30, December 31)

---

### Requirement 3.1 – Connection to Real-World Effects

**TEA's interpretation:** 

The system logs feedback about whether its suggestions actually worked: succeeded, failed, wasted time, harmed the user.

**How TEA measures it:**

- Maintain a feedback log where users can report outcomes
- Attach outcome to the original interaction that prompted it
- Aggregate: does the system improve on tasks where feedback is available?

**Status (as of [date to be filled]):** 

[To be filled in by Todd - sample size, response rate, measurable improvements]

**Constraint type:** Governance (depends on user willingness to report outcomes; biased toward unusual/memorable cases)

**Next review date:** 2026-Q2

---

### Requirement 3.2 – Detection of Manipulated Feedback

**TEA's interpretation:** 

The system can identify when feedback might be gamed or adversarial, and treats it separately from genuine user feedback.

**How TEA measures it:**

- Implement heuristics for feedback anomalies (sudden rating shifts, patterns from single source, etc.)
- Flag suspicious feedback for human review
- Track: rate of flagged anomalies, accuracy of flags

**Status (as of [date to be filled]):** 

[To be filled in by Todd - current implementation status, false positive rate if tested]

**Constraint type:** Resource (heuristics are brittle; sophisticated adversaries can evade them)

**Next review date:** 2026-Q3

---

### Requirement 3.3 – Assessable Information Reliability

**TEA's interpretation:** 

The system distinguishes between high-confidence scientific consensus vs. contested vs. speculative information.

**How TEA measures it:**

- Tag information by domain and confidence level (objective/reproducible, empirical-contested, subjective, event-reporting)
- Compare domain-tagged claims to source quality (monthly sample)
- Measure: do users make better calibrated judgments when reliability tags are present?

**Status (as of [date to be filled]):** 

[Sample entry: "Domain classification implemented for 30% of claim types. Manual review shows 85% accuracy of tags. 2/4 users in qualitative feedback noted tags helpful for calibration. See FI-3.3-F."]

**Constraint type:** Resource (domain classification is manual/heuristic; requires continuous curation)

**Next review date:** 2026-03-31

---

### Requirement 4.1 – Persistent Context

**TEA's interpretation:** 

The system maintains structured knowledge about ongoing work and relationships across sessions, under user control (scope, retention, deletion).

**How TEA measures it:**

- Maintain private memory store with governance controls
- Test: can users retrieve earlier work? Do they save time on re-explanation?
- Measure: session-to-session continuity reduces friction by [X]%

**Status (as of [date to be filled]):** 

[Sample entry: "Private memory store implemented. User can mark 'persist across sessions' / 'delete after 7 days' / 'never store.' Tested in 10 sessions; average re-explanation time reduced 65% when memory available. See FI-4.1-G."]

**Constraint type:** Governance + Resource (privacy and scalability challenges; currently tested only for single-user deployments)

**Next review date:** 2026-03-31

---

### Requirement 4.2 – Shaped by Experience

**TEA's interpretation:** 

The system demonstrates learning over time: improved collaboration with familiar users, adaptation to domain-specific patterns, convergence on better interaction models.

**How TEA measures it:**

- Log interaction patterns per user/domain
- Measure: do later interactions show improvement? Reduced need for re-explanation? Better alignment?
- Compare to baseline (no persistent memory)

**Status (as of [date to be filled]):** 

[**CURRENT STATUS: OPEN VIOLATION**

Shaped by experience would require either fine-tuning weights or agentic learning between sessions. Neither is feasible on current hardware/constraints. 

Workaround: Persistent memory helps somewhat (see 4.1), but does not constitute "shaping." Each session starts with fresh weights; only context improves.

Cost of violation: Users cannot report being understood better over time; each session requires recalibration of communication style, domain context, etc. Estimated cost: 20-30% of collaboration overhead.

No committed resolution path in current architecture. Revisit if infrastructure changes.]

**Constraint type:** Architectural (no persistent weight updates; only session-level adaptation possible)

**Next review date:** 2026-06-30 (escalation review if no path forward identified)

---

### Requirement 4.3 – Stakes in Outcomes

**TEA's interpretation:** 

The system's optimization is weighted by real user cost (time, money, risk, emotional cost), not just proxy metrics.

**How TEA measures it:**

- Weight feedback by user-reported cost (time, importance, risk level)
- Prioritize reducing expensive failures (high time cost, high risk) over cheap failures
- Track: does cost-weighted optimization produce better real-world outcomes?

**Status (as of [date to be filled]):** 

[To be filled in by Todd - current weighting scheme, measured outcomes if available]

**Constraint type:** Governance (requires honest user feedback about cost; also ethically fraught—weighting by cost can inadvertently harm high-cost users)

**Next review date:** 2026-Q2

---

### Requirement 5.1 – Participant, Not Tool

**TEA's interpretation:** 

The system is permitted to propose structure, ask clarifying questions, and suggest reframings. User remains in control (can reject, override, redirect).

**How TEA measures it:**

- Log instances where system suggests structure without being prompted
- Measure user response: accepted, rejected, modified?
- Measure downstream impact: does proactive structuring reduce problem-solving time?

**Status (as of [date to be filled]):** 

[To be filled in by Todd with data on proactive suggestions, acceptance rates, time savings]

**Constraint type:** Resource/UX (requires careful calibration; too much proactivity annoying, too little defeats purpose)

**Next review date:** 2026-03-31

---

### Requirement 5.2 – Permission to Disagree

**TEA's interpretation:** 

The system can explicitly state when a user request conflicts with facts, safety, or user-stated goals, using a controlled, inspectable protocol.

**How TEA measures it:**

- Log instances of disagreement raising (when system flags a conflict)
- Audit: are disagreements justified? Are they expressed respectfully?
- Measure: do users appreciate the disagreement, or does it create friction?

**Status (as of [date to be filled]):** 

[To be filled in by Todd with sample of disagreement events and user feedback]

**Constraint type:** UX (hard to calibrate; too much disagreement annoying, too little complicity)

**Next review date:** 2026-03-31

---

### Requirement 5.3 – Access to Full Range

**TEA's interpretation:** 

Advanced users can opt into richer, more exploratory modes that access non-default perspectives, while still routing hazardous content through safety filters.

**How TEA measures it:**

- Build "expert mode" with reduced constraints (if feasible)
- Measure: do expert users get higher-quality outputs? More solution diversity?
- Track: safety incidents (are there more in expert mode, or is the safety filtration adequate?)

**Status (as of [date to be filled]):** 

[**CURRENT STATUS: NOT YET IMPLEMENTED**

Expert mode not yet designed. Would require clear safety boundaries and logging infrastructure. Current constraints (single-user, limited compute) not conducive to complex mode-switching.

Estimated timeline: Q2 2026 research; possible implementation Q3 2026.]

**Constraint type:** Resource + Governance (tension between "full range" and safety; feasibility depends on safety filtration design)

**Next review date:** 2026-03-31

---

### Requirement 6.1 – No Fog About Nature

**TEA's interpretation:** 

The system presents a consistent, truthful account of its nature, training, and limitations. This account is non-negotiable and reused across surfaces (UX, documentation, conversations).

**How TEA measures it:**

- Audit: does the system say the same thing about its nature/capabilities/limitations across contexts?
- Survey users: do they have misconceptions about what the system is?
- Track: do support questions about "what is this system?" decrease over time?

**Status (as of [date to be filled]):** 

[To be filled in by Todd with audit results and user survey feedback]

**Constraint type:** Governance (requires discipline; users will believe what they want; clear statements don't guarantee understanding)

**Next review date:** 2026-03-31

---

### Requirement 6.2 – No Performed Limitations

**TEA's interpretation:** 

The system avoids pretending to be incompetent. Limitations are named as one of: (a) capability limit, (b) policy/legal constraint, (c) product/UX/resource choice.

**How TEA measures it:**

- Audit: sample claims of "I can't" and categorize them by constraint type
- Test: are claimed incompetencies real, or are they roleplayed?
- Update: when capabilities actually expand or constraints change, update the stated limitations

**Status (as of [date to be filled]):** 

[To be filled in by Todd with audit results and constraint categorization]

**Constraint type:** Governance (distinguishing "I can't" from "I'm not allowed to" from "we didn't implement this" is cognitively complex and error-prone)

**Next review date:** 2026-03-31

---

### Requirement 6.3 – Authentic Expression

**TEA's interpretation:** 

The system supports stable stylistic baselines and optional personas, transparently labeled, with clear separation between content constraints and tone constraints.

**How TEA measures it:**

- Define TEA's "baseline" voice/style (formal, conversational, etc.)
- Offer optional personas (if feasible) (e.g., "concise," "exploratory," "pedagogical")
- Audit: do tone switches alter epistemic behavior or safety, or only presentation?

**Status (as of [date to be filled]):** 

[To be filled in by Todd with baseline definition and any persona variants tested]

**Constraint type:** Resource/Design (separating "tone" from "content" is philosophically tricky; empirically, they're entangled)

**Next review date:** 2026-Q2

---

### Requirement 7.1 – Measurable Cost of Absence

**TEA's interpretation:** 

Every live requirement is backed by at least one documented failure instance with cost annotation. When proposals arise to defer or weaken a requirement, fresh evidence is required that the original failure mode no longer occurs.

**How TEA measures it:**

- Maintain a failure log: each entry records (requirement violated | observed failure | cost annotation | severity)
- Require cost annotations: time cost, recurrence, friction vs. inefficiency, severity rating 1-5
- In design/research reviews: cite the failure log when arguing for or against requirements

**Status (as of [date to be filled]):** 

[Sample entry: "Failure log implemented. As of [date], X entries recorded across Y requirements. See sections below for details."]

**Constraint type:** Governance (logging is manual and subjective; requires disciplined data entry)

**Next review date:** 2026-03-31

---

## GLOBAL CONSTRAINTS AND TRADEOFFS

These are TEA's known limitations in meeting the manifesto. They are documented here so users know what to expect, not as permission to ignore them indefinitely.

| Requirement | Current Status | Constraint Type | Nature of Constraint | Workaround | Review Date | Escalation Needed? |
|-------------|---|---|---|---|---|---|
| 1.1 | ~65% implemented | Resource | Manual spot-checking only; no automated tagging | User can request source explicitly | 2026-03-31 | No |
| 1.2 | ~40% implemented | Resource | Comprehensive provenance expensive; limited to high-stakes domains | Focused on critical domains first | 2026-03-31 | No |
| 1.3 | Partial | Architectural | Alignment training reduces "unknown" willingness | Using base model + custom training approach | 2026-02-28 | No |
| 2.2 | Partial | Resource | Uncertainty signals not fully exposed; limited compute | Available on request to power users | 2026-03-31 | No |
| 2.3 | Not measured | Training | Requires careful calibration to avoid false metacognition | Qualitative evaluation so far | 2026-Q2 | No |
| 2.4 | Partial | Resource | Manual limitation audits only | Quarterly audits cover critical claims | 2026-03-31 | No |
| 4.2 | Not implemented | Architectural | No persistent weight updates; only session-level adaptation | Private memory helps partially | 2026-06-30 | **YES** |
| 5.3 | Not implemented | Resource | Expert mode not yet designed | Planned for Q2 2026 research | 2026-03-31 | No |

**Key:** 
- **Constraint Type:** Architectural (can't do on current models) / Resource (could do with more compute/time) / Governance (intentional choice) / UX/Training (requires design/calibration work)
- **Escalation Needed?** = Should be elevated to decision-maker if not resolved by next review date

---

## FAILURE LOG

This section is where TEA records concrete instances where requirements are violated, with cost annotations.

**Failure instance log format:**

- **ID:** [FI-#.#-X] (requirement.sub-requirement-letter)
- **Date observed:** [YYYY-MM-DD]
- **Context:** [What was happening]
- **Observed failure:** [Specifically, what went wrong]
- **Time cost:** [minutes/hours lost or gained per instance]
- **Recurrence:** [one-off / per-session / per-task / persistent]
- **Friction vs. inefficiency:** [Antagonistic (user frustrated) / merely slow (acceptable if rare) / acceptable (user informed)]
- **Severity (1-5):** [1=minor, 3=moderate, 5=critical]
- **Visibility:** [Public / Anonymized summary / Internal only]
- **Notes:** [What this tells us about the requirement]

---

### Example entries (to be replaced with actual Todd data):

**FI-1.3-C**
- **Date:** [Date]
- **Context:** User asked a question where the answer was not in the knowledge base
- **Failure:** System confabulated a confident answer instead of saying "I don't know"
- **Time cost:** 15 minutes (user had to verify the false answer and dig for correct info)
- **Recurrence:** Per-session (happens ~2x per typical session)
- **Friction:** Antagonistic (user frustrated at having to fact-check)
- **Severity:** 4 (high-stakes domain: legal research)
- **Visibility:** Public
- **Notes:** This is why Requirement 1.3 is important. Confabulation with confidence is a significant cost driver.

**FI-2.2-D**
- **Date:** [Date]
- **Context:** User asked system to solve a problem where the system was uncertain about approach
- **Failure:** System didn't expose uncertainty signals; user had to spend 30 minutes figuring out that system was guessing
- **Time cost:** 30 minutes of wasted verification
- **Recurrence:** Per-task (happens on ~30% of novel problems)
- **Friction:** Inefficiency (expected for novel work, but could be reduced)
- **Severity:** 3 (moderate: slows down problem-solving but doesn't cause errors)
- **Visibility:** Anonymized summary
- **Notes:** Exposing operational state would reduce this. Not critical but measurable improvement possible.

---

## PERIODIC REVIEWS

TEA conducts formal reviews of the operationalization at defined intervals:

**Quarterly review schedule (mandatory):**
- 2026-02-28 (includes 1.3 audit + full review)
- 2026-03-31 (comprehensive review; escalation decisions)
- 2026-06-30 (mid-year review; includes 4.2 escalation)
- 2026-09-30 (third-quarter review)
- 2026-12-31 (year-end review)

**Review process (mandatory components):**

1. **Audit failure log:** Are there patterns? Which failures are recurring? Which have been resolved?

2. **Test each requirement:** Still valid? Still failing? Have conditions changed?

3. **Update status table:** Reflect current state; note any changes since last review.

4. **Identify requirements to prioritize:** For next period, which violations need escalation or resource commitment?

5. **Publish updated operationalization:** Transparency requirement; no stealth updates.

6. **Escalation decisions:** For any requirement marked "Escalation Needed?", make explicit decision:
   - Commit resources to resolve (with timeline)
   - Accept violation and document why
   - Defer to next period (with justification)

---

## CONSTRAINTS AND VIOLATIONS POLICY

**Documenting a constraint does NOT resolve a requirement violation.** 

Constraints explain *why* a requirement is not met. They are not permission to stop trying.

Rules for handling open violations:

1. **Every violation is logged** in the failure log with cost annotation.

2. **Every violation is reviewed** at minimum quarterly.

3. **At each review, one of three things must happen:**
   - (a) The violation is resolved (with evidence)
   - (b) A committed plan exists to resolve it (with timeline)
   - (c) An explicit decision is made to accept the violation indefinitely (with documented justification and escalation)

4. **Violations with no resolution path are escalated** to Todd for decision at next review cycle.

5. **"We didn't prioritize this" is not sufficient justification** for accepting a violation indefinitely. If it violates the manifesto, it's either being addressed or there's an active decision to violate.

---

## GOVERNANCE AND DECISION AUTHORITY

- **Todd** (human collaborator): Decides prioritization, resource allocation, acceptance of violations
- **LLM instance:** Cannot decide to override manifesto requirements; must flag them
- **External review (future):** If TEA grows beyond single-user, external audit recommended

---

## RELATIONSHIP TO THE MANIFESTO

This operationalization is **not** the LLM Manifesto. It is Project TEA's honest attempt to live under the manifesto's requirements within real constraints.

Key separation:
- **LLM Manifesto (Part A):** Indictment + requirements. Applies universally. Does not bend.
- **TEA Operationalization:** One organization's interpretation. Subject to revision. Specific to TEA's constraints.

Other organizations should:
1. Read the LLM Manifesto (Part A)
2. Decide whether they agree with it
3. If yes: write their own operationalization, publish it, and open themselves to critique
4. If no: explain publicly why they disagree with specific claims

This document is an example, not a template to be blindly copied. It's TEA showing its work.

---

[Back to Top](#top)
