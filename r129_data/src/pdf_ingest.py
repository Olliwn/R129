"""Ingest downloaded PDFs into AI-friendly JSONL chunks.

Pipeline:
1. Extract text per page via pymupdf4llm (page_chunks=True)
2. Extract images via PyMuPDF
3. Transcribe significant images via Gemini vision API
4. Output: JSONL chunks + per-document metadata YAML in doc_index/
"""

import json
import os
import re
import time
from pathlib import Path

import fitz  # PyMuPDF
import pymupdf4llm
import yaml
from rich.console import Console

console = Console()

IMAGE_MIN_SIZE_BYTES = 5_000
IMAGE_MIN_DIMENSION = 100

DATA_DIR = Path(__file__).parent.parent


def make_doc_id(filename: str) -> str:
    """Convert a PDF filename to a clean doc_id slug."""
    stem = Path(filename).stem
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', stem).strip('_').lower()
    if len(slug) > 60:
        slug = slug[:60].rstrip('_')
    return slug


def extract_images_from_page(doc: fitz.Document, page_idx: int, output_dir: Path, doc_id: str) -> list[dict]:
    """Extract significant images from a PDF page, save to disk, return metadata."""
    page = doc[page_idx]
    images = []
    for img_idx, img_info in enumerate(page.get_images(full=True)):
        xref = img_info[0]
        try:
            base_image = doc.extract_image(xref)
        except Exception:
            continue

        img_bytes = base_image["image"]
        if len(img_bytes) < IMAGE_MIN_SIZE_BYTES:
            continue

        ext = base_image.get("ext", "png")
        width = base_image.get("width", 0)
        height = base_image.get("height", 0)
        if width < IMAGE_MIN_DIMENSION or height < IMAGE_MIN_DIMENSION:
            continue

        img_filename = f"{doc_id}_p{page_idx + 1:02d}_img{img_idx + 1}.{ext}"
        img_path = output_dir / img_filename
        with open(img_path, "wb") as f:
            f.write(img_bytes)

        images.append({
            "image_file": img_filename,
            "width": width,
            "height": height,
            "size_bytes": len(img_bytes),
            "transcription": "",
        })

    return images


TRANSCRIPTION_PROMPT = (
    "Describe this technical diagram or image from a Mercedes R129 service document. "
    "Include: component names, connections, measurements, part numbers, "
    "wire colors, and any text visible in the image. Be precise and complete. "
    "If this is not a technical diagram (e.g. a logo or decorative image), "
    "respond with just: 'Non-technical image'."
)

EXT_TO_MIME = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif"}

TRANSCRIPTION_WORKERS = 4


