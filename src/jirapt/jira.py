"""Module with search interface."""
from typing import Dict, Iterable, Optional

from jira import JIRA, Issue
from jira.client import ResultList

from jirapt.jira_response_iterable import JiraResponseIterable, JiraResponseIterableParallel
from jirapt.jql_builder import JqlQueryBuilder


def search_issues(
    jira: JIRA, jql: str, n_threads: Optional[int] = None, **kwargs: Optional[Dict]
) -> Iterable[Issue]:
    """
    Lazily search for paginated jira issues.

    :param jira: Jira API instance.
    :param jql: JQL query to search.
    :param n_threads: Number of threads to use for execution.
    :param kwargs: Additional search_issues arguments.
    :return: Iterable of Jira issues found.
    """

    def get_more_fn(start_idx: int) -> ResultList:
        return jira.search_issues(jql, startAt=start_idx, **kwargs)

    if n_threads is not None:
        return JiraResponseIterableParallel(get_more_fn(0), get_more_fn, n_threads)
    return JiraResponseIterable(get_more_fn(0), get_more_fn)


def query_issues(
    jira: JIRA, query: Dict, n_threads: Optional[int] = None, **kwargs: Optional[Dict]
) -> Iterable[Issue]:
    """
    Lazily search for paginated jira issues using dictionary-based queries.

    :param jira: Jira API instance.
    :param query: Dictionary of query.
    :param n_threads: Number of threads to use for execution.
    :param kwargs: Additional search_issues arguments.
    :return: Iterable of Jira issues found.
    """
    jql_builder = JqlQueryBuilder()
    jql = jql_builder.build(query)

    return search_issues(jira, jql, n_threads, **kwargs)
