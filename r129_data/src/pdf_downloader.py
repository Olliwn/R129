"""Download all PDFs from the BenzWorld R129 PDF collection sticky thread.

Thread: https://www.benzworld.org/threads/all-of-the-r129-pdfs-i-have-collected-over-the-years.3099517/
The thread spans multiple pages with PDF attachments posted by community members.
"""

import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

THREAD_URL = "https://www.benzworld.org/threads/all-of-the-r129-pdfs-i-have-collected-over-the-years.3099517/"
MAX_PAGES = 10
DOWNLOAD_DELAY = 1.5
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) R129-DataRepo/1.0"

console = Console()


def get_thread_pages(session: requests.Session) -> list[str]:
    """Discover all page URLs for the thread."""
    resp = session.get(THREAD_URL, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    pages = [THREAD_URL]
    nav = soup.select("ul.pageNav-main li a")
    for link in nav:
        href = link.get("href", "")
        if href and "/page-" in href:
            full_url = requests.compat.urljoin(THREAD_URL, href)
            if full_url not in pages:
                pages.append(full_url)

    return sorted(set(pages))[:MAX_PAGES]


def extract_attachment_urls(session: requests.Session, page_url: str) -> list[tuple[str, str]]:
    """Extract (filename, url) pairs for PDF attachments from a thread page."""
    resp = session.get(page_url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    attachments = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/attachments/" in href and href.endswith("/"):
            full_url = requests.compat.urljoin(page_url, href)
            text = link.get_text(strip=True)
            if text and text.lower().endswith(".pdf"):
                filename = sanitize_filename(text)
                attachments.append((filename, full_url))

    return attachments


def sanitize_filename(name: str) -> str:
    """Clean up filename for filesystem safety."""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'\s+', ' ', name).strip()
    if len(name) > 200:
        name = name[:200]
    return name


def download_file(session: requests.Session, url: str, dest: Path) -> bool:
    """Download a file, return True on success."""
    try:
        resp = session.get(url, timeout=60, stream=True)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        console.print(f"  [red]Failed:[/red] {e}")
        return False


def run_download(output_dir: Path | None = None):
    """Main download orchestration."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "references" / "pdfs"
    output_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    console.print("[bold]BenzWorld R129 PDF Collection Downloader[/bold]\n")

    console.print("Discovering thread pages...")
    pages = get_thread_pages(session)
    console.print(f"Found {len(pages)} page(s)\n")
    time.sleep(DOWNLOAD_DELAY)

    all_attachments: list[tuple[str, str]] = []
    for page_url in pages:
        console.print(f"Scanning: {page_url}")
        attachments = extract_attachment_urls(session, page_url)
        all_attachments.extend(attachments)
        console.print(f"  Found {len(attachments)} PDF(s)")
        time.sleep(DOWNLOAD_DELAY)

    seen_urls = set()
    unique_attachments = []
    for filename, url in all_attachments:
        if url not in seen_urls:
            seen_urls.add(url)
            unique_attachments.append((filename, url))

    console.print(f"\n[bold]Total unique PDFs: {len(unique_attachments)}[/bold]\n")

    downloaded = 0
    skipped = 0
    failed = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Downloading...", total=len(unique_attachments))

        for filename, url in unique_attachments:
            dest = output_dir / filename
            if dest.exists():
                skipped += 1
                progress.update(task, advance=1, description=f"[dim]Skip: {filename[:50]}[/dim]")
            else:
                progress.update(task, advance=0, description=f"[cyan]{filename[:50]}[/cyan]")
                if download_file(session, url, dest):
                    downloaded += 1
                else:
                    failed += 1
                time.sleep(DOWNLOAD_DELAY)
                progress.update(task, advance=1)

    console.print(f"\n[green]Downloaded: {downloaded}[/green]")
    console.print(f"[dim]Skipped (already exists): {skipped}[/dim]")
    if failed:
        console.print(f"[red]Failed: {failed}[/red]")

    manifest_path = output_dir / "download_manifest.txt"
    with open(manifest_path, "w") as f:
        for filename, url in unique_attachments:
            f.write(f"{filename}\t{url}\n")
    console.print(f"\nManifest written to {manifest_path}")


if __name__ == "__main__":
    run_download()
