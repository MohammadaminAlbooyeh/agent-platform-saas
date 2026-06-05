import { useState, useEffect } from 'react';
import {
  Container, Typography, Button, Dialog, DialogTitle, DialogContent,
  DialogActions, TextField, Box, Card, CardContent, CardActions, IconButton,
  Alert, CircularProgress,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import AddIcon from '@mui/icons-material/Add';
import { getDocuments, createDocument, updateDocument, deleteDocument } from '../services/search_api';

const EMPTY_FORM = { title: '', content: '', source: '', author: '' };

export default function DocumentsPage() {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({ ...EMPTY_FORM });
  const [saving, setSaving] = useState(false);

  const fetchDocs = async () => {
    setLoading(true);
    try {
      const data = await getDocuments();
      setDocs(data);
    } catch (err) {
      setError('Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchDocs(); }, []);

  const openCreate = () => {
    setEditingId(null);
    setForm({ ...EMPTY_FORM });
    setDialogOpen(true);
  };

  const openEdit = (doc) => {
    setEditingId(doc.id);
    setForm({
      title: doc.title || '',
      content: doc.content || '',
      source: doc.source || '',
      author: doc.author || '',
    });
    setDialogOpen(true);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      if (editingId) {
        await updateDocument(editingId, form);
      } else {
        await createDocument(form);
      }
      setDialogOpen(false);
      fetchDocs();
    } catch (err) {
      setError(editingId ? 'Failed to update document' : 'Failed to create document');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteDocument(id);
      fetchDocs();
    } catch (err) {
      setError('Failed to delete document');
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4">Documents</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={openCreate}>
          Add Document
        </Button>
      </Box>
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}
      {loading && <CircularProgress />}
      {!loading && docs.map((doc) => (
        <Card key={doc.id} variant="outlined" sx={{ mb: 1 }}>
          <CardContent>
            <Typography variant="h6">{doc.title}</Typography>
            <Typography variant="body2" color="text.secondary">
              {doc.content?.slice(0, 200)}{doc.content?.length > 200 ? '...' : ''}
            </Typography>
            {(doc.source || doc.author) && (
              <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                {[doc.source && `Source: ${doc.source}`, doc.author && `Author: ${doc.author}`].filter(Boolean).join(' | ')}
              </Typography>
            )}
          </CardContent>
          <CardActions>
            <IconButton onClick={() => openEdit(doc)} color="primary" size="small">
              <EditIcon />
            </IconButton>
            <IconButton onClick={() => handleDelete(doc.id)} color="error" size="small">
              <DeleteIcon />
            </IconButton>
          </CardActions>
        </Card>
      ))}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingId ? 'Edit Document' : 'Add Document'}</DialogTitle>
        <DialogContent>
          <TextField label="Title" fullWidth margin="dense" value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })} />
          <TextField label="Content" fullWidth margin="dense" multiline rows={4} value={form.content}
            onChange={(e) => setForm({ ...form, content: e.target.value })} />
          <TextField label="Source" fullWidth margin="dense" value={form.source}
            onChange={(e) => setForm({ ...form, source: e.target.value })} />
          <TextField label="Author" fullWidth margin="dense" value={form.author}
            onChange={(e) => setForm({ ...form, author: e.target.value })} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSave} variant="contained" disabled={!form.title || !form.content || saving}>
            {saving ? 'Saving...' : editingId ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
