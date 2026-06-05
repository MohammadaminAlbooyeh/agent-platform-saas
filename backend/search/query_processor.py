from typing import List

from backend.nlp.preprocessor import TextPreprocessor


class QueryProcessor:
    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def process(self, query: str) -> str:
        return self.preprocessor.clean(query)

    def expand_query(self, query: str) -> List[str]:
        variants = [query]
        processed = self.process(query)
        if processed != query:
            variants.append(processed)
        return variants
