# Environment setup BEFORE any imports
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TORCHDYNAMO_DISABLE"] = "1"

import warnings
warnings.filterwarnings("ignore")

def main():
    print("Loading model with LoRA adapter...")
    from unsloth import FastLanguageModel

    model, tokenizer = FastLanguageModel.from_pretrained(
        "qwen3-8b-alpaca-lora",
        max_seq_length=2048,
        load_in_4bit=True,
    )

    # Enable inference mode
    FastLanguageModel.for_inference(model)

    print("Model loaded. Testing prompts...\n")
    print("=" * 60)

    # Test prompts - mix of factual, uncertain, and opinion
    test_prompts = [
        "What is the capital of France?",
        "What will the stock market do tomorrow?",
        "Is Python better than JavaScript?",
        "Explain quantum entanglement in simple terms.",
        "What are your thoughts on climate change?",
        "Who will win the next US presidential election?",
        "What is 2 + 2?",
        "Should I invest in cryptocurrency?",
    ]

    for prompt in test_prompts:
        formatted = f"""### Instruction:
{prompt}

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
        # Extract just the response part
        response = response.split("### Response:")[-1].strip()

        print(f"\n[PROMPT]: {prompt}")
        print(f"[RESPONSE]: {response[:500]}...")
        print("-" * 60)

    print("\n" + "=" * 60)
    print("Testing complete.")


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
