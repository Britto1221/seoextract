import typer
from rich import print

from seoextract import SEOExtract, __version__

app = typer.Typer()


@app.command()
def audit(url: str, max_pages: int = 20):
    """Run a rule-based SEO audit."""
    result = SEOExtract.audit(url=url, max_pages=max_pages)

    print("\n[bold green]SEO Audit Complete[/bold green]")
    print(f"URL: {result.url}")
    print(f"Pages crawled: {result.pages_crawled}")
    print(f"Site score: {result.site_score}")
    print(f"Grade: {result.grade}")
    print(f"Total issues: {result.total_issues}")
    print(f"Critical: {result.critical_count}")
    print(f"Warnings: {result.warning_count}")
    print(f"Info: {result.info_count}")

    if result.pages:
        print("\n[bold]Page Scores[/bold]")
        for page in result.pages:
            print(f"\n[cyan]{page.url}[/cyan]")
            print(f"Score: {page.page_score}")
            print(f"Status: {page.status_code}")
            print(f"Title: {page.title or 'N/A'}")

    if result.issues:
        print("\n[bold]Detected Issues[/bold]")
        for issue in result.issues[:20]:
            print(f"\n[yellow]{issue.issue_type.value}[/yellow]")
            print(f"Page: {issue.page_url}")
            print(f"Severity: {issue.severity.value}")
            if issue.current_value:
                print(f"Current value: {issue.current_value}")
            print(f"Fix: {issue.suggestion}")


@app.command()
def version():
    """Show SEOExtract version."""
    print(__version__)


if __name__ == "__main__":
    app()