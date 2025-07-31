# bot/services/github_client.py
import requests
import os

def fetch_repo_metadata(repo_url):
    token = os.getenv("GITHUB_TOKEN")
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    
    # Remove .git suffix if present
    if repo.endswith('.git'):
        repo = repo[:-4]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"token {token}"} if token else {}
    
    try:
        resp = requests.get(api_url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        
        # Get additional useful info
        languages_url = f"{api_url}/languages"
        lang_resp = requests.get(languages_url, headers=headers)
        languages = lang_resp.json() if lang_resp.status_code == 200 else {}
        
        return {
            "language": data.get("language", "Unknown"),
            "name": repo,
            "owner": owner,
            "description": data.get("description", ""),
            "languages": list(languages.keys())[:3],  # Top 3 languages
            "size": data.get("size", 0),
            "private": data.get("private", False)
        }
    except Exception as e:
        return {
            "language": "Unknown", 
            "name": repo, 
            "owner": owner,
            "error": str(e)
        }
