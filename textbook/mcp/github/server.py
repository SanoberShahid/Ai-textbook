import os
from mcp import FastMCP
from github import Github

# Initialize FastMCP
mcp = FastMCP()

# --- GitHub Instance ---
def get_github_instance():
    """Initializes and returns a Github instance."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set.")
    return Github(token)

# --- GitHub Tools ---
@mcp.tool(name="github.list_repos")
def list_repos(username: str):
    """Lists repositories for a given user."""
    g = get_github_instance()
    user = g.get_user(username)
    repos = [repo.full_name for repo in user.get_repos()]
    return repos

# --- Main Server Execution ---
if __name__ == "__main__":
    # You might want to add more tools here
    mcp.run()
