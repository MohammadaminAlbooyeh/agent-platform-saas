import pytest
from backend.nlp.intent_classifier import IntentClassifier


class TestIntentClassifier:
    @pytest.fixture
    def classifier(self):
        return IntentClassifier()

    def test_classify_search(self, classifier):
        assert classifier.classify("find me documents about AI") == "search"
        assert classifier.classify("search for machine learning") == "search"
        assert classifier.classify("show results for transformers") == "search"

    def test_classify_question(self, classifier):
        assert classifier.classify("what is deep learning") == "question"
        assert classifier.classify("how does BERT work") == "question"
        assert classifier.classify("explain attention mechanism") == "question"

    def test_classify_compare(self, classifier):
        assert classifier.classify("compare CNN and RNN") == "compare"
        assert classifier.classify("difference between SVM and neural networks") == "compare"

    def test_classify_define(self, classifier):
        assert classifier.classify("define gradient descent") == "define"
        assert classifier.classify("definition of transformer") == "define"

    def test_classify_empty_query(self, classifier):
        assert classifier.classify("") == "search"

    def test_classify_fallback(self, classifier):
        assert classifier.classify("xyzzy", fallback="question") == "question"

    def test_classify_batch(self, classifier):
        queries = ["find AI", "what is ML", "xyzzy"]
        results = classifier.classify_batch(queries)
        assert results == ["search", "question", "search"]

    def test_case_insensitive(self, classifier):
        assert classifier.classify("SEARCH FOR AI") == "search"
        assert classifier.classify("WHAT IS ML") == "question"
