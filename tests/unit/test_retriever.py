import numpy as np
import pytest
from unittest.mock import Mock

from backend.search.retriever import Retriever


class TestRetriever:
    @pytest.fixture
    def emb_gen(self):
        mock = Mock()
        mock.generate.return_value = np.zeros(384)
        return mock

    @pytest.fixture
    def vec_store(self):
        mock = Mock()
        mock.search.return_value = ([1, 2, 3], [0.9, 0.8, 0.7])
        return mock

    def test_retrieve_returns_ids_and_scores(self, emb_gen, vec_store):
        retriever = Retriever(emb_gen, vec_store)
        ids, scores = retriever.retrieve("test query", top_k=10)
        assert ids == [1, 2, 3]
        assert scores == [0.9, 0.8, 0.7]

    def test_calls_generate(self, emb_gen, vec_store):
        retriever = Retriever(emb_gen, vec_store)
        retriever.retrieve("hello world")
        emb_gen.generate.assert_called_once_with("hello world")
