import { Box, Chip, Typography } from '@mui/material';

const INTENTS = ['search', 'question', 'compare', 'define'];

export default function FilterPanel({ selectedIntent, onIntentChange, resultCount }) {
  return (
    <Box sx={{ mb: 2 }}>
      <Typography variant="caption" color="text.secondary" sx={{ mr: 1 }}>
        Intent Filter:
      </Typography>
      {INTENTS.map((intent) => (
        <Chip
          key={intent}
          label={intent}
          size="small"
          variant={selectedIntent === intent ? 'filled' : 'outlined'}
          color={selectedIntent === intent ? 'secondary' : 'default'}
          onClick={() => onIntentChange(selectedIntent === intent ? null : intent)}
          sx={{ mr: 0.5, mb: 0.5 }}
        />
      ))}
      {resultCount != null && (
        <Typography variant="caption" color="text.secondary" sx={{ ml: 2 }}>
          {resultCount} result{resultCount !== 1 ? 's' : ''}
        </Typography>
      )}
    </Box>
  );
}
