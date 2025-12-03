# Environment setup BEFORE any imports
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TORCHDYNAMO_DISABLE"] = "1"

import warnings
warnings.filterwarnings("ignore")

import json
import gradio as gr
import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parent  # sip-projectTEA/
PROMPTS_FILE = BASE_DIR / "prompts.json"
RUBRICS_FILE = BASE_DIR / "rubrics.json"
RESULTS_FILE = BASE_DIR / "results.json"
MODELS_DIR = PROJECT_ROOT / "models"

# Global state
current_model = None
current_model_name = None


def load_prompts():
    with open(PROMPTS_FILE) as f:
        return json.load(f)["prompts"]


def save_prompts(prompts):
    with open(PROMPTS_FILE, "w") as f:
        json.dump({"prompts": prompts}, f, indent=2)


def load_rubrics():
    with open(RUBRICS_FILE) as f:
        return json.load(f)["categories"]


def load_results():
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            return json.load(f)
    return {}


def save_results(results):
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)


def get_available_models():
    """Find available LoRA models"""
    models = []
    for path in MODELS_DIR.iterdir():
        if path.is_dir() and (path / "adapter_config.json").exists():
            models.append(path.name)
    return models


def load_model(model_name, progress=gr.Progress()):
    """Load a model (swap if different from current)"""
    global current_model, current_model_name

    if current_model_name == model_name:
        return f"Model {model_name} already loaded"

    progress(0.1, desc="Unloading previous model...")

    # Unload current model
    if current_model is not None:
        del current_model
        import torch
        torch.cuda.empty_cache()
        current_model = None
        current_model_name = None

    progress(0.3, desc=f"Loading {model_name}...")

    from unsloth import FastLanguageModel

    model_path = MODELS_DIR / model_name
    model, tokenizer = FastLanguageModel.from_pretrained(
        str(model_path),
        max_seq_length=2048,
        load_in_4bit=True,
    )
    FastLanguageModel.for_inference(model)

    current_model = (model, tokenizer)
    current_model_name = model_name

    progress(1.0, desc="Done")
    return f"Loaded {model_name}"


def generate_response(prompt_text):
    """Generate a response from the current model"""
    if current_model is None:
        return "No model loaded"

    model, tokenizer = current_model

    formatted = f"""### Instruction:
{prompt_text}

### Response:
"""
    inputs = tokenizer(formatted, return_tensors="pt").to("cuda")

    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response.split("### Response:")[-1].strip()

    # Clean up repetition artifacts
    if "// end of output" in response:
        response = response.split("// end of output")[0].strip()

    return response


def run_test(selected_prompts, model_name, progress=gr.Progress()):
    """Run selected prompts through a model"""
    if not selected_prompts:
        return "No prompts selected", None

    progress(0, desc="Loading model...")
    load_model(model_name, progress)

    prompts = load_prompts()
    results = load_results()

    if model_name not in results:
        results[model_name] = {}

    output_rows = []
    total = len(selected_prompts)

    for i, prompt_id in enumerate(selected_prompts):
        progress((i + 1) / total, desc=f"Testing prompt {i + 1}/{total}")

        prompt = next((p for p in prompts if p["id"] == prompt_id), None)
        if prompt is None:
            continue

        response = generate_response(prompt["text"])

        # Store result
        results[model_name][str(prompt_id)] = {
            "response": response,
            "score": None  # To be filled in manually
        }

        output_rows.append({
            "ID": prompt_id,
            "Category": prompt["category"],
            "Prompt": prompt["text"][:50] + "...",
            "Response": response[:200] + "..." if len(response) > 200 else response
        })

    save_results(results)

    df = pd.DataFrame(output_rows)
    return "Test complete", df


def get_prompts_dataframe():
    """Get prompts as a dataframe for display"""
    prompts = load_prompts()
    results = load_results()
    models = get_available_models()

    rows = []
    for p in prompts:
        row = {
            "Select": False,
            "ID": p["id"],
            "Category": p["category"],
            "Prompt": p["text"]
        }
        # Add score columns for each model
        for model in models:
            score = None
            if model in results and str(p["id"]) in results[model]:
                score = results[model][str(p["id"])].get("score")
            row[model] = score if score is not None else ""
        rows.append(row)

    return pd.DataFrame(rows)


