# credits: https://github.com/deependujha

import github
from github import Github

from prtracker.types import PRStatus, RepoPR


def pr_status(
    repo_pr: RepoPR,
    github_instance: Github,
) -> str:
    assert repo_pr.pr_number > 0, "PR number must be a positive integer."
    assert isinstance(github_instance, Github), "github_instance must be an instance of Github."

    repository = repo_pr.repository or f"{repo_pr.repo_org}/{repo_pr.repo_name}"

    try:
        repo = github_instance.get_repo(repository)
        pr = repo.get_pull(repo_pr.pr_number)
        commit = repo.get_commit(pr.head.sha)
        check_runs = commit.get_check_runs()
        from collections import Counter

        different_statuses = Counter(run.conclusion for run in check_runs)
        print(f"PR #{repo_pr.pr_number} - Check run statuses: {different_statuses}")
        # PR #21634 - Check run statuses: Counter({'success': 13, 'neutral': 1})
        # PR #21615 - Check run statuses: Counter({'success': 125, 'failure': 13, 'neutral': 1, 'skipped': 1})
        # PR #21612 - Check run statuses: Counter({'success': 96, 'skipped': 1, 'neutral': 1})
        ci_tests_passed = all(run.conclusion == "success" for run in check_runs)
        is_merged = pr.merged
        is_closed = pr.state == "closed"

        result = PRStatus(
            pr_number=repo_pr.pr_number,
            title=pr.title,
            last_commit_sha=pr.head.sha,
            ci_check_passed=ci_tests_passed,
            is_merged=is_merged,
            is_closed=is_closed,
        )
        return result
    except github.GithubException as e:
        print(f"Error fetching PR status: {e}")
        return PRStatus(
            pr_number=repo_pr.pr_number,
            title="",
            last_commit_sha="",
            ci_check_passed=False,
            is_merged=False,
            is_closed=False,
            error_occured=True,
            error_msg=str(e),
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        return PRStatus(
            pr_number=repo_pr.pr_number,
            title="",
            last_commit_sha="",
            ci_check_passed=False,
            is_merged=False,
            is_closed=False,
            error_occured=True,
            error_msg=str(e),
        )
