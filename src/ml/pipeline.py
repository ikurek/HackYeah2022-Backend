from typing import Tuple, List, Optional, Dict

from src.ml.language import get_language, translate, LANGUAGE_REVERSE_MAPPER, polish_text_to_embeddings, PL, EN, \
    score_scam_potential


def process_tweet(text: str) -> Optional[Tuple[List[float], Dict[str, float]]]:
    """
    Translate tweet, calculate embeddings by HerBERT and score scam by one zero shot model.

    :return: tuple of list of embeddings and list with scam scores
    """
    if text_language := get_language(text):
        texts = {
            text_language: text,
            LANGUAGE_REVERSE_MAPPER[text_language]: translate(text, text_language)
        }
        return polish_text_to_embeddings(texts[PL]), score_scam_potential(texts[EN])
    return None
