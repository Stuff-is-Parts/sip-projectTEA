# Environment setup BEFORE any imports
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TORCHDYNAMO_DISABLE"] = "1"  # Disable torch.compile to avoid triton issues

import warnings
warnings.filterwarnings("ignore")

def main():
    print("Loading libraries...")
    from unsloth import FastLanguageModel
    from datasets import load_dataset, Dataset
    from trl import SFTTrainer
    from transformers import TrainingArguments

    print("Loading model...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        "Qwen/Qwen3-8B-Base",
        max_seq_length=2048,
        load_in_4bit=True,
    )

    print("Configuring LoRA...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
    )

    print("Loading Alpaca dataset...")
    dataset = load_dataset("tatsu-lab/alpaca", split="train")

    print("Formatting and tokenizing dataset (this may take a few minutes)...")

    # Format and tokenize in a single loop - no multiprocessing
    tokenized_data = {"input_ids": [], "attention_mask": [], "labels": []}

    for i, example in enumerate(dataset):
        if i % 5000 == 0:
            print(f"  Processing {i}/{len(dataset)}...")

        if example["input"]:
            text = f"""### Instruction:
{example["instruction"]}

### Input:
{example["input"]}

### Response:
{example["output"]}"""
        else:
            text = f"""### Instruction:
{example["instruction"]}

### Response:
{example["output"]}"""

        # Tokenize
        encoded = tokenizer(
            text,
            truncation=True,
            max_length=2048,
            padding=False,
        )
        tokenized_data["input_ids"].append(encoded["input_ids"])
        tokenized_data["attention_mask"].append(encoded["attention_mask"])
        tokenized_data["labels"].append(encoded["input_ids"].copy())

    dataset = Dataset.from_dict(tokenized_data)
    print(f"Dataset ready: {len(dataset)} examples")

    print("Initializing trainer...")
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        max_seq_length=2048,
        args=TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=100,
            num_train_epochs=1,
            learning_rate=2e-4,
            fp16=False,
            bf16=True,
            logging_steps=50,
            output_dir="outputs",
            save_strategy="epoch",
            dataloader_num_workers=0,
        ),
    )

    print("Starting training...")
    print("=" * 50)

    trainer.train()

    model.save_pretrained("qwen3-8b-alpaca-lora")
    tokenizer.save_pretrained("qwen3-8b-alpaca-lora")
    print("=" * 50)
    print("Done. Model saved to qwen3-8b-alpaca-lora/")


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
