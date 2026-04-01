# credits: https://github.com/deependujha

import random

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from prtracker.server.templates import templates

router = APIRouter()

# Dummy data for demo
DUMMY_STATUSES = ["success", "failure", "pending", "merged", "closed"]
DUMMY_TITLES = [
    "feat: Add dark mode support",
    "fix: Resolve memory leak in database connection",
    "refactor: Simplify authentication flow",
    "docs: Update API documentation",
    "test: Add comprehensive unit tests",
    "perf: Optimize image loading",
    "chore: Update dependencies",
    "feat: Implement real-time notifications",
]
DUMMY_REPOS = [
    "pytorch/pytorch",
    "tensorflow/tensorflow",
    "huggingface/transformers",
    "openai/gpt-3",
    "facebook/react",
]

pr_counter = 0


def get_status_color(status: str) -> str:
    """Get Tailwind color class for status"""
    colors = {
        "success": "bg-emerald-500",
        "merged": "bg-purple-500",
        "closed": "bg-slate-500",
        "failure": "bg-red-500",
        "pending": "bg-yellow-500",
    }
    return colors.get(status, "bg-yellow-500")


def get_status_badge(status: str) -> str:
    """Get Tailwind badge classes for status"""
    badges = {
        "success": "bg-emerald-500/20 text-emerald-300",
        "merged": "bg-purple-500/20 text-purple-300",
        "closed": "bg-slate-500/20 text-slate-300",
        "failure": "bg-red-500/20 text-red-300",
        "pending": "bg-yellow-500/20 text-yellow-300",
    }
    return badges.get(status, "bg-yellow-500/20 text-yellow-300")


@router.post("/prs")
def add_pr(request: Request, github_pr_url: str = Form(...)):
    """Add a new PR to track with dummy data"""
    global pr_counter
    pr_counter += 1

    # Parse PR number from URL if possible, otherwise use counter
    pr_number = pr_counter
    try:
        # Try to extract number from URL like owner/repo#123 or .../pull/123
        if "#" in github_pr_url:
            pr_number = int(github_pr_url.split("#")[-1])
        elif "/pull/" in github_pr_url:
            pr_number = int(github_pr_url.split("/pull/")[-1])
    except ValueError:
        pass

    # Generate dummy PR data
    status = random.choice(DUMMY_STATUSES)  # noqa: S311
    title = random.choice(DUMMY_TITLES)  # noqa: S311
    repo = random.choice(DUMMY_REPOS)  # noqa: S311
    updated_at = "2 min ago"

    return templates.TemplateResponse(
        request=request,
        name="partials/new_pr_card.html",
        context={
            "status": status.upper(),
            "status_color": get_status_color(status),
            "status_badge": get_status_badge(status),
            "title": title,
            "repo": repo,
            "pr_number": pr_number,
            "updated_at": updated_at,
            "pr_counter": pr_counter,
        },
    )


@router.delete("/prs/{pr_id}")
def delete_pr(pr_id: int):
    """Delete a PR from tracking"""
    return HTMLResponse("")
