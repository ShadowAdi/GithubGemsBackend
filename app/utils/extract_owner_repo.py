from urllib.parse import urlparse


def extract_owner_repo(repoUrl: str):
    url = repoUrl.strip("/")
    parts = url.split("/")
    if len(parts) < 2:
        raise ValueError("Invalid Github Link")
    return parts[-2], parts[-1]
