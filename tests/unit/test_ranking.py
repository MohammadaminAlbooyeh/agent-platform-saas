import pytest

from backend.search.ranker import Ranker


class TestRanker:
    @pytest.fixture
    def ranker(self):
        return Ranker()

    def test_rerank_returns_scored(self, ranker):
        docs = [(1, "machine learning is fun"), (2, "I like cats")]
        results = ranker.rerank("machine learning", docs, top_k=5)
        assert len(results) == 2
        for doc_id, score in results:
            assert isinstance(doc_id, int)
            assert isinstance(score, float)

    def test_rerank_empty(self, ranker):
        assert ranker.rerank("test", []) == []

    def test_rerank_top_k(self, ranker):
        docs = [(i, f"document number {i}") for i in range(10)]
        results = ranker.rerank("document", docs, top_k=3)
        assert len(results) <= 3
