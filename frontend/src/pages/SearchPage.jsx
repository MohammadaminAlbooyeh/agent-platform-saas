import { useState, useCallback } from 'react';
import { Container, Typography, Box, Alert, CircularProgress } from '@mui/material';
import SearchBar from '../components/SearchBar';
import ResultCard from '../components/ResultCard';
import FilterPanel from '../components/FilterPanel';
import { searchDocuments } from '../services/search_api';

const INTENT_KEYWORDS = {
  search: ['find', 'search', 'look', 'get', 'show', 'list', 'retrieve', 'locate', 'result', 'match', 'document'],
  question: ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'explain', 'describe', 'tell', 'meaning'],
  compare: ['compare', 'vs', 'versus', 'difference', 'better', 'worse', 'similar', 'advantage', 'disadvantage', 'than', 'instead'],
  define: ['define', 'definition', 'meaning', 'terminology', 'glossary'],
};

function matchesIntent(text, intent) {
  const lower = text.toLowerCase();
  const keywords = INTENT_KEYWORDS[intent];
  if (!keywords) return true;
  return keywords.some(kw => lower.includes(kw));
}

export default function SearchPage() {
  const [results, setResults] = useState([]);
  const [intent, setIntent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedIntent, setSelectedIntent] = useState(null);
  const [lastQuery, setLastQuery] = useState('');

  const handleSearch = useCallback(async (query, useRerank) => {
    setLoading(true);
    setError(null);
    setLastQuery(query);
    try {
      const data = await searchDocuments(query, 10, useRerank);
      setResults(data.results);
      setIntent(data.intent);
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed. Is the backend running?');
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const filteredResults = selectedIntent
    ? results.filter(r => matchesIntent(r.title + ' ' + r.content, selectedIntent))
    : results;

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Neural Search Engine
      </Typography>
      <SearchBar onSearch={handleSearch} loading={loading} />
      {intent && (
        <Box sx={{ mt: 1 }}>
          <FilterPanel
            selectedIntent={selectedIntent}
            onIntentChange={setSelectedIntent}
            resultCount={filteredResults.length}
          />
        </Box>
      )}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      )}
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {!loading && !error && results.length > 0 && (
        <Box sx={{ mt: 2 }}>
          {filteredResults.map((r) => (
            <ResultCard key={r.id} result={r} />
          ))}
        </Box>
      )}
      {!loading && !error && results.length === 0 && !intent && (
        <Typography variant="body1" color="text.secondary" sx={{ mt: 4, textAlign: 'center' }}>
          Enter a query above to search your documents.
        </Typography>
      )}
    </Container>
  );
}
