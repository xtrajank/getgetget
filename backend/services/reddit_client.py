'''
Reddit facing client that fetches desired data in its entirety from Reddit API

Endpoints used:
    - GET /api/subreddit_autocomplete_v2: list of subreddits whose name starts with query
    - GET /subreddits/'where' (popular, new, gold): 'where' parameter chooses order in which subreddits are displayed

Features:
    - Retrieve most relevant subreddits
    - Retrieve most relevant threads in a relevant subreddit
    - Retrieve most relevant and popular comment in a relevant thread & subreddit
'''
import httpx
import os
from urllib.parse import unquote
from dotenv import load_dotenv
from backend.services.Result import Result

load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = "getgetget/0.1 by u/xtrajank"
BASE_URL = "https://www.reddit.com/"

def build_url(base_url: str = BASE_URL, path: str = "", headers: dict = {"User-Agent": USER_AGENT}) -> tuple:
    '''
    Builds any url to be passed into http get calls. Headers also passed.

    Parameters:
        base_url(str): the domain of the site (default=BASE_URL)
        path(str): where in that domain (default="")
        headers(dict): any information you might want to include when passing into http get
    '''
    full_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    return full_url, headers

async def get_json(url, params=None, headers=None): 
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPStatusError as e:
            return {"error": f"Request failed: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}

def get_keywords(question: str) -> str:
    '''
    Takes the question passed from frontend and extracts the key words.
    '''
    common_words =  {
        "a", "an", "the", "this", "that", "these", "those",
        "in", "on", "at", "to", "from", "with", "about", "by", "for", "of", "over", "under", "between",
        "and", "or", "but", "nor", "so", "yet", "if", "although", "because", "while",
        "I", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
        "my", "your", "his", "their", "its", "our",
        "is", "am", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did",
        "will", "would", "can", "could", "shall", "should", "may", "might", "must",
        "very", "really", "just", "only", "even", "too", "also", "not",
        "now", "then", "ever", "always", "never", "here", "there", "like", "such", "thing", "things", "stuff",
        "actually", "basically", "literally", "okay", "well", "uh", "hmm", "maybe", "perhaps", "anyway"
    }

    result = ''

    decoded = unquote(question)
    keywords = decoded.split(' ')
    valid_query = True

    while valid_query:
        for word in keywords:
            if len(result) + len(word) > 25:
                valid_query = False
            elif '=' in word and len(word) > 1:
                parts = word.split('=')
                for part in parts:
                    result += f' {part}'
                result += ' ='
            elif word.lower() not in common_words:
                result += f' {word}'
        valid_query = False
    return result.strip()

async def fetch_subreddit(subreddit: str, limit: int = 3):
    '''
    Gets the specified subreddits top posts.

    Parameters:
        subreddit(str): the subreddit to fetch
        limit(int): the max number of top threads to return (default=3)
    '''
    subreddit_url, headers = build_url(path=f"r/{subreddit}/top.json?limit={limit}&t=month")
    return await get_json(subreddit_url, headers=headers)
        
async def search_reddit(question: str):
    results = []
    # max 2 subreddits re: the query -> subreddit_response
    subreddit_url, headers = build_url(path=f"api/subreddit_autocomplete_v2.json")
    subreddit_params = {
        "query": get_keywords(question),
        "include_over_18": "true",
        "include_profiles": "false",
        "limit": 5
    }
    subreddit_response = await get_json(url=subreddit_url, params=subreddit_params, headers=headers)

    # get sorted list of relevant subreddits by subscribers
    subreddit_titles = [(child["data"]["title"], child["data"]["display_name"]) for child in sorted(subreddit_response.get("data", {}).get("children",[]), key=lambda s: s["data"].get("subscribers") or 0, reverse=True)]

    print(subreddit_titles)

    if len(subreddit_titles) == 0:
        result_error = Result("No subreddits found.")
        results.append(result_error)
        return results
    
    # using the titles, get the top 3 threads
    for title, display_name in subreddit_titles:
        search_result = Result(title, display_name)

        top_thread_url, headers = build_url(path=f"/r/{display_name}/search.json")
        top_thread_params = {
            "q": get_keywords(question),
            "limit": 1,
            "sort": "top",
            "restrict_sr": True
        }

        thread_response = await get_json(url=top_thread_url, params=top_thread_params, headers=headers)

        # get list of the threads
        thread_children = thread_response.get("data", {}).get("children", [])

        if not thread_children:
            result_error = Result(f"No threads found in subreddit {title}")
            results.append(result_error)
            return results

        # get all data into one variable
        top_thread_data = thread_children[0]["data"]

        # thread id
        thread_id = top_thread_data["id"]

        print(thread_id)
        # get desired data into dict
        search_result.top_thread = {
            "author": top_thread_data["author"],
            "body": top_thread_data["selftext"]
        }

        # get top comment from thread id
        top_comment_url, headers = build_url(path=f"comments/{thread_id}.json")
        top_comment_params = {
            "sort": "top"
        }

        top_comment_response = await get_json(url=top_comment_url, params=top_comment_params, headers=headers)

        # get full top comment data
        top_comment_full = top_comment_response[1]["data"]["children"][0]["data"]

        # set top comment to dict of information desired
        search_result.top_comment = {
            "author": top_comment_full["author"],
            "body": top_comment_full["body"]
        }

        results.append(search_result)

    return results