import httpx
from app.config import logger
from fastapi import HTTPException


async def GetRepoInfoUrl(repoName: str, repoOwnerName: str):
    url = f"https://api.github.com/repos/{repoOwnerName}/{repoName}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                logger.warning(
                    f"GitHub API failed for {repoOwnerName}/{repoName}. Status: {response.status_code}"
                )
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"GitHub API error for {repoOwnerName}/{repoName}",
                )
            return response.json()
    except Exception as e:
        logger.error(
            f"Failed to get the Repo Information about Repo Name {str(repoName)} and Repo Owner Name {str(repoOwnerName)} and error is: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get the Repo Information about Repo Name {str(repoName)} and Repo Owner Name {str(repoOwnerName)} and error is: {str(e)}",
        )

