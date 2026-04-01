"""AI-assisted triage of downloaded PDFs before ingestion.

Reads first 2 pages of each PDF, sends to Gemini for applicability
classification against the owner's vehicle, and generates a curation
YAML for human review.
"""

import os
import time
import yaml
import fitz
from pathlib import Path

from rich.console import Console

console = Console()

PDFS_DIR = Path(__file__).parent.parent / "references" / "pdfs"
CURATION_FILE = Path(__file__).parent.parent / "references" / "curation.yaml"
VEHICLE_FILE = Path(__file__).parent.parent / "data" / "vehicle.yaml"
GEMINI_DELAY = 1.0


def load_vehicle_context() -> str:
    if VEHICLE_FILE.exists():
        with open(VEHICLE_FILE) as f:
            v = yaml.safe_load(f)
        return (
            f"{v.get('model_year', '?')} {v.get('model', '?')}, "
            f"chassis {v.get('chassis_code', '?')}, "
            f"engine {v.get('engine_code', '?')} ({v.get('engine_description', '?')}), "
            f"fuel system {v.get('fuel_system', '?')}, "
            f"transmission {v.get('transmission_code', '?')}, "
            f"key systems: {', '.join(v.get('key_systems', []))}"
        )
    return "1991 Mercedes-Benz 500 SL (R129)"


def extract_first_pages(pdf_path: Path, max_pages: int = 2) -> str:
    doc = fitz.open(str(pdf_path))
    text = ""
    for i in range(min(max_pages, len(doc))):
        text += doc[i].get_text()
    page_count = len(doc)
    doc.close()
    return text[:4000], page_count


def classify_with_gemini(client, filename: str, text_preview: str, vehicle_ctx: str) -> dict:
    prompt = f"""You are an expert on Mercedes-Benz R129 (1989-2001) model variations.
You must determine whether a document applies to this SPECIFIC vehicle:
{vehicle_ctx}

Document filename: {filename}
First pages content:
---
{text_preview[:3000]}
---

CRITICAL model-year differences (the owner has a 1991, early pre-facelift model):
- 1990-1992 ONLY: KE-Jetronic (CIS-E), EZL ignition, ROTARY climate control (no DTC via display), ADS I, 4-speed 722.3, no OBD
- 1993-1995: HFM fuel injection (M119.972), PB pushbutton climate with N22 DTC memory, ADS II, 5-speed 722.5
- 1996-1998: OBD-II, M119.982, updated electronics, ESP option
- 1999-2001: M113 V8 engine, completely different engine management
- UNIVERSAL (all years): roof/top mechanism, body panels, window lifts, seats, door trim, locks, general maintenance

Clues that a document does NOT apply to 1991:
- References to "N22 pushbutton control module" or DTC readout via climate display -> 1993+
- References to HFM, ME, or OBD-II diagnostics -> 1993+/1996+
- References to M113 engine -> 1999+
- References to "Hand-Held Tester" or STAR diagnostics for climate -> could be any year
- References to ESP -> 1996+

Respond in EXACTLY this YAML format (no markdown fencing, no explanation):
title: <concise document title>
system: <one of: roof, electrical, engine, climate, suspension, brakes, interior, body, wheels, audio, diagnostics, general, other>
description: <1-sentence summary>
applicability: <exact_match|likely_applicable|partially_applicable|wrong_model_year|wrong_engine|not_applicable|unknown>
applicability_reason: <1-sentence explanation>
model_years: <list of years this applies to>
priority: <high|medium|low>"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        result_text = response.text.strip()
        if result_text.startswith("```"):
            result_text = result_text.split("\n", 1)[1]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
        return yaml.safe_load(result_text)
    except Exception as e:
        return {
            "title": filename,
            "system": "unknown",
            "description": f"Classification failed: {e}",
            "applicability": "unknown",
            "applicability_reason": str(e)[:200],
            "model_years": [],
            "priority": "medium",
        }


def run_triage():
    """Generate curation.yaml by classifying all PDFs."""
    from google import genai
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        console.print("[red]Set GEMINI_API_KEY or GOOGLE_API_KEY[/red]")
        return

    client = genai.Client(api_key=api_key)
    vehicle_ctx = load_vehicle_context()

    pdfs = sorted(PDFS_DIR.glob("*.pdf"))
    console.print(f"[bold]PDF Triage: {len(pdfs)} documents to classify[/bold]")
    console.print(f"Vehicle: {vehicle_ctx}\n")

    existing = {}
    if CURATION_FILE.exists():
        with open(CURATION_FILE) as f:
            data = yaml.safe_load(f) or {}
        for entry in data.get("documents", []):
            existing[entry["filename"]] = entry
        console.print(f"[dim]Loaded {len(existing)} existing classifications[/dim]")

    results = []
    new_count = 0

    for idx, pdf_path in enumerate(pdfs):
        filename = pdf_path.name

        if filename in existing:
            results.append(existing[filename])
            console.print(f"  [{idx+1}/{len(pdfs)}] [dim]cached: {filename[:60]}[/dim]")
            continue

        text_preview, page_count = extract_first_pages(pdf_path)
        classification = classify_with_gemini(client, filename, text_preview, vehicle_ctx)

        appl = classification.get("applicability", "unknown")
        include = appl in ("exact_match", "likely_applicable", "partially_applicable")
        tag = "[green]INCL[/green]" if include else "[red]EXCL[/red]"

        entry = {
            "filename": filename,
            "pages": page_count,
            "size_kb": round(pdf_path.stat().st_size / 1024),
            **classification,
            "include": include,
        }
        results.append(entry)
        new_count += 1

        console.print(f"  [{idx+1}/{len(pdfs)}] {tag} {appl}: {filename[:55]}")
        time.sleep(GEMINI_DELAY)

    results.sort(key=lambda x: (not x.get("include", False), x.get("system", ""), x.get("filename", "")))

    curation = {
        "vehicle": vehicle_ctx,
        "total_documents": len(results),
        "auto_included": sum(1 for r in results if r.get("include")),
        "auto_excluded": sum(1 for r in results if not r.get("include")),
        "newly_classified": new_count,
        "instructions": (
            "Review each document below. Set 'include: true' to ingest, 'include: false' to skip. "
            "The AI classification is a starting point -- override as needed. "
            "Pay special attention to 'applicability: partially_applicable' entries."
        ),
        "documents": results,
    }

    with open(CURATION_FILE, "w") as f:
        yaml.dump(curation, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)

    console.print(f"\n[bold green]Triage complete![/bold green]")
    console.print(f"  Total: {len(results)}")
    console.print(f"  Auto-included: {curation['auto_included']}")
    console.print(f"  Auto-excluded: {curation['auto_excluded']}")
    console.print(f"  New classifications: {new_count}")
    console.print(f"\n[bold]Review and edit:[/bold] {CURATION_FILE}")
    console.print("[dim]Then run 'ingest-pdfs' which will respect the include/exclude flags.[/dim]")


if __name__ == "__main__":
    run_triage()
