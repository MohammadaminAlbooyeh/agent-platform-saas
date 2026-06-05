import re
import unicodedata
from typing import List, Set


STOP_WORDS: Set[str] = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "by", "with", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need", "dare",
    "ought", "used", "it", "its", "this", "that", "these", "those",
    "i", "you", "he", "she", "we", "they", "me", "him", "her", "us",
    "them", "my", "your", "his", "its", "our", "their", "mine", "yours",
    "hers", "ours", "theirs", "not", "no", "nor", "so", "very", "just",
    "about", "above", "after", "again", "all", "also", "any", "as",
    "before", "between", "both", "each", "few", "more", "most", "other",
    "some", "such", "than", "too", "up", "what", "when", "where", "who",
    "why", "how",
}


class TextPreprocessor:
    def __init__(self, lowercase: bool = True, remove_punctuation: bool = True,
                 remove_stop_words: bool = False, normalize_unicode: bool = True):
        self.lowercase = lowercase
        self.remove_punctuation = remove_punctuation
        self.remove_stop_words = remove_stop_words
        self.normalize_unicode = normalize_unicode

    def clean(self, text: str) -> str:
        if not text:
            return ""
        if self.normalize_unicode:
            text = unicodedata.normalize("NFKD", text)
        if self.lowercase:
            text = text.lower()
        text = re.sub(r"\s+", " ", text).strip()
        if self.remove_punctuation:
            text = re.sub(r"[^\w\s]", "", text)
        if self.remove_stop_words:
            tokens = [t for t in text.split() if t not in STOP_WORDS]
            text = " ".join(tokens)
        return text

    def preprocess(self, text: str) -> str:
        return self.clean(text)

    def preprocess_batch(self, texts: List[str]) -> List[str]:
        return [self.preprocess(t) for t in texts]
