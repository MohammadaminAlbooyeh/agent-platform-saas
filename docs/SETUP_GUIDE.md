# Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- pip / npm

## Backend Setup

```bash
# Clone and enter the project
cd neural_search_engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## Seed Sample Data

```bash
# From the project root with the virtualenv active
python -c "
import pandas as pd
from backend.models.database import init_db, SessionLocal
from backend.models.document import Document

init_db()
df = pd.read_csv('data/raw/documents.csv')
db = SessionLocal()
for _, row in df.iterrows():
    doc = Document(title=row['title'], content=row['content'], source=row.get('source',''), author=row.get('author',''))
    db.add(doc)
db.commit()
db.close()
print('Seeded', len(df), 'documents')
"
```

Then reindex:
```bash
curl -X POST http://localhost:8000/api/v1/index/reindex
```

## Docker

```bash
docker-compose up --build
```
