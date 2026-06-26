from seoextract import SEOExtract

result = SEOExtract.audit(
    "https://example.com"
)

print("Site Score:", result.site_score)
print("Grade:", result.grade)
print("Pages Crawled:", result.pages_crawled)
print("Total Issues:", result.total_issues)
print("Safe Browsing:", result.safe_browsing.is_safe)

print("\nIssues:")
for issue in result.issues:
    print(f"- [{issue.severity}] {issue.issue_type}")