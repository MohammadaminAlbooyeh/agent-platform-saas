import numpy as np
import pytest

from backend.search.embedding_generator import EmbeddingGenerator


@pytest.fixture(scope="module")
def generator():
    return EmbeddingGenerator(model_name="all-MiniLM-L6-v2")


class TestEmbeddingGenerator:
    def test_generate_returns_vector(self, generator):
        vec = generator.generate("test sentence")
        assert isinstance(vec, np.ndarray)
        assert vec.ndim == 1

    def test_generate_batch(self, generator):
        texts = ["hello world", "test sentence", "another one"]
        vecs = generator.generate_batch(texts)
        assert vecs.shape == (3, generator.dimension)

    def test_normalized_embeddings(self, generator):
        vec = generator.generate("hello world")
        norm = np.linalg.norm(vec)
        assert abs(norm - 1.0) < 1e-5

    def test_similar_sentences_close(self, generator):
        vec1 = generator.generate("I like cats")
        vec2 = generator.generate("I love cats")
        vec3 = generator.generate("quantum physics")
        sim_similar = np.dot(vec1, vec2)
        sim_different = np.dot(vec1, vec3)
        assert sim_similar > sim_different
