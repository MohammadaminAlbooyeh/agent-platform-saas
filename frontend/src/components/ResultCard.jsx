import { Card, CardContent, Typography, Chip, Box } from '@mui/material';

export default function ResultCard({ result }) {
  const scorePct = result.score != null ? (result.score * 100).toFixed(1) : null;

  return (
    <Card variant="outlined" sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {result.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          {result.content?.length > 300 ? result.content.slice(0, 300) + '...' : result.content}
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', alignItems: 'center' }}>
          {result.source && <Chip label={result.source} size="small" variant="outlined" />}
          {result.author && <Chip label={`By: ${result.author}`} size="small" variant="outlined" />}
          {scorePct && <Chip label={`Score: ${scorePct}%`} size="small" color="primary" />}
        </Box>
      </CardContent>
    </Card>
  );
}
