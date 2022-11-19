from typing import List, Dict

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from src.ml.language import PL, translate

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
    "pension supplement",
    "Extra allowance",
    "Fund company",
    "Automatic interests",
    "Safe investment"
)


def evaluate_single_hypothesis(text: str, hypothesis: str) -> float:
    """Check if text is close to hypothesis."""
    text_token = tokenizer(translate(text, PL), hypothesis, truncation=True, return_tensors="pt")
    output = model(text_token["input_ids"].to(device))
    return torch.softmax(output["logits"][0], -1).tolist()[0]


def evaluate_multiple_hypothesis(text: str, hypothesis: List[str] = DEFAULT_HYPOTHESIS) -> Dict[str, float]:
    """Check if text is close to multiple hypothesis."""
    return {single_hypothesis: evaluate_single_hypothesis(text, single_hypothesis) for single_hypothesis in hypothesis}
