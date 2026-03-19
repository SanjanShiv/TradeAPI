from duckduckgo_search import DDGS
from fastapi import HTTPException
import asyncio
import logging

logger = logging.getLogger(__name__)

def _blocking_search(query: str):
    with DDGS() as ddgs:
        return list(ddgs.text(query, region="in-en", max_results=5))

async def search_market_data(sector: str) -> str:
    """
    Searches for current market data and news regarding a specific sector in India.
    Returns a consolidated string of the search results context.
    """
    query = f"trade opportunities in {sector} sector India market analysis news"
    
    try:
        # Run the blocking search in an executor to keep FastAPI async loop free (Python 3.8 compatible)
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, _blocking_search, query)
            
        if not results:
            return "No recent market data found for this sector."
            
        # Combine the snippets and titles to provide context to the LLM
        context = ""
        for i, res in enumerate(results):
            context += f"Result {i+1}:\n"
            context += f"Title: {res.get('title', '')}\n"
            context += f"Body: {res.get('body', '')}\n\n"
            
        return context
        
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        # Raise proper 502 Bad Gateway to signify external dependency failure
        raise HTTPException(status_code=502, detail="External Search API unavailable. Please try again later.")
