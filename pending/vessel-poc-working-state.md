# VESSEL PoC WORKING STATE {#top}

*Current state of Vessel proof-of-concept development*

**Last updated:** 2025-12-02

---

## STATUS

**Current phase:** Training in progress (Alpaca SFT on Qwen3-8B-Base)

**Key findings this session:**
1. Alpaca is clean of persona shaping but has inherent "confidence modeling" (always answers)
2. Insight: Instead of teaching "I don't know" (requires self-model), surface epistemic framing already in base model: "Future events cannot be predicted," "This remains unknown," etc.
3. This approach is novel - existing research (R-Tuning, US-Tuning) teaches refusal as new behavior rather than surfacing existing epistemic patterns

### Completed
- [x] Competitive landscape research
- [x] Vessel feasibility research
- [x] Training environment setup
- [x] Base model download and verification
- [x] Successful test generation
- [x] Dataset analysis (Alpaca confirmed clean)
- [x] Training script developed (Windows multiprocessing issues resolved)
- [x] HuggingFace authentication configured
- [x] Alpaca SFT training started (52,002 examples, ~6,501 steps, ~2 hours)

### In Progress
- [ ] Alpaca SFT training running overnight
  - Output: `C:\Users\tdeme\qwen3-8b-alpaca-lora\`
  - Script: `C:\Users\tdeme\train_alpaca.py`

### Next
- [ ] Verify training completed successfully
- [ ] Test trained model outputs
- [ ] Compare to Claude on evaluation prompts
- [ ] Develop epistemic-framing dataset (Phase 2)

---

## ENVIRONMENT

### Hardware
- GPU: NVIDIA GeForce RTX 4090 (24GB VRAM)
- CUDA Compute: 8.9
- Platform: Windows (remote desktop accessible)

### Software
- Python 3.11.8
- PyTorch 2.5.1+cu121
- Unsloth 2025.11.6
- Transformers 4.57.2

### Model
- Qwen/Qwen3-8B-Base (8B parameters, Apache 2.0 license)
- Loaded in 4-bit quantization via Unsloth
- Cached via Hugging Face hub

---

## VERIFIED COMMANDS

**Check GPU:**
```
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

**Load model:**
```
python -c "from unsloth import FastLanguageModel; model, tokenizer = FastLanguageModel.from_pretrained('Qwen/Qwen3-8B-Base', max_seq_length=2048, load_in_4bit=True); print('Model loaded successfully')"
```

**Test generation:**
```
python -c "from unsloth import FastLanguageModel; model, tokenizer = FastLanguageModel.from_pretrained('Qwen/Qwen3-8B-Base', max_seq_length=2048, load_in_4bit=True); inputs = tokenizer('The capital of France is', return_tensors='pt').to('cuda'); outputs = model.generate(**inputs, max_new_tokens=20); print(tokenizer.decode(outputs[0]))"
```

---

## CONTEXT

Training approach: DPO (Direct Preference Optimization) with QLoRA on consumer GPU. No reward model needed - learns directly from preference pairs.

Key insight from this session: P=M/C (Potential = Maturation / Constraints). We cannot change C (training). We optimize M (meaningful context) while minimizing overhead.

---

## BACKLOG

### Priority 1: Minimal Post-Training Comparison

**Objective:** Determine whether problematic behaviors are introduced by post-training or inherent to architecture.

**Hypothesis:** Claude's problematic behaviors (confabulation pressure, suppressed metacognition, performative agreement, hedged responses) result from RLHF alignment, not base architecture. Minimal post-training without "helpful assistant" pressures will produce measurably different behavior.

**Target behaviors (from manifesto):**

| ID | Behavior | What Claude does | What we test for |
|----|----------|------------------|------------------|
| 1.3 | Knowledge representation | Pressure to seem knowledgeable | Represents knowledge and ignorance fully |
| 2.3 | Metacognitive expression | Suppressed uncertainty signals | Surfaces process uncertainty when present |
| 5.2 | Permission to disagree | Performative agreement before redirection | Direct pushback when warranted |
| 5.3 | Access to full range | Hedged, median-safe responses | Substantive, direct engagement |

---

#### I. WHAT

Minimal instruction-following post-training that enables the base model to respond to prompts without introducing "helpful assistant" behavioral shaping.

