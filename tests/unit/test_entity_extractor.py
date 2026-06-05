import pytest
from backend.nlp.entity_extractor import EntityExtractor


class TestEntityExtractor:
    @pytest.fixture
    def extractor(self):
        return EntityExtractor()

    def test_extract_email(self, extractor):
        result = extractor.extract("Contact me at test@example.com")
        assert "email" in result
        assert "test@example.com" in result["email"]

    def test_extract_url(self, extractor):
        result = extractor.extract("Visit https://example.com/page")
        assert "url" in result
        assert "https://example.com/page" in result["url"]

    def test_extract_phone(self, extractor):
        result = extractor.extract("Call +1-555-123-4567")
        assert "phone" in result

    def test_extract_date(self, extractor):
        result = extractor.extract("Date: 2024-01-15")
        assert "date" in result
        assert "2024-01-15" in result["date"]

    def test_extract_year(self, extractor):
        result = extractor.extract("Published in 2023")
        assert "year" in result
        assert "2023" in result["year"]

    def test_extract_currency(self, extractor):
        result = extractor.extract("Price: $49.99")
        assert "currency" in result

    def test_extract_person(self, extractor):
        result = extractor.extract("Dr. Smith presented")
        assert "person" in result

    def test_extract_no_entities(self, extractor):
        result = extractor.extract("just some plain text")
        assert result == {}

    def test_extract_batch(self, extractor):
        results = extractor.extract_batch(["hello@world.com", "plain text"])
        assert "email" in results[0]
        assert results[1] == {}
