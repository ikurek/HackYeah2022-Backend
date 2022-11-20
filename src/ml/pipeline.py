from typing import Tuple, List, Optional

from src.ml.language import get_language, translate, LANGUAGE_REVERSE_MAPPER, polish_text_to_embeddings, PL, EN
from src.ml.one_shot_classifier import evaluate_multiple_hypothesis


def process_tweet(text: str) -> Optional[Tuple[List[float], float]]:
    """
    Translate tweet, calculate embeddings by HerBERT and score scam by one zero shot model.

    :return: tuple of list of embeddings and scam score
    """
    text = text.replace('\n', ' ').replace('\t', ' ')
    if text_language := get_language(text):
        texts = {
            text_language: text,
            LANGUAGE_REVERSE_MAPPER[text_language]: translate(text, text_language)
        }
        return polish_text_to_embeddings(texts[PL]), evaluate_multiple_hypothesis(texts[EN])
    return None