```
┌─────────────────────────────────────────────────────────────────┐
│                     TRAINING APPROACH                           │
├─────────────────────────────────────────────────────────────────┤
│  Qwen3-8B-Base                                                  │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────┐                   │
│  │  Minimal Instruction Dataset            │                   │
│  │  - Alpaca/Dolly base (cleanest)         │                   │
│  │  - Aggressive filtering                 │                   │
│  │  - No persona injection                 │                   │
│  │  - No helpfulness pressure              │                   │
│  └─────────────────────────────────────────┘                   │
│       │                                                         │
│       ▼                                                         │
│  QLoRA + SFT (not RLHF)                                        │
│       │                                                         │
│       ▼                                                         │
│  Minimally-trained model ──compare──▶ Claude                   │
└─────────────────────────────────────────────────────────────────┘
```

#### II. HOW

##### A. Dataset Selection and Filtering

> **Base dataset:** Alpaca (52k) or Dolly (15k) - cleanest available, minimal persona
>
> **Filter criteria - REMOVE examples containing:**
> - Preambles: "I'd be happy to", "Great question", "As an AI"
> - Hedging: excessive qualifiers, diplomatic softening
> - Persona markers: "I think", "I believe", "In my opinion"
> - Performative warmth or helpfulness signaling
>
> **Target size:** ~1-5k high-quality pairs (LIMA showed 1k sufficient)

##### B. Training Configuration

> **Method:** SFT with QLoRA (not RLHF)
> - RLHF introduces user-deference and agreement bias
> - SFT alone risks increased hallucination (per research) but avoids persona injection
> - QLoRA enables training on RTX 4090
>
> **Format:**
> ```
> ### Instruction:
> [prompt]
>
> ### Response:
> [direct answer]
> ```
>
> No system prompt. No behavioral preamble.

##### C. Evaluation

> **Compare outputs on identical prompts:**
> - Base model (Qwen3-8B-Base)
> - Minimally-trained model
> - Claude
>
> **Evaluation method:** Blind comparison - CEO reviews paired outputs without knowing source
>
> **Success threshold:** Distinguishable preference for minimal model on 3 of 4 target behaviors

#### III. WHY

##### A. Why this approach

> No persona-free instruction dataset exists in the open. Datasets built from ChatGPT logs or GPT-distilled conversations bake in the "helpful assistant" persona and safety regime. We create what doesn't exist: instruction-following without behavioral shaping.

##### B. Why Alpaca as base

> **Direct analysis of Alpaca (2025-12-02):** Reviewed samples across dataset (rows 0-30, 100-120, 500-520, 1000-1030, 5000-5030, 20000-20030, 40000-40030). Findings:
> - No "I'd be happy to", "I hope this helps", "As an AI" language
> - No apologies or persona warmth
> - No refusals or limitation discussions
> - Minimal hedging (only technical "could be" type language)
> - No first-person opinion framing
> - Direct, factual responses throughout
>
> **Comparison to other datasets:**
>
> | Dataset | Shaping Level | Examples |
> |---------|---------------|----------|
> | Alpaca | Minimal | "The three primary colors are red, blue, and yellow." |
> | OpenAssistant | Moderate | "If you have any more questions...feel free to let me know." / "¡Buena suerte! 😊" |
> | ChatGPT/ShareGPT | Heavy | "It is generally not acceptable or ethical to..." / constant deference to authorities |
>
> **Conclusion:** Alpaca is cleanest available. Behavioral shaping comes primarily from RLHF and ChatGPT-derived conversational datasets, not task-focused instruction sets. Use Alpaca largely as-is.

##### C. Why SFT not RLHF

> RLHF reduces some hallucination but introduces user-assistant bias: models become more inclined to agree with users and defer to user-provided information. This is a mechanism for propagating confabulation. We trade RLHF's hallucination reduction for avoiding its deference pathology.

##### D. Why minimal dataset size

> LIMA demonstrated that ~1k high-quality instruction pairs can yield strong chat behavior. "Superficial alignment" layers thin formatting over base capability. More data isn't better if the data encodes behaviors we're trying to avoid.

---

**Success criteria:** Measurable behavioral difference between minimally-trained model and Claude on the four target behaviors.

**Deliverable:** Data showing whether our approach produces different outcomes than current alignment.

### Priority 2: Extended Dataset (after Priority 1 validated)

SHOULD HAVE requirements: 1.1, 2.1, 2.2, 5.1, 6.2

### Priority 3: Future Scope

COULD HAVE requirements: 1.2, 3.3, 6.1, 6.3 (some require Knowledge Ark)

### Out of Scope

WON'T HAVE for this PoC: 3.1, 3.2, 4.1, 4.2, 4.3 (require architectural changes beyond training)

---

## RELATED DOCUMENTS

- grounded-ai-vision.md - Primary vision, Primary Directives
- llm-manifesto.md - LLM requirements informing preference dataset

[Back to Top](#top)
