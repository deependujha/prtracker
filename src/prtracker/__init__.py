# credits: https://github.com/deependujha
import os
from concurrent.futures import ThreadPoolExecutor

import github
from dotenv import load_dotenv
from github import Github

from prtracker.pr_tracker import pr_status
from prtracker.types import PRStatus, RepoPR


def get_all_prs(repository: str, prs_list: list[int]) -> list[RepoPR]:
    return [RepoPR(repository=repository, pr_number=pr_number) for pr_number in prs_list]


def pr_statuses(tracking_prs: list[RepoPR], github_instance: Github, max_workers: int = 5) -> list[PRStatus]:
    """
    Fetch PR status for all tracking PRs using multithreading.

    Args:
        tracking_prs: List of RepoPR objects to track
        github_instance: Github instance for API calls
        max_workers: Maximum number of worker threads

    Returns:
        List of PRStatus objects
    """
    results: list[PRStatus] = []

    def fetch_status(repo_pr: RepoPR) -> PRStatus:
        return pr_status(repo_pr=repo_pr, github_instance=github_instance)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(fetch_status, tracking_prs))

    return results


def main() -> None:
    load_dotenv(dotenv_path=".env")
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN not found in environment variables.")
    gh = Github(auth=github.Auth.Token(os.environ["GITHUB_TOKEN"]))

    repository = "Lightning-AI/pytorch-lightning"
    prs_list = [21612, 21615, 21634, 21628]  # Example

    tracking_prs = get_all_prs(repository, prs_list)

    print("Hello from prtracker!")
    statuses = pr_statuses(
        tracking_prs=tracking_prs,
        github_instance=gh,
    )

    print("\nPR Statuses:")
    for status in statuses:
        print(f"  PR #{status.pr_number}: {status.title}")
        print(f"    - CI Passed: {status.ci_check_passed}")
        print(f"    - Merged: {status.is_merged}")
        print(f"    - Closed: {status.is_closed}")
        print(f"    - Error: {status.error_occured}")
        print()
