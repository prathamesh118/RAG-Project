"""GitHub Loader"""

from typing import List
from langchain_community.document_loaders import GithubFileLoader
from langchain_core.documents import Document


def load_github(repo: str, branch: str = "main", access_token: str = "") -> List[Document]:
    loader = GithubFileLoader(
        repo=repo,
        branch=branch,
        access_token=access_token,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: file_path.endswith(
            (".md", ".txt", ".py", ".js", ".ts", ".json")
        ),
    )
    return loader.load()
