"""Forum search via Google + Gemini.

Searches R129-specific forums using Google, fetches result pages,
and uses Gemini to extract and summarize technical findings.
"""

import os
import time
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

DATA_DIR = Path(__file__).parent.parent
VEHICLE_FILE = DATA_DIR / "data" / "vehicle.yaml"

FORUM_SITES = [
    "benzworld.org/forums/r129-sl-class",
    "peachparts.com/shopforum/mercedes-benz-sl-discussion-forum",
    "mbworld.org/forums",
]

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) R129-DataRepo/1.0"
FETCH_DELAY = 1.0
MAX_RESULTS = 7
MAX_CONTENT_PER_PAGE = 6000


def load_vehicle_context() -> str:
    """Load vehicle identity for Gemini context."""
    if VEHICLE_FILE.exists():
        with open(VEHICLE_FILE) as f:
            vehicle = yaml.safe_load(f)
        return (
            f"{vehicle.get('model_year', 1991)} {vehicle.get('model', 'Mercedes-Benz 500 SL')} "
            f"(chassis {vehicle.get('chassis_code', '129.066')}, "
            f"engine {vehicle.get('engine_code', 'M119.960')}, "
            f"{vehicle.get('fuel_system', 'KE-Jetronic')})"
        )
    return "1991 Mercedes-Benz 500 SL (chassis 129.066, engine M119.960, KE-Jetronic, ADS I)"


def google_search(query: str, num_results: int = MAX_RESULTS) -> list[dict]:
    """Search Google with site restrictions for R129 forums."""
    try:
        from googlesearch import search as gsearch
    except ImportError:
        console.print("[red]googlesearch-python not installed[/red]")
        return []

    site_query = " OR ".join(f"site:{site}" for site in FORUM_SITES)
    full_query = f"R129 {query} ({site_query})"

    results = []
    try:
        for url in gsearch(full_query, num_results=num_results, lang="en"):
            results.append({"url": url})
    except Exception as e:
        console.print(f"[yellow]Google search error: {e}[/yellow]")

    return results


def fetch_page_text(url: str) -> str:
    """Fetch a forum page and extract text content."""
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        posts = soup.select("article.message, .bbWrapper, .messageContent, .postBody")
        if posts:
            text = "\n\n---\n\n".join(p.get_text(separator="\n", strip=True) for p in posts)
        else:
            main = soup.select_one("main, .content, #content, .p-body")
            text = main.get_text(separator="\n", strip=True) if main else soup.get_text(separator="\n", strip=True)

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        text = "\n".join(lines)

        return text[:MAX_CONTENT_PER_PAGE]
    except Exception as e:
        return f"[Failed to fetch: {e}]"


def summarize_with_gemini(query: str, pages: list[dict], vehicle_context: str) -> str:
    """Send fetched forum content to Gemini for structured extraction."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "Error: Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable"

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return f"Error initializing Gemini: {e}"

    forum_content = ""
    for i, page in enumerate(pages, 1):
        forum_content += f"\n\n=== Source {i}: {page['url']} ===\n{page.get('text', '[No content]')}\n"

    prompt = f"""You are an R129 Mercedes-Benz technical expert. The user owns a {vehicle_context}.

Given these forum posts about "{query}", extract:

1. **Confirmed Technical Facts** -- specific, actionable information. Cite which source URL.
2. **Applicability** -- does each fact apply to the user's specific model year and engine? Flag differences.
3. **Part Numbers** -- any Mercedes or aftermarket part numbers mentioned.
4. **Diagnostic Steps** -- recommended troubleshooting procedures in order.
5. **Confidence** -- rate each finding as HIGH (multiple sources agree), MEDIUM (single credible source), or LOW (anecdotal/uncertain).

Format your response as a clear, structured summary. Use markdown headings and bullet points.
If the forum posts don't contain useful information about the query, say so clearly.

--- Forum Content ---
{forum_content}"""

    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text
    except Exception as e:
        return f"Gemini error: {e}"


def run_forum_search(query: str, save: bool = False):
    """Main forum search pipeline."""
    console.print(f"[bold]Forum Search:[/bold] {query}\n")

    vehicle_context = load_vehicle_context()
    console.print(f"[dim]Vehicle: {vehicle_context}[/dim]\n")

    console.print("Searching Google...")
    results = google_search(query)

    if not results:
        console.print("[yellow]No forum results found.[/yellow]")
        return

    console.print(f"Found {len(results)} result(s). Fetching content...\n")

    for i, result in enumerate(results):
        console.print(f"  [{i + 1}] {result['url']}")
        result["text"] = fetch_page_text(result["url"])
        time.sleep(FETCH_DELAY)

    console.print("\nSummarizing with Gemini...\n")
    summary = summarize_with_gemini(query, results, vehicle_context)

    console.print(Panel(summary, title="[bold cyan]Forum Search Results[/bold cyan]", border_style="cyan"))

    console.print("\n[dim]Sources:[/dim]")
    for i, result in enumerate(results, 1):
        console.print(f"  [{i}] {result['url']}")

    if save:
        save_to_known_issues(query, summary, results)


def save_to_known_issues(query: str, summary: str, results: list[dict]):
    """Append forum findings to known_issues.yaml."""
    issues_file = DATA_DIR / "data" / "known_issues.yaml"

    if issues_file.exists():
        with open(issues_file) as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}

    if "known_issues" not in data:
        data["known_issues"] = []

    import re
    issue_id = re.sub(r'[^a-z0-9]+', '_', query.lower()).strip('_')[:50]
    existing_ids = {i.get("id") for i in data["known_issues"]}
    if issue_id in existing_ids:
        issue_id += f"_{len(data['known_issues'])}"

    source_urls = [r["url"] for r in results]

    new_issue = {
        "id": issue_id,
        "title": query,
        "severity": "medium",
        "description": summary[:2000],
        "affected_systems": [],
        "symptoms": [],
        "diagnostic_hint": f"See forum search results for '{query}'",
        "applies_to": {"years": [1989, 2001], "chassis": "all"},
        "source": {
            "type": "community",
            "ref": "; ".join(source_urls[:3]),
            "confidence": "medium",
        },
    }

    data["known_issues"].append(new_issue)

    with open(issues_file, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    console.print(f"\n[green]Saved to {issues_file} as '{issue_id}'[/green]")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_forum_search(" ".join(sys.argv[1:]))
    else:
        print("Usage: python forum_search.py <query>")
