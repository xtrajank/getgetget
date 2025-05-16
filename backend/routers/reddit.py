'''
Handle OAuth & set up router from public facing results
'''
from fastapi import APIRouter, Query
import backend.services.reddit_client as client

router = APIRouter(prefix="/api/reddit", tags=["Reddit"])

@router.get("/test-subreddit")
async def test_subreddit():
    return await client.fetch_subreddit("learnprogramming")

@router.get("/search")
async def search(question: str = Query(...)):
    return await client.search_reddit(question)
