"""Unified CLI for the R129 Technical Data Repository."""

import argparse
import sys

from rich.console import Console

console = Console()


def main():
    parser = argparse.ArgumentParser(
        prog="r129",
        description="R129 Technical Data Repository -- search, ingest, and query tools",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # download-pdfs
    dl = subparsers.add_parser("download-pdfs", help="Download BenzWorld R129 PDF collection")
    dl.add_argument("--output", type=str, default=None, help="Output directory")

    # triage-pdfs
    subparsers.add_parser("triage-pdfs", help="AI-classify PDFs for applicability before ingestion")

    # ingest-pdfs
    ing = subparsers.add_parser("ingest-pdfs", help="Ingest PDFs into searchable JSONL chunks")
    ing.add_argument("--pdf-dir", type=str, default=None, help="Directory containing PDFs")
    ing.add_argument("--no-gemini", action="store_true", help="Skip Gemini image transcription")
    ing.add_argument("--limit", type=int, default=None, help="Max number of PDFs to ingest")
    ing.add_argument("--force", action="store_true", help="Re-ingest even if already done")

    # build-embeddings
    subparsers.add_parser("build-embeddings", help="Generate embedding vectors for all chunks")

    # search-docs
    sd = subparsers.add_parser("search-docs", help="Semantic search over ingested documents")
    sd.add_argument("query", nargs="+", help="Search query")
    sd.add_argument("-k", "--top-k", type=int, default=5, help="Number of results")

    # forum-search
    fs = subparsers.add_parser("forum-search", help="Search R129 forums via Google + Gemini")
    fs.add_argument("query", nargs="+", help="Search query")
    fs.add_argument("--save", action="store_true", help="Save findings to known_issues.yaml")

    # search
    s = subparsers.add_parser("search", help="Search local YAML data")
    s.add_argument("query", nargs="*", help="Search query")
    s.add_argument("--fuse", type=str, help="Look up a specific fuse (e.g., F14)")
    s.add_argument("--system", type=str, help="Filter by system (e.g., ads, lighting)")
    s.add_argument("--field", type=str, help="Filter results to items containing this field")

    # validate
    subparsers.add_parser("validate", help="Validate all YAML data files")

    # audit
    au = subparsers.add_parser("audit", help="Audit data quality")
    au.add_argument("--low-confidence", action="store_true", help="Show low-confidence entries")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "download-pdfs":
        from r129_data.src.pdf_downloader import run_download
        from pathlib import Path
        output = Path(args.output) if args.output else None
        run_download(output)

    elif args.command == "triage-pdfs":
        from r129_data.src.pdf_triage import run_triage
        run_triage()

    elif args.command == "ingest-pdfs":
        from r129_data.src.pdf_ingest import run_ingest
        from pathlib import Path
        pdf_dir = Path(args.pdf_dir) if args.pdf_dir else None
        run_ingest(pdf_dir, use_gemini=not args.no_gemini, limit=args.limit, force=args.force)

        if not args.limit:
            console.print("\n[bold]Rebuilding embeddings...[/bold]")
            from r129_data.src.pdf_search import run_build_embeddings
            run_build_embeddings()

    elif args.command == "build-embeddings":
        from r129_data.src.pdf_search import run_build_embeddings
        run_build_embeddings()

    elif args.command == "search-docs":
        from r129_data.src.pdf_search import run_search
        query = " ".join(args.query)
        run_search(query, top_k=args.top_k)

    elif args.command == "forum-search":
        from r129_data.src.forum_search import run_forum_search
        query = " ".join(args.query)
        run_forum_search(query, save=args.save)

    elif args.command == "search":
        from r129_data.src.search import run_search
        query = " ".join(args.query) if args.query else ""
        run_search(query, fuse=args.fuse, system=args.system, field=args.field)

    elif args.command == "validate":
        from r129_data.src.loader import validate_all
        issues = validate_all()
        if issues:
            console.print(f"[bold yellow]Found {len(issues)} issue(s):[/bold yellow]\n")
            for issue in issues:
                console.print(f"  [yellow]- {issue}[/yellow]")
        else:
            console.print("[bold green]All data files valid.[/bold green]")

    elif args.command == "audit":
        from r129_data.src.loader import validate_all
        issues = validate_all()
        if args.low_confidence:
            issues = [i for i in issues if "low confidence" in i.lower() or "tbd" in i.lower()]
        if issues:
            console.print(f"[bold]Audit results ({len(issues)} item(s)):[/bold]\n")
            for issue in issues:
                console.print(f"  - {issue}")
        else:
            console.print("[green]No audit issues found.[/green]")


if __name__ == "__main__":
    main()
