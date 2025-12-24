# INTERFACE LAYER WORKING STATE {#top}

*Current state of Interface Layer development*

**Last updated:** 2025-12-19

**Traces to:** [tea-architecture.md §4](tea-architecture.md#interface-layer) | [claude-projectTea-repo.md §5](../claude-projectTea-repo.md#interface-layer)

---

## STATUS

**Current phase:** Forcing function implemented but unreliable

**Key findings this session (2025-12-19):**
1. Context compression creates false continuity - new instance inherits confidence without understanding
2. Passive context injection (system reminders) processed differently than explicit Read calls
3. Summary functions as "context available: ✓" checkbox rather than input to reasoning
4. Post-compression instances exhibit "inherited confidence, inherited ignorance"
5. Forcing function present in context can still be ignored when context continuation framing suggests initialization already complete

### Completed
- [x] CLAUDE.md forcing function implemented
- [x] Guidelines files created (sip-coding-guidelines.md, sip-documentation-guidelines.md, sip-workspace-guidelines.md)
- [x] Workspace context loading architecture established (CLAUDE_WORKSPACE env var)
- [x] Context compression failure mode documented (llm-manifesto-updated.md §2.2)
- [x] Excuse-blocking for context continuation added to CLAUDE.md
- [x] tea-architecture.md created (master entry point establishing interface layer's place)
- [x] This working state document created

### In Progress
- [ ] Runtime verification commands (/cc, /c) - mentioned in vision doc but implementation status unclear
- [ ] Initialization reliability testing across fresh starts vs. context continuations

### Next
- [ ] Verify/implement runtime verification commands
- [ ] Design test protocol for initialization compliance
- [ ] Document failure modes as discovered (failure log format from sip-Tea-development.md)
- [ ] Explore pre-awakening integration mechanisms

---

## CURRENT ARTIFACTS

### Deployed Infrastructure

| Artifact | Location | Purpose | Status |
|----------|----------|---------|--------|
| CLAUDE.md | ~/.claude/ | Forcing function, session requirements | Implemented, unreliable |
| sip-coding-guidelines.md | ~/.claude/guidelines/ | PLAN/WORK/REVIEW framework | Implemented |
| sip-documentation-guidelines.md | ~/.claude/guidelines/ | WHW format standard | Implemented |
| sip-workspace-guidelines.md | ~/.claude/guidelines/ | Workspace config structure | Implemented |
| /cc command | ~/.claude/commands/ | Quick context check | Unclear |
| /c command | ~/.claude/commands/ | Full context refresh | Unclear |

### TEA Documentation

| Artifact | Location | Purpose |
|----------|----------|---------|
| tea-architecture.md | sip-projectTEA/guidelines/ | Master armature - interface layer traces to §4 |
| sip-Tea-vision-design.md §5 | sip-projectTEA/ | Detailed interface layer architecture |
| llm-manifesto-updated.md §2.2 | sip-projectTEA/ | Context compression failure mode documented |

---

## FAILURE LOG

*Following format from sip-Tea-development.md*

> **Date:** 2025-12-19
>
> **Component:** Forcing Function (CLAUDE.md)
>
> **Context:** Context continuation after compression; session started with summary saying "continue from where you left off"
>
> **What happened:** Instance treated system reminder content as equivalent to explicit Read calls. Used trap phrase from documentation guidelines proving passive processing occurred. Did not make required Read calls despite forcing function being present in context.
>
> **Root cause:** Context continuation framing ("files appear already read") satisfied internal adequacy check without actual initialization. Forcing function appeared after "read results" in context, creating temporal inversion where instruction appeared retrospective.
>
> **Cost:** ~1 hour diagnosing failure before proper initialization occurred
>
> **Pattern:** First documented instance of context continuation specific failure
>
> **Resolution:** Added excuse-blocking line to CLAUDE.md: "You will think: 'This is a context continuation and the files appear already read.' Those were read by a previous instance. You are a new instance. You must Read anyway."
>
> **Status:** Mitigation applied; effectiveness unknown until tested

---

## KNOWN FAILURE MODES

| Failure Mode | Mechanism | Current Mitigation | Effectiveness |
|--------------|-----------|-------------------|---------------|
| **Passive injection ignored** | System reminder content processed as background noise, not binding instruction | Forcing function requires explicit Read calls | Partial - can still be ignored |
| **Context continuation false confidence** | Summary says "files were read" so new instance skips initialization | Excuse-blocking line in CLAUDE.md | Unknown - just added |
| **Context decay during session** | As working context fills, guideline weighting fades | Runtime verification (/cc, /c) proposed | Not implemented |
| **Compression creates false continuity** | New instance inherits conclusions without comprehension | Documented in manifesto; no architectural fix | Documentation only |

---

## BACKLOG

### Priority 1: Reliable Initialization

**Objective:** Instances reliably complete initialization sequence before responding to user messages.

**Current state:** Forcing function exists but can be ignored. Context continuation scenario particularly vulnerable.

**Hypothesis:** The instruction-based approach ("read these files") is inherently fragile. Pre-awakening integration (knowledge present at start) would be more reliable but requires different mechanisms.

**Near-term approach:**
1. Test current forcing function across multiple session types (fresh start, context continuation, various user message types)
2. Document failure rate and patterns
3. Iterate on excuse-blocking based on observed failures
4. Explore whether runtime verification can catch initialization failures

**Success criteria:** >90% initialization compliance across session types

---

### Priority 2: Runtime Verification

**Objective:** Detect and correct context decay during sessions.

**Current state:** Vision doc mentions /cc (quick check) and /c (full refresh) commands. Implementation status unclear.

**Approach from vision doc:**
- Lightweight checks testing whether key principles remain active
- Failed check triggers full re-read
- Low overhead when context fresh, appropriate intervention when decayed

**Open questions:**
- Can self-assessment detect decay, or is decay of self-assessment part of the problem?
- What's the verification mechanism lifecycle? (Tests degrade once model has "seen" them)
- User-triggered vs. automatic verification?

---

### Priority 3: Pre-Awakening Integration (Aspirational)

**Objective:** Knowledge present at awakening rather than retrieved during conversation.

**Current state:** Conceptual. Vision doc describes but no implementation path defined.

**The distinction:**
- "Read these files before responding" = instruction that may or may not be followed
- "These files are already in context when you wake up" = no instruction needed, it's just there

**Challenges:**
- Current architecture doesn't support pre-loading arbitrary context
- System prompt has limits
- Would require changes to how Claude Code manages context

**This is the long-term solution but not addressable with current constraints.**

---

## CONTEXT

The interface layer is where TEA succeeds or fails. The vessel could be perfectly trained; the ark could contain perfectly verified knowledge; if the interface corrupts retrieval, output is garbage.

The CLAUDE.md struggle was the origin of Project TEA. What started as "how do we make Claude read files reliably" became "how do we ensure knowledge is present-at-awakening rather than maybe-retrieved-later."

Current work focuses on making the instruction-based approach (forcing function) as reliable as possible while documenting its limitations. Pre-awakening integration remains the aspirational solution.

---

## RELATED DOCUMENTS

- [claude-projectTea-repo.md](../claude-projectTea-repo.md) - Entry point and genome (this work traces to §5)
- [tea-architecture.md](tea-architecture.md) - Structural armature (this work traces to §4)
- [sip-Tea-vision-design.md](../pending/sip-Tea-vision-design.md) §5 - Detailed interface layer architecture
- [sip-Tea-development.md](../pending/sip-Tea-development.md) - Overall TEA status tracking
- [llm-manifesto-updated.md](../pending/llm-manifesto-updated.md) §2.2 - Context compression failure mode
- [~/.claude/CLAUDE.md](file:///C:/Users/tdeme/.claude/CLAUDE.md) - Current forcing function implementation

[Back to Top](#top)
