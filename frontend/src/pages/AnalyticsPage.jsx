import { useState, useEffect } from 'react';
import { Container, Typography, Card, CardContent, Box, Alert, CircularProgress, Button } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import { getAnalyticsStats, getIndexInfo, reindex } from '../services/search_api';

export default function AnalyticsPage() {
  const [stats, setStats] = useState(null);
  const [indexInfo, setIndexInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reindexing, setReindexing] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [s, i] = await Promise.all([getAnalyticsStats(), getIndexInfo()]);
      setStats(s);
      setIndexInfo(i);
    } catch (err) {
      setError('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  const handleReindex = async () => {
    setReindexing(true);
    try {
      await reindex();
      fetchData();
    } catch (err) {
      setError('Reindex failed');
    } finally {
      setReindexing(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4">Analytics</Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button variant="outlined" startIcon={<RefreshIcon />} onClick={fetchData} disabled={loading}>
            Refresh
          </Button>
          <Button variant="contained" onClick={handleReindex} disabled={reindexing}>
            {reindexing ? 'Reindexing...' : 'Reindex All'}
          </Button>
        </Box>
      </Box>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {loading && <CircularProgress />}
      {stats && (
        <Card variant="outlined" sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6">Document Stats</Typography>
            <Typography>Total Documents: {stats.total_documents}</Typography>
            {stats.latest_document_title && (
              <Typography>Latest: {stats.latest_document_title}</Typography>
            )}
          </CardContent>
        </Card>
      )}
      {indexInfo && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6">Index Info</Typography>
            <Typography>Name: {indexInfo.name}</Typography>
            <Typography>Model: {indexInfo.model_name}</Typography>
            <Typography>Dimension: {indexInfo.dimension}</Typography>
            <Typography>Indexed Documents: {indexInfo.num_documents}</Typography>
          </CardContent>
        </Card>
      )}
    </Container>
  );
}
