import pytest
from backend.nlp.preprocessor import TextPreprocessor


class TestTextPreprocessor:
    def test_lowercase(self):
        p = TextPreprocessor(lowercase=True, remove_punctuation=False)
        assert p.clean("Hello World") == "hello world"

    def test_remove_punctuation(self):
        p = TextPreprocessor(lowercase=False, remove_punctuation=True)
        assert p.clean("hello, world!") == "hello world"

    def test_lowercase_and_punctuation(self):
        p = TextPreprocessor(lowercase=True, remove_punctuation=True)
        assert p.clean("Hello, World!") == "hello world"

    def test_remove_stop_words(self):
        p = TextPreprocessor(remove_stop_words=True)
        assert p.clean("the cat in the hat") == "cat hat"

    def test_normalize_unicode(self):
        p = TextPreprocessor(normalize_unicode=True)
        text = "café"
        result = p.clean(text)
        assert isinstance(result, str)

    def test_empty_string(self):
        p = TextPreprocessor()
        assert p.clean("") == ""

    def test_whitespace_collapsed(self):
        p = TextPreprocessor()
        assert p.clean("hello    world") == "hello world"

    def test_preprocess_alias(self):
        p = TextPreprocessor(lowercase=True, remove_punctuation=True)
        assert p.preprocess("Hello, World!") == "hello world"

    def test_preprocess_batch(self):
        p = TextPreprocessor(lowercase=True, remove_punctuation=True)
        result = p.preprocess_batch(["Hello!", "World."])
        assert result == ["hello", "world"]
