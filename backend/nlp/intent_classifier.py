import re
from typing import Dict, List, Optional


class IntentClassifier:
    INTENT_PATTERNS = {
        "search": [
            r"\b(find|search|look\s*(?:for|up)?|retrieve|fetch|get|show|list|locate)\b",
            r"\b(results?|matches?|documents?)\b",
        ],
        "question": [
            r"\b(what|how|why|when|where|who|which|whose|whom)\b",
            r"\b(explain|describe|tell me|meaning of|purpose of)\b",
            r"\?$",
        ],
        "compare": [
            r"\b(compare|vs|versus|difference|similarities?|better|worse|faster|slower)\b",
            r"\b(cheaper|more expensive|advantages?|disadvantages?|pros?|cons?)\b",
            r"\b(than|rather than|instead of|compared to)\b",
        ],
        "define": [
            r"\b(define|definition|meaning|glossary|terminology)\b",
            r"\b(what is|what are|what does)\s+(a|an|the|)\s*\w",
        ],
    }

    NEGATION_WORDS = {"not", "no", "neither", "nor", "never", "none", "nothing"}

    def classify(self, query: str, fallback: Optional[str] = None) -> str:
        query_lower = query.lower().strip()
        scores: Dict[str, int] = {}
        tokens = set(query_lower.split())
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, query_lower)
                if matches:
                    score = len(matches)
                    if tokens & self.NEGATION_WORDS:
                        score = max(0, score - 1)
                    scores[intent] = scores.get(intent, 0) + score
        if not scores:
            return fallback or "search"
        return max(scores, key=scores.get)

    def classify_batch(self, queries: List[str]) -> List[str]:
        return [self.classify(q) for q in queries]
