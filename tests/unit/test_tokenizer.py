import pytest
from backend.nlp.tokenizer import Tokenizer


class TestTokenizer:
    @pytest.fixture
    def tokenizer(self):
        return Tokenizer()

    def test_tokenize_simple(self, tokenizer):
        assert tokenizer.tokenize("hello world") == ["hello", "world"]

    def test_tokenize_punctuation(self, tokenizer):
        assert tokenizer.tokenize("hello, world!") == ["hello", "world"]

    def test_tokenize_contractions(self, tokenizer):
        tokens = tokenizer.tokenize("don't can't it's")
        assert "do" in tokens
        assert "not" in tokens
        assert "cannot" in tokens
        assert "it" in tokens
        assert "is" in tokens

    def test_tokenize_empty(self, tokenizer):
        assert tokenizer.tokenize("") == []

    def test_tokenize_single_letter(self, tokenizer):
        result = tokenizer.tokenize("a b c")
        assert "a" in result
        assert "b" not in result
        assert "c" not in result

    def test_tokenize_case_insensitive(self, tokenizer):
        assert tokenizer.tokenize("Hello World") == ["hello", "world"]

    def test_tokenize_batch(self, tokenizer):
        results = tokenizer.tokenize_batch(["hello world", "foo bar"])
        assert results == [["hello", "world"], ["foo", "bar"]]
