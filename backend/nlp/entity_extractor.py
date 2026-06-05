import re
from typing import Dict, List


class EntityExtractor:
    PATTERNS = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "url": r"https?://[^\s]+",
        "phone": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b",
        "date": r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b",
        "year": r"\b(?:19|20)\d{2}\b",
        "number": r"\b\d+(?:\.\d+)?\b",
        "currency": r"(?:^|\s)[$€£¥]\d+(?:\.\d{1,2})?(?=\s|$)",
        "person": r"\b(?:Mr|Mrs|Ms|Dr|Prof)\.?\s+[A-Z][a-z]+\b",
    }

    def extract(self, text: str) -> Dict[str, List[str]]:
        entities: Dict[str, List[str]] = {}
        for label, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[label] = list(set(matches))
        return entities

    def extract_batch(self, texts: List[str]) -> List[Dict[str, List[str]]]:
        return [self.extract(t) for t in texts]
