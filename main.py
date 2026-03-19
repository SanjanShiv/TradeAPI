from fastapi import FastAPI, Depends, Request, HTTPException, status, Path
from fastapi.responses import Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from models import AnalysisResponse, ErrorResponse
from auth import get_api_key, get_session_info
from rate_limiter import limiter
from search import search_market_data
from analyzer import generate_analysis_report

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Trade Opportunities API",
    description="Analyzes market data and provides trade opportunity insights for specific sectors in India.",
    version="1.0.0"
)

# Attach rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get(
    "/analyze/{sector}", 
    responses={
        200: {
            "content": {"text/markdown": {}},
            "description": "A Markdown report containing the market analysis."
        },
        400: {"model": ErrorResponse}, 
        401: {"model": ErrorResponse}, 
        429: {"model": ErrorResponse},
        502: {"model": ErrorResponse}
    }
)
@limiter.limit("5/minute")
async def analyze_sector(
    request: Request,
    sector: str = Path(..., min_length=2, max_length=50, pattern="^[a-zA-Z0-9 -]+$"), 
    api_key: str = Depends(get_api_key)
):
    """
    Analyzes a given sector and returns a structured markdown report about trade opportunities.
    """
    session_info = get_session_info(api_key)
    logger.info(f"Processing request for sector: {sector}. Session: {session_info.get('session_id')}")

    try:
        # Step 1: Collect market data/news
        logger.info(f"Fetching market data for {sector}...")
        market_data_context = await search_market_data(sector)
        
        # Step 2: Analyze with Gemini
        logger.info(f"Analyzing data with Gemini for {sector}...")
        markdown_report = await generate_analysis_report(sector, market_data_context)
        
        # Return as a downloadable Markdown file
        return Response(
            content=markdown_report,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f'attachment; filename="{sector}_market_analysis.md"'
            }
        )
    except HTTPException:
        # Re-raise already formed HTTP Exceptions (from analyzer/search)
        raise
    except Exception as e:
        logger.error(f"Error processing /analyze/{sector}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during analysis: {str(e)}"
        )
