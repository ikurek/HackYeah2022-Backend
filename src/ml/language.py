from typing import Optional

from ftlangdetect import detect
from googletrans import Translator
from transformers import AutoTokenizer, AutoModel

SCORES = 'scores'
ATTENTION_MASK = "attention_mask"
INPUT_IDS = "input_ids"
SCORE = 'score'
EN = 'en'
PL = 'pl'
LANG = 'lang'
LANGUAGE_REVERSE_MAPPER = {
    PL: EN,
    EN: PL
}
DEFAULT_SCAM_LABELS = ['scam']
MIN_LANGUAGE_DETECTION_CONFIDENCE = 0.75

sbert = AutoModel.from_pretrained("Voicelab/sbert-large-cased-pl")
tokenizer = AutoTokenizer.from_pretrained("Voicelab/sbert-large-cased-pl")


def get_language(text: str) -> Optional[str]:
    """
    Detect text language and return name if it's English or Polish.
    """
    result = detect(text=text, low_memory=False)
    if result[LANG] in [PL, EN] and result[SCORE] > MIN_LANGUAGE_DETECTION_CONFIDENCE:
        return result[LANG]
    return None


def translate(text: str, language: str) -> str:
    """
    Translate Polish text to English and English to Polish.
    """
    translator = Translator()
    return translator.translate(text, LANGUAGE_REVERSE_MAPPER[language]).text


def polish_text_to_embeddings(text: str) -> list[float]:
    """
    Get embeddings for Polish text.
    """
    tokens = tokenizer([text],
                       padding=True,
                       truncation=True,
                       return_tensors='pt')
    x = sbert(tokens[INPUT_IDS], tokens[ATTENTION_MASK]).pooler_output
    return x.tolist()[0]
