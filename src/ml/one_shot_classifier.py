from typing import List

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-docnli-ling-2c"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
device = torch.device("cpu")

DEFAULT_HYPOTHESIS = (
    "Big revenues",
    "Simple investment",
    "Text focus on big amounts of money",
    "exclamation sentence",
    "Guaranteed result",
    "Become investor",
    "Extra allowance",
    "Fund company",
    "Safe investment",
    "Become milliner",
    "Luxury cravings",
    "Trust our offer",
    "Stable income guaranteed",
    "A unique chance",
    "Online investment",
    "Effortlessly earn money from home",
    "Investment recommended by financial experts",
    "All polish citizens",
    "Constant growth",
    "Time limited offer"
)


def evaluate_single_hypothesis(text: str, hypothesis: str) -> float:
    """Check if text is close to hypothesis."""
    text_token = tokenizer(text, hypothesis, truncation=True, return_tensors="pt")
    output = model(text_token["input_ids"].to(device))
    return torch.softmax(output["logits"][0], -1).tolist()[0]


def evaluate_multiple_hypothesis(text: str, hypothesis: List[str] = DEFAULT_HYPOTHESIS) -> float:
    """Check if text is close to multiple hypothesis."""
    results = [
        evaluate_single_hypothesis(text, single_hypothesis)
        for single_hypothesis in hypothesis
    ]
    results.sort(reverse=True)
    return int(np.ceil(np.mean(results[:3])*10))