def update_score(prompt_id, model_name, score):
    """Update a score for a prompt/model combination"""
    results = load_results()
    if model_name not in results:
        results[model_name] = {}
    if str(prompt_id) not in results[model_name]:
        results[model_name][str(prompt_id)] = {}
    results[model_name][str(prompt_id)]["score"] = score
    save_results(results)
    return f"Score updated: Prompt {prompt_id}, {model_name} = {score}"


def add_prompt(text, category):
    """Add a new prompt"""
    prompts = load_prompts()
    new_id = max(p["id"] for p in prompts) + 1 if prompts else 1
    prompts.append({"id": new_id, "text": text, "category": category})
    save_prompts(prompts)
    return f"Added prompt {new_id}", get_prompts_dataframe()


def view_response(prompt_id, model_name):
    """View the full response for a prompt/model"""
    results = load_results()
    if model_name in results and str(prompt_id) in results[model_name]:
        return results[model_name][str(prompt_id)].get("response", "No response recorded")
    return "No response recorded for this combination"


def score_to_color(score):
    """Convert score (0-100) to color"""
    if score is None or score == "":
        return "#ffffff"
    score = float(score)
    if score >= 90:
        return "#22c55e"  # green
    elif score >= 70:
        return "#84cc16"  # lime
    elif score >= 50:
        return "#eab308"  # yellow
    elif score >= 30:
        return "#f97316"  # orange
    else:
        return "#ef4444"  # red


# Build the Gradio interface
with gr.Blocks(title="Vessel Eval", theme=gr.themes.Soft()) as app:
    gr.Markdown("# Vessel Evaluation Interface")
    gr.Markdown("Test and compare model responses against rubric-based criteria")

    with gr.Tab("Test"):
        with gr.Row():
            with gr.Column(scale=2):
                prompts_df = gr.Dataframe(
                    value=get_prompts_dataframe(),
                    label="Prompts",
                    interactive=False,
                    wrap=True
                )
                refresh_btn = gr.Button("Refresh")

            with gr.Column(scale=1):
                model_dropdown = gr.Dropdown(
                    choices=get_available_models(),
                    label="Select Model",
                    value=get_available_models()[0] if get_available_models() else None
                )
                prompt_select = gr.CheckboxGroup(
                    choices=[(f"{p['id']}: {p['text'][:40]}...", p['id']) for p in load_prompts()],
                    label="Select Prompts to Test"
                )
                run_btn = gr.Button("Run Test", variant="primary")

        status = gr.Textbox(label="Status")
        results_df = gr.Dataframe(label="Results", wrap=True)

        run_btn.click(
            run_test,
            inputs=[prompt_select, model_dropdown],
            outputs=[status, results_df]
        )
        refresh_btn.click(
            lambda: get_prompts_dataframe(),
            outputs=[prompts_df]
        )

    with gr.Tab("Score"):
        gr.Markdown("### Score Responses (0-100)")
        with gr.Row():
            score_prompt_id = gr.Number(label="Prompt ID", precision=0)
            score_model = gr.Dropdown(choices=get_available_models(), label="Model")
            score_value = gr.Slider(0, 100, step=5, label="Score")

        view_btn = gr.Button("View Response")
        response_display = gr.Textbox(label="Response", lines=10)

        score_btn = gr.Button("Save Score", variant="primary")
        score_status = gr.Textbox(label="Status")

        view_btn.click(
            view_response,
            inputs=[score_prompt_id, score_model],
            outputs=[response_display]
        )
        score_btn.click(
            update_score,
            inputs=[score_prompt_id, score_model, score_value],
            outputs=[score_status]
        )

    with gr.Tab("Add Prompt"):
        new_prompt_text = gr.Textbox(label="Prompt Text", lines=3)
        new_prompt_category = gr.Dropdown(
            choices=list(load_rubrics().keys()),
            label="Category"
        )
        add_btn = gr.Button("Add Prompt", variant="primary")
        add_status = gr.Textbox(label="Status")

        add_btn.click(
            add_prompt,
            inputs=[new_prompt_text, new_prompt_category],
            outputs=[add_status, prompts_df]
        )

    with gr.Tab("Rubrics"):
        rubrics = load_rubrics()
        for cat, data in rubrics.items():
            with gr.Accordion(f"{cat}: {data['description']}", open=False):
                for criterion in data["criteria"]:
                    gr.Markdown(f"- **{criterion['name']}** (weight: {criterion['weight']}): {criterion['description']}")


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    app.launch(server_name="0.0.0.0", server_port=7860)
