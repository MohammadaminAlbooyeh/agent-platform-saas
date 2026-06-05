import re
from typing import List


class Tokenizer:
    CONTRACTION_MAP = {
        "don't": "do not", "doesn't": "does not", "didn't": "did not",
        "won't": "will not", "can't": "cannot", "couldn't": "could not",
        "shouldn't": "should not", "wouldn't": "would not", "isn't": "is not",
        "aren't": "are not", "wasn't": "was not", "weren't": "were not",
        "haven't": "have not", "hasn't": "has not", "hadn't": "had not",
        "i'm": "i am", "you're": "you are", "he's": "he is", "she's": "she is",
        "it's": "it is", "we're": "we are", "they're": "they are",
        "i'll": "i will", "you'll": "you will", "he'll": "he will",
        "she'll": "she will", "it'll": "it will", "we'll": "we will",
        "they'll": "they will", "i've": "i have", "you've": "you have",
        "we've": "we have", "they've": "they have",
    }

    def _expand_contractions(self, text: str) -> str:
        text_lower = text.lower()
        for contraction, expansion in self.CONTRACTION_MAP.items():
            text_lower = text_lower.replace(contraction, expansion)
        return text_lower

    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        text = self._expand_contractions(text)
        tokens = re.findall(r"\b\w+(?:'\w+)?\b", text.lower())
        return [t for t in tokens if len(t) > 1 or t in ("a", "i")]

    def tokenize_batch(self, texts: List[str]) -> List[List[str]]:
        return [self.tokenize(t) for t in texts]
