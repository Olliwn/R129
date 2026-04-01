# R129 Technical Data Repository

Searchable reference data for a 1991 Mercedes-Benz 500 SL (R129), chassis 129.066, engine M119.960 (KE-Jetronic).

## Quick Start

```bash
cd r129_data
pip install -r requirements.txt

# Download BenzWorld R129 PDF collection
python -m r129_data download-pdfs

# Ingest PDFs into searchable chunks (requires GEMINI_API_KEY)
python -m r129_data ingest-pdfs

# Search ingested documents (embedding-based)
python -m r129_data search-docs "hydraulic pump soft top pressure"

# Search R129 forums via Google + Gemini
python -m r129_data forum-search "3rd brake light fuse dashboard"

# Search local structured data (YAML)
python -m r129_data search "headlight fuse"

# Validate all YAML data files
python -m r129_data validate
```

## Directory Layout

```
r129_data/
  data/                       Structured YAML reference data
    vehicle.yaml              This car's identity (VIN, build, options)
    variants.yaml             All R129 model/engine/year variants
    fuse_box.yaml             Fuse assignments and ratings
    relay_box.yaml            Relay assignments
    fluids.yaml               Fluid specs and capacities
    torques.yaml              Torque specs by system
    service_intervals.yaml    Maintenance schedule
    known_issues.yaml         Common problems and cross-system gotchas
    components.yaml           ECUs, modules, sensors (placeholder, needs ETM)
    ground_points.yaml        Ground locations (placeholder, needs ETM)

  references/
    pdfs/                     Raw downloaded PDFs
    chunks/                   Ingested JSONL (one JSON object per page)
    doc_index/                Per-document metadata YAML (topics, TOC)
    embeddings/               Numpy embedding vectors for search
    images/                   Extracted diagram images

  src/                        Python source
  tests/                      Schema validation tests
```

## Data Sources

| Source | Status | Content |
|--------|--------|---------|
| 1990 Owner's Manual | Available (Google Drive) | Fuse legend, fluid specs, basic specs |
| Engineering Diary | Available (docs/) | Vehicle-specific discoveries and measurements |
| Wikipedia R129 article | Available | Model codes, production changes, engine specs |
| BenzWorld PDF collection | Download via CLI | 60+ technical documents (roof, AC, seats, etc.) |
| R129 ETM (Electrical Troubleshooting Manual) | Not yet acquired | Complete wiring diagrams (Tier 2) |
| Mercedes EPC | Not yet acquired | Part numbers and exploded diagrams |

## Search Modes

- **`search-docs`** -- Semantic similarity over ingested PDF content. Best for natural language questions.
- **`forum-search`** -- Live Google search across R129 forums, summarized by Gemini. Best for questions not covered by local data.
- **`search`** -- Keyword + structured queries over local YAML. Best for exact lookups (fuse numbers, fluid specs).
- **Direct file access** -- All data is plain text (YAML/JSONL). Use grep, read, or any text tool directly.

## Environment Variables

- `GEMINI_API_KEY` -- Required for PDF ingestion (vision), embedding generation, and forum search.
