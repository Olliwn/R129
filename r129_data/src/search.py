"""Local YAML data search with vehicle-specific filtering."""

import json
from pathlib import Path
from typing import Any

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from r129_data.src.loader import load_all_data, load_vehicle, load_doc_index, check_applies_to

console = Console()


def search_in_value(value: Any, query_terms: list[str]) -> bool:
    """Check if any query term appears in a value (recursive for nested structures)."""
    if isinstance(value, str):
        lower = value.lower()
        return any(term in lower for term in query_terms)
    elif isinstance(value, list):
        return any(search_in_value(item, query_terms) for item in value)
    elif isinstance(value, dict):
        return any(search_in_value(v, query_terms) for v in value.values())
    return False


def search_items(items: list[dict], query_terms: list[str], vehicle: dict) -> list[dict]:
    """Search a list of items, filtering by query and vehicle applicability."""
    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        applies_to = item.get("applies_to")
        if not check_applies_to(applies_to, vehicle):
            continue
        if search_in_value(item, query_terms):
            results.append(item)
    return results


def run_search(query: str, fuse: str | None = None, system: str | None = None,
               field: str | None = None, show_all: bool = False):
    """Main search across all YAML data files."""
    vehicle = load_vehicle()
    all_data = load_all_data()

    if not all_data:
        console.print("[yellow]No data files found. Populate r129_data/data/ first.[/yellow]")
        return

    if fuse:
        _search_fuse(fuse, all_data, vehicle)
        return

    query_terms = query.lower().split() if query else []
    if not query_terms and not system:
        console.print("[yellow]Provide a search query or --fuse/--system flag.[/yellow]")
        return

    console.print(f"[bold]Searching local data for:[/bold] {query}")
    if vehicle:
        year = vehicle.get("model_year", "?")
        chassis = vehicle.get("chassis_code", "?")
        console.print(f"[dim]Filtering for vehicle: {year} / {chassis}[/dim]\n")

    total_results = 0

    for file_key, content in all_data.items():
        if not isinstance(content, dict):
            continue

        if system:
            skip = True
            for value in _flatten_values(content):
                if isinstance(value, str) and system.lower() in value.lower():
                    skip = False
                    break
            if skip:
                continue

        for list_key, items in content.items():
            if not isinstance(items, list):
                continue

            matches = search_items(items, query_terms, vehicle)
            if field:
                matches = [m for m in matches if field in m]

            if matches:
                console.print(f"[bold cyan]{file_key}.yaml[/bold cyan] ({list_key}):")
                for match in matches:
                    _display_item(match, query_terms)
                    total_results += 1
                console.print()

    doc_index = load_doc_index()
    if doc_index and query_terms:
        doc_matches = [d for d in doc_index if search_in_value(d, query_terms)]
        if doc_matches:
            console.print(f"[bold cyan]Document Index[/bold cyan]:")
            for doc in doc_matches:
                title = doc.get("title", "?")
                topics = ", ".join(doc.get("topics", []))
                pages = doc.get("pages", "?")
                console.print(f"  [green]{doc.get('doc_id', '?')}[/green]: {title} ({pages} pages)")
                if topics:
                    console.print(f"    Topics: [dim]{topics}[/dim]")
                total_results += 1
            console.print()

    if total_results == 0:
        console.print("[yellow]No results found in local data.[/yellow]")
        console.print("[dim]Try: python -m r129_data forum-search \"your query\"[/dim]")
    else:
        console.print(f"[dim]{total_results} result(s) found[/dim]")


def _search_fuse(fuse_id: str, all_data: dict, vehicle: dict):
    """Direct fuse lookup."""
    fuse_data = all_data.get("fuse_box", {})
    fuses = fuse_data.get("fuses", [])

    for fuse in fuses:
        if not isinstance(fuse, dict):
            continue
        if fuse.get("id", "").upper() == fuse_id.upper():
            if not check_applies_to(fuse.get("applies_to"), vehicle):
                console.print(f"[yellow]Fuse {fuse_id} exists but does not apply to your vehicle.[/yellow]")
            _display_item(fuse, [fuse_id.lower()])
            return

    console.print(f"[yellow]Fuse {fuse_id} not found.[/yellow]")


def _display_item(item: dict, highlights: list[str]):
    """Pretty-print a data item."""
    item_id = item.get("id", item.get("doc_id", "?"))
    title = item.get("title", item.get("designation", item.get("system", "")))

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="dim", width=20)
    table.add_column("Value")

    skip_keys = {"source", "applies_to"}
    for key, value in item.items():
        if key in skip_keys:
            continue
        if isinstance(value, list):
            value_str = ", ".join(str(v) for v in value)
        elif isinstance(value, dict):
            value_str = yaml.dump(value, default_flow_style=True).strip()
        else:
            value_str = str(value)

        text = Text(value_str)
        for term in highlights:
            start = 0
            lower_value = value_str.lower()
            while True:
                idx = lower_value.find(term, start)
                if idx == -1:
                    break
                text.stylize("bold yellow", idx, idx + len(term))
                start = idx + 1

        table.add_row(key, text)

    source = item.get("source", {})
    if isinstance(source, dict):
        conf = source.get("confidence", "?")
        ref = source.get("ref", "?")
        conf_style = {"high": "green", "medium": "yellow", "low": "red"}.get(conf, "dim")
        table.add_row("source", Text(f"[{conf}] {ref}", style=conf_style))

    console.print(Panel(table, title=f"[bold]{item_id}[/bold] {title}", border_style="blue"))


def _flatten_values(obj: Any) -> list:
    """Recursively flatten all string values from a nested structure."""
    if isinstance(obj, str):
        return [obj]
    elif isinstance(obj, list):
        result = []
        for item in obj:
            result.extend(_flatten_values(item))
        return result
    elif isinstance(obj, dict):
        result = []
        for v in obj.values():
            result.extend(_flatten_values(v))
        return result
    return []
