from bot.services.github_client import fetch_repo_metadata

def test_fetch_repo_metadata_stub():
    # Use a dummy or real public GitHub repo URL for the test
    metadata = fetch_repo_metadata("https://github.com/stevemar/sample-python-app")
    assert isinstance(metadata, dict)
    assert "language" in metadata
    assert "name" in metadata
    assert "owner" in metadata
