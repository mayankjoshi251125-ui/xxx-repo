from langchain.tools import tool
from app.github_tools import (
    create_repository,
    create_issue,
    create_pull_request,
    audit_repository,
    commit_and_push_file,
)

@tool
def create_github_repository_tool(
    name: str,
    description: str = "",
    private: bool = False,
) -> str:
    """Create a GitHub repository.
    STRICT TOOL: Use ONLY when the user explicitly wants to CREATE a new GitHub repository.

    Triggers:
    - "create repo"
    - "create repository"
    - "create private repo"
    - "create public repo"

    DO NOT use this tool for:
    - README generation
    - auditing
    - file creation

    """

    result = create_repository(
        name=name,
        description=description,
        private=private
    )

    return result


@tool
def commit_and_push_file_tool(
    repo: str,
    file_path: str,
    branch: str = "main",
    commit_message: str = "Update file",
) -> str:
    """
    Create or update a file in a GitHub repository and commit it.
    """

    result = commit_and_push_file(
        repo=repo,
        branch=branch,
        file_path=file_path,
        commit_message=commit_message,
    )

    if isinstance(result, dict) and result.get("content"):
        return f" File '{file_path}' committed successfully to branch '{branch}'."

    if isinstance(result, dict) and result.get("error"):
        return f" {result['error']}"

    return f" GitHub API Error: {result}"


@tool
def create_issue_tool(repo: str, title: str, body: str) -> str:
    """Create a GitHub issue."""
    return str(create_issue(repo, title, body))



@tool
def create_pr_tool(
    repo: str,
    title: str,
    body: str,
    head: str,
    base: str = "main",
) -> str:
    """Create a pull request."""
    return str(create_pull_request(repo, title, body, head, base))


@tool
def audit_repo_tool(repo: str) -> str:
    """
    Suggest best GitHub practices for the given repository.
    """
    return audit_repository(repo)


from app.readme_generator import generate_readme

@tool
def create_readme_file_tool(repo: str) -> str:
    """
    Generate a professional README for a GitHub repository
       STRICT TOOL: Use ONLY when the user wants to GENERATE or UPDATE a README.md file.

    Triggers:
    - "generate readme"
    - "create readme"
    - "update readme"

    DO NOT use this tool for:
    - creating repositories
    - auditing repositories
    """

    content = generate_readme(repo)

    # Save locally
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    return content












