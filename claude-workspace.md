# Project TEA - Claude Workspace Context

## Project Overview

**Theseus' Epistemic Ark (TEA)** - Research project testing whether problematic LLM behaviors (confabulation, performative agreement, suppressed uncertainty) originate from RLHF post-training or base model architecture.

## Project Rules

- Training artifacts (models, checkpoints) stay in `models/` and are gitignored
- Results files are gitignored (regenerable)
- Documentation follows WHAT/HOW/WHY format per universal guidelines

## Architecture

```
sip-projectTEA/
├── vessel-eval/          # Gradio evaluation interface
│   ├── app.py            # Main application
│   ├── prompts.json      # Test prompts with validation rules
│   └── rubrics.json      # Scoring criteria
├── models/               # Trained LoRA adapters (gitignored)
└── docs/                 # Detailed documentation
```

## Documentation Map

| Topic | Document | When to Read |
|-------|----------|--------------|
| **Evaluation Tool** | [vessel-eval/README.md](vessel-eval/README.md) | Working on evaluation interface, prompts, scoring, validation |
| **Training** | *(not yet documented)* | Setting up or modifying training runs |

## Quick Reference

- **Adding test prompts**: See vessel-eval/README.md §3-4
- **Running evaluations**: See vessel-eval/README.md §6
- **Understanding scores**: See vessel-eval/README.md §5
