import typer
from rich import print
from seoextract import SEOExtract, __version__

app = typer.Typer()


@app.command()
def audit(
    url: str,
    max_pages: int = 20,
):
    """Run an AI-powered SEO audit."""

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

    print("\n[bold]Top Page Audits[/bold]")
    for audit_result in result.page_audits:
        print(f"\n[cyan]{audit_result['page_url']}[/cyan]")
        print(f"Score: {audit_result['page_score']}")
        print(f"Grade: {audit_result['grade']}")
        print(f"Summary: {audit_result['summary']}")


@app.command()
def version():
    """Show SEOExtract version."""
    print(__version__)


if __name__ == "__main__":
    app()