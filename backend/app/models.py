from pydantic import BaseModel

class SearchRequest(BaseModel):
    keywords: str
    max_results: int = 50

class VideoInfo(BaseModel):
    id: str
    title: str
    channel: str
    timestamp: str

class SearchResult(BaseModel):
    added: int
    skipped: int
    errors: int
    videos: list
