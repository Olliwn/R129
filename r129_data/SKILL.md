---
name: r129-technical-data
description: >-
  Search the R129 Mercedes-Benz technical data repository for fuse assignments,
  wiring, fluid specs, torques, known issues, service procedures, and diagnostic
  information. Use when the user asks about their 1991 R129 500 SL (chassis
  129.066, M119.960, KE-Jetronic, ADS I) or needs technical reference data for
  repair, diagnostics, or maintenance.
---

# R129 Technical Data Repository

Technical knowledge base for a **1991 Mercedes-Benz 500 SL**: chassis 129.066,
engine M119.960 (5.0 L V8 32-valve DOHC), KE-Jetronic (CIS-E) fuel injection,
EZL ignition, 722.3 transmission, ADS I adaptive damping, PSE pneumatic locking.

## Data Sources

### 1. Structured YAML Data (exact lookups)

Files in `r129_data/data/`:

| File | Content |
|------|---------|
| `vehicle.yaml` | VIN, build spec, option codes |
| `fuse_box.yaml` | Fuse number, protected circuits, amp rating |
| `relay_box.yaml` | Relay designation, function, location |
| `fluids.yaml` | Fluid type, capacity, MB spec, change interval |
| `torques.yaml` | Torque values by system |
| `known_issues.yaml` | Common failures, cross-system dependencies |
| `service_intervals.yaml` | Maintenance schedule |
| `components.yaml` | Component part numbers and locations |
| `ground_points.yaml` | Chassis ground point locations |
| `variants.yaml` | All R129 model codes and production changes |

**Search method:** Grep `r129_data/data/` for keywords. Entries have `applies_to`
blocks with year ranges and chassis codes -- filter to 1991 / 129.066.

### 2. Ingested Service Documents (110 PDFs, 2435 chunks)

Factory workshop manuals, STAR TekInfo diagnostic guides, owner's handbooks,
and system-specific service literature ingested into searchable text.

#### Search Option A: Embedding-based semantic search (recommended for broad queries)

```bash
cd r129_data && source .venv/bin/activate
python -m r129_data search-docs "KE-Jetronic fuel pressure adjustment"
python -m r129_data search-docs "ADS I fault codes" -k 10
```

Requires the venv at `r129_data/.venv/` and a `GEMINI_API_KEY` env var.

#### Search Option B: Raw file search with Cursor tools (no Python needed)

The raw data is fully accessible with standard file tools (Grep, Read, Glob):

1. **Find relevant documents** -- Grep `r129_data/references/doc_index/` for topic keywords.
   Each YAML index file has `title`, `topics`, `toc`, and `applies_to`.
2. **Search chunk text** -- Grep `r129_data/references/chunks/all_chunks.jsonl` for
   specific terms. Each JSON line has:
   - `doc_id`: source document identifier
   - `page`: page number in the original PDF
   - `type`: `"text"` or `"image"`
   - `text`: extracted text content
   - `images[].transcription`: Gemini-generated descriptions of diagrams
3. **View source images** -- Referenced images are in `r129_data/references/images/`.

#### Search Option C: YAML data search

```bash
cd r129_data && source .venv/bin/activate
python -m r129_data search "query"
python -m r129_data search --fuse F6
python -m r129_data search --system ads
```

### 3. Document Curation

`r129_data/references/curation.yaml` contains metadata and applicability
classification for all 150 source PDFs (110 included, 40 excluded as
non-applicable to this specific build). Review this file to understand
which documents were ingested and why some were excluded.

### 4. Forum Search (live)

For questions not answered by local data:

```bash
python -m r129_data forum-search "soft top hydraulic pump replacement"
```

Queries BenzWorld/PeachParts via Google and summarizes with Gemini.

## CLI Reference

All commands run from the repo root:

```bash
cd r129_data && source .venv/bin/activate
python -m r129_data <command>
```

| Command | Purpose |
|---------|---------|
| `search-docs "query"` | Semantic search over ingested PDFs |
| `search "query"` | Keyword search over YAML data files |
| `search --fuse F14` | Look up a specific fuse |
| `search --system lighting` | Filter by vehicle system |
| `forum-search "query"` | Live forum search via Google + Gemini |
| `triage-pdfs` | AI-classify new PDFs for applicability |
| `ingest-pdfs` | Ingest PDFs into JSONL (auto-builds embeddings) |
| `ingest-pdfs --limit 5` | Ingest a batch of 5 PDFs |
| `build-embeddings` | Rebuild embedding vectors |
| `validate` | Validate YAML data files |
| `audit --low-confidence` | Show entries needing review |
