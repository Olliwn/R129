"""Embedding-based semantic search over ingested PDF chunks.

Uses gemini-embedding-001 to embed chunks and queries,
then cosine similarity for retrieval.
"""

import json
import os
from pathlib import Path

import numpy as np
from google.genai import types
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

DATA_DIR = Path(__file__).parent.parent
CHUNKS_FILE = DATA_DIR / "references" / "chunks" / "all_chunks.jsonl"
EMBEDDINGS_DIR = DATA_DIR / "references" / "embeddings"
EMBEDDINGS_FILE = EMBEDDINGS_DIR / "chunks.npz"
CHUNK_IDS_FILE = EMBEDDINGS_DIR / "chunk_ids.json"

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMS = 768
BATCH_SIZE = 20


def get_genai_client():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable")
    from google import genai
    return genai.Client(api_key=api_key)


def load_chunks() -> list[dict]:
    """Load all chunks from JSONL."""
    if not CHUNKS_FILE.exists():
        return []
    chunks = []
    with open(CHUNKS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def build_embeddings():
    """Generate embeddings for all chunks and save to disk."""
    client = get_genai_client()
    chunks = load_chunks()
    if not chunks:
        console.print("[red]No chunks found. Run 'ingest-pdfs' first.[/red]")
        return

    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold]Building embeddings for {len(chunks)} chunks[/bold]")

    texts = []
    chunk_ids = []
    for chunk in chunks:
        text = chunk.get("text", "")[:8000]
        if not text.strip():
            text = f"Document: {chunk.get('doc_title', 'unknown')}, page {chunk.get('page', 0)}"
        texts.append(text)
        chunk_ids.append(chunk["chunk_id"])

    all_embeddings = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        console.print(f"  Embedding batch {i // BATCH_SIZE + 1}/{(len(texts) + BATCH_SIZE - 1) // BATCH_SIZE}...")
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=EMBEDDING_DIMS,
            ),
        )
        for emb in result.embeddings:
            all_embeddings.append(emb.values)

    embeddings_array = np.array(all_embeddings, dtype=np.float32)
    np.savez_compressed(str(EMBEDDINGS_FILE), embeddings=embeddings_array)

    with open(CHUNK_IDS_FILE, "w") as f:
        json.dump(chunk_ids, f)

    console.print(f"[green]Saved {len(chunk_ids)} embeddings to {EMBEDDINGS_FILE}[/green]")


def search(query: str, top_k: int = 5) -> list[dict]:
    """Search chunks by embedding similarity. Returns top-K results with scores."""
    if not EMBEDDINGS_FILE.exists() or not CHUNK_IDS_FILE.exists():
        console.print("[yellow]No embeddings found. Run 'build-embeddings' first.[/yellow]")
        console.print("[yellow]Falling back to keyword search...[/yellow]")
        return keyword_search(query, top_k)

    client = get_genai_client()

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIMS,
        ),
    )
    query_embedding = np.array(result.embeddings[0].values, dtype=np.float32)

    data = np.load(str(EMBEDDINGS_FILE))
    embeddings = data["embeddings"]

    with open(CHUNK_IDS_FILE) as f:
        chunk_ids = json.load(f)

    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    normalized = embeddings / norms
    query_norm = query_embedding / (np.linalg.norm(query_embedding) or 1)
    similarities = normalized @ query_norm

    top_indices = np.argsort(similarities)[::-1][:top_k]

    chunks = load_chunks()
    chunk_map = {c["chunk_id"]: c for c in chunks}

    results = []
    for idx in top_indices:
        cid = chunk_ids[idx]
        score = float(similarities[idx])
        chunk = chunk_map.get(cid, {"chunk_id": cid})
        results.append({**chunk, "score": score})

    return results


def keyword_search(query: str, top_k: int = 5) -> list[dict]:
    """Simple keyword fallback when embeddings aren't available."""
    chunks = load_chunks()
    if not chunks:
        return []

    query_terms = query.lower().split()
    scored = []
    for chunk in chunks:
        text = chunk.get("text", "").lower()
        score = sum(1 for term in query_terms if term in text)
        if score > 0:
            scored.append({**chunk, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def display_results(results: list[dict], query: str):
    """Pretty-print search results."""
    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return

    console.print(f"\n[bold]Search results for:[/bold] {query}\n")

    for i, r in enumerate(results, 1):
        score = r.get("score", 0)
        doc_title = r.get("doc_title", "Unknown")
        page = r.get("page", "?")
        text = r.get("text", "")
        topics = r.get("topics", [])
        chunk_id = r.get("chunk_id", "")

        preview = text[:500].replace("\n", " ").strip()
        if len(text) > 500:
            preview += "..."

        header = Text(f"#{i} ", style="bold cyan")
        header.append(f"{doc_title}", style="bold")
        header.append(f" (p.{page})", style="dim")
        header.append(f"  score={score:.3f}", style="green")

        panel_text = Text(preview)
        if topics:
            panel_text.append(f"\n\nTopics: {', '.join(topics)}", style="dim italic")

        console.print(Panel(panel_text, title=header, subtitle=chunk_id, border_style="blue"))


def run_search(query: str, top_k: int = 5):
    """Main entry point for CLI search."""
    results = search(query, top_k=top_k)
    display_results(results, query)


def run_build_embeddings():
    """Main entry point for building embeddings."""
    build_embeddings()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_search(" ".join(sys.argv[1:]))
    else:
        print("Usage: python pdf_search.py <query>")
