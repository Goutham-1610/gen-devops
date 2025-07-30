import requests
import os

def fetch_repo_metadata(repo_url):
    token = os.getenv("GITHUB_TOKEN")
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    headers = {"Authorization": f"token {token}"} if token else {}

    resp = requests.get(api_url, headers=headers)
    data = resp.json()
    language = data.get("language", "Unknown")

    # Add more fields as needed
    return {"language": language, "name": repo, "owner": owner}
