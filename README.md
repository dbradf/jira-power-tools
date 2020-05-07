# jira power tools

A collection of tools to make it easier to work with the 
[Python Jira API](https://pypi.org/project/jira/).

## Usages

### Lazy Pagination of Jira Issues

If you are querying a lot of jira issues. Paginating the results can lighten the memory usage
on the Jira server. But needing to keep track of the pagination is painful. Using lazy pagination
gives you an iterable that can track pagination for you:

```python
import jirapt

jira = # jira server instance.
jql = "JQL query"

issues = jirapt.search_issues(jira, jql, ...) # you can include any parameters you might pass to search_issues.

for issue in issues:
    # perform work on issue

```