def _transcribe_one(client, img: dict, images_dir: Path, idx: int, total: int) -> dict:
    """Transcribe a single image with retries. Returns the updated img dict."""
    img_path = images_dir / img["image_file"]
    if not img_path.exists():
        return img

    img_bytes = img_path.read_bytes()
    ext = img_path.suffix.lstrip(".").lower()
    mime = EXT_TO_MIME.get(ext, "image/png")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[
                    TRANSCRIPTION_PROMPT,
                    {"inline_data": {"mime_type": mime, "data": img_bytes}},
                ],
            )
            img["transcription"] = response.text.strip()
            console.print(f"    [{idx + 1}/{total}] {img['image_file']}: {len(img['transcription'])} chars")
            return img
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait = (attempt + 1) * 15
                console.print(f"    [{idx + 1}/{total}] Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                console.print(f"    [{idx + 1}/{total}] [red]{img['image_file']}: {e}[/red]")
                img["transcription"] = f"[Transcription failed: {e}]"
                return img
    return img


def transcribe_images_with_gemini(images: list[dict], images_dir: Path) -> list[dict]:
    """Transcribe images in parallel using a thread pool."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        console.print("[yellow]No GEMINI_API_KEY/GOOGLE_API_KEY set -- skipping image transcription[/yellow]")
        return images

    try:
        from google import genai as genai_new
        client = genai_new.Client(api_key=api_key)
    except Exception as e:
        console.print(f"[yellow]Gemini init failed: {e} -- skipping image transcription[/yellow]")
        return images

    total = len(images)
    workers = min(TRANSCRIPTION_WORKERS, total)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_transcribe_one, client, img, images_dir, i, total): i
            for i, img in enumerate(images)
        }
        for future in as_completed(futures):
            future.result()

    return images


def infer_topics(filename: str, text: str) -> list[str]:
    """Infer topic tags from filename and content."""
    combined = (filename + " " + text[:2000]).lower()
    topic_keywords = {
        "roof": ["roof", "rst", "soft top", "convertible", "cabriolet", "tonneau"],
        "hydraulics": ["hydraulic", "pump", "cylinder", "valve", "zhm", "zh-m"],
        "roll_bar": ["roll bar", "rollbar", "roll-bar"],
        "lighting": ["headlight", "headlamp", "tail light", "bulb", "lamp", "fog light", "turn signal"],
        "wiring": ["wiring", "wire", "harness", "connector", "pin"],
        "electrical": ["fuse", "relay", "electrical", "circuit", "voltage"],
        "engine": ["engine", "m119", "m104", "m103", "m113", "m120", "spark plug", "coil", "ignition"],
        "transmission": ["transmission", "722", "gearbox", "atf"],
        "suspension": ["suspension", "ads", "damping", "spring", "shock", "accumulator"],
        "brakes": ["brake", "abs", "caliper", "rotor", "pad"],
        "climate": ["climate", "hvac", "a/c", "air conditioning", "heater", "blower"],
        "seats": ["seat", "lumbar", "orthopedic", "headrest", "head rest"],
        "doors": ["door", "window", "regulator", "handle", "lock", "latch"],
        "body": ["bumper", "fender", "hood", "trunk", "molding", "moulding", "pillar"],
        "wheels": ["wheel", "tire", "rim", "alloy"],
        "audio": ["radio", "speaker", "bose", "antenna", "loudspeaker"],
        "instrument_cluster": ["instrument cluster", "cluster", "gauge", "odometer", "speedometer"],
        "central_locking": ["central locking", "pse", "pneumatic", "remote", "infrared", "irc"],
        "steering": ["steering", "power steering"],
        "diagnostics": ["fault code", "dtc", "trouble code", "diagnostic"],
    }

    found = []
    for topic, keywords in topic_keywords.items():
        if any(kw in combined for kw in keywords):
            found.append(topic)
    return found or ["general"]


def estimate_tokens(text: str) -> int:
    """Rough token estimate (1 token ~ 4 chars for English)."""
    return len(text) // 4


def ingest_pdf(pdf_path: Path, chunks_dir: Path, images_dir: Path, doc_index_dir: Path,
               use_gemini: bool = True) -> tuple[str, int]:
    """Ingest a single PDF. Returns (doc_id, chunk_count)."""
    doc_id = make_doc_id(pdf_path.name)
    source_url = ""

    manifest_path = pdf_path.parent / "download_manifest.txt"
    if manifest_path.exists():
        with open(manifest_path) as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) == 2 and parts[0] == pdf_path.name:
                    source_url = parts[1]
                    break

    doc = fitz.open(str(pdf_path))
    page_count = len(doc)

    try:
        md_chunks = pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)
    except Exception as e:
        console.print(f"[yellow]pymupdf4llm failed for {pdf_path.name}: {e}[/yellow]")
        md_chunks = []
        for i in range(page_count):
            text = doc[i].get_text("text")
            md_chunks.append({"metadata": {"page": i + 1}, "text": text})

    all_page_images: dict[int, list[dict]] = {}
    for page_idx in range(page_count):
        imgs = extract_images_from_page(doc, page_idx, images_dir, doc_id)
        if imgs:
            all_page_images[page_idx] = imgs

    if use_gemini:
        all_images_flat = [img for imgs in all_page_images.values() for img in imgs]
        if all_images_flat:
            console.print(f"  Transcribing {len(all_images_flat)} image(s) with Gemini...")
            transcribe_images_with_gemini(all_images_flat, images_dir)

    doc.close()

    topics_from_filename = infer_topics(pdf_path.name, "")
    toc_entries = []
    chunks_written = 0

    chunks_file = chunks_dir / "all_chunks.jsonl"

    # Remove any existing chunks for this doc_id before appending
    if chunks_file.exists():
        existing = []
        with open(chunks_file) as rf:
            for line in rf:
                line = line.strip()
                if line:
                    c = json.loads(line)
                    if c.get("doc_id") != doc_id:
                        existing.append(line)
        with open(chunks_file, "w") as wf:
            for line in existing:
                wf.write(line + "\n")

    with open(chunks_file, "a") as f:
        for chunk_data in md_chunks:
            if isinstance(chunk_data, dict):
                text = chunk_data.get("text", "")
                meta = chunk_data.get("metadata", {})
                page_num = meta.get("page", chunks_written + 1)
            else:
                text = str(chunk_data)
                page_num = chunks_written + 1

            page_idx = page_num - 1
            page_images = all_page_images.get(page_idx, [])

            combined_text = text
            for img in page_images:
                if img["transcription"] and "Non-technical image" not in img["transcription"]:
                    combined_text += f"\n\n[Image: {img['image_file']}]\n{img['transcription']}"

            topics = infer_topics(pdf_path.name, combined_text)

            heading = ""
            for line in text.split("\n"):
                stripped = line.strip()
                if stripped and len(stripped) > 3 and not stripped.startswith("|"):
                    heading = stripped[:100]
                    break
            if heading and page_num <= 5:
                toc_entries.append({"page": page_num, "heading": heading})

            chunk = {
                "chunk_id": f"{doc_id}_p{page_num:02d}",
                "doc_id": doc_id,
                "doc_title": pdf_path.stem,
                "page": page_num,
                "text": combined_text.strip(),
                "images": [
                    {"image_file": img["image_file"], "transcription": img["transcription"]}
                    for img in page_images
                ],
                "source_url": source_url,
                "topics": topics,
                "token_count": estimate_tokens(combined_text),
            }

            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
            chunks_written += 1

    all_topics = set(topics_from_filename)
    for chunk_data in md_chunks:
        if isinstance(chunk_data, dict):
            text = chunk_data.get("text", "")
        else:
            text = str(chunk_data)
        all_topics.update(infer_topics(pdf_path.name, text))

    doc_meta = {
        "doc_id": doc_id,
        "title": pdf_path.stem,
        "filename": pdf_path.name,
        "source_url": source_url,
        "pages": page_count,
        "topics": sorted(all_topics),
        "toc": toc_entries[:20],
        "applies_to": {"years": [1989, 2001], "chassis": "all"},
        "quality": "medium",
    }

    doc_index_path = doc_index_dir / f"{doc_id}.yaml"
    with open(doc_index_path, "w") as f:
        yaml.dump(doc_meta, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return doc_id, chunks_written


def load_curation(pdf_dir: Path) -> dict[str, bool] | None:
    """Load curation.yaml and return {filename: include} map, or None if no curation file."""
    curation_path = pdf_dir.parent / "curation.yaml"
    if not curation_path.exists():
        return None
    with open(curation_path) as f:
        data = yaml.safe_load(f) or {}
    return {d["filename"]: d.get("include", False) for d in data.get("documents", [])}


def get_already_ingested(chunks_dir: Path) -> set[str]:
    """Return set of doc_ids already present in the JSONL."""
    chunks_file = chunks_dir / "all_chunks.jsonl"
    if not chunks_file.exists():
        return set()
    doc_ids = set()
    with open(chunks_file) as f:
        for line in f:
            line = line.strip()
            if line:
                doc_ids.add(json.loads(line).get("doc_id", ""))
    return doc_ids


def run_ingest(pdf_dir: Path | None = None, use_gemini: bool = True,
               limit: int | None = None, force: bool = False):
    """Ingest PDFs respecting curation.yaml and skipping already-ingested docs."""
    base = DATA_DIR
    if pdf_dir is None:
        pdf_dir = base / "references" / "pdfs"

    chunks_dir = base / "references" / "chunks"
    images_dir = base / "references" / "images"
    doc_index_dir = base / "references" / "doc_index"

    for d in [chunks_dir, images_dir, doc_index_dir]:
        d.mkdir(parents=True, exist_ok=True)

    curation = load_curation(pdf_dir)
    all_pdfs = sorted(pdf_dir.glob("*.pdf"))

    if curation is not None:
        included = [p for p in all_pdfs if curation.get(p.name, False)]
        excluded = len(all_pdfs) - len(included)
        console.print(f"[bold]R129 PDF Ingestion Pipeline[/bold]")
        console.print(f"Curation: {len(included)} included, {excluded} excluded out of {len(all_pdfs)} PDFs")
    else:
        included = all_pdfs
        console.print(f"[bold]R129 PDF Ingestion Pipeline[/bold]")
        console.print(f"No curation.yaml found -- ingesting all {len(included)} PDFs")

    if not force:
        already_done = get_already_ingested(chunks_dir)
        pending = []
        for p in included:
            doc_id = make_doc_id(p.name)
            if doc_id in already_done:
                console.print(f"  [dim]skip (already ingested): {p.name[:60]}[/dim]")
            else:
                pending.append(p)
        console.print(f"Already ingested: {len(included) - len(pending)}, pending: {len(pending)}")
    else:
        pending = included
        console.print(f"Force mode: re-ingesting all {len(pending)} documents")

    if limit is not None:
        pending = pending[:limit]
        console.print(f"Limit: processing first {limit} document(s)")

    if not pending:
        console.print("[green]Nothing to ingest.[/green]")
        return

    console.print()

    total_chunks = 0
    for idx, pdf_path in enumerate(pending):
        console.print(f"[{idx+1}/{len(pending)}] [cyan]{pdf_path.name}[/cyan]")
        try:
            doc_id, chunk_count = ingest_pdf(
                pdf_path, chunks_dir, images_dir, doc_index_dir, use_gemini=use_gemini
            )
            total_chunks += chunk_count
            console.print(f"  -> {chunk_count} chunks")
        except Exception as e:
            console.print(f"  [red]FAILED: {e}[/red]")

    console.print(f"\n[bold green]Done![/bold green] {len(pending)} PDFs -> {total_chunks} chunks")
    console.print(f"Chunks: {chunks_dir / 'all_chunks.jsonl'}")
    console.print(f"Doc index: {doc_index_dir}")
    console.print(f"Images: {images_dir}")


if __name__ == "__main__":
    run_ingest()
