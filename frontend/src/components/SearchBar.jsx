import { useState } from 'react';
import { TextField, IconButton, Switch, FormControlLabel, Box } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

export default function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('');
  const [useRerank, setUseRerank] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim(), useRerank);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Search documents using neural search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={loading}
        size="small"
        sx={{ flex: 1, minWidth: 300 }}
      />
      <IconButton type="submit" color="primary" disabled={loading || !query.trim()}>
        <SearchIcon />
      </IconButton>
      <FormControlLabel
        control={<Switch checked={useRerank} onChange={(e) => setUseRerank(e.target.checked)} size="small" />}
        label="Rerank"
      />
    </Box>
  );
}
