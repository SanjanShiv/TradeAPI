import os
import logging
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Configure Gemini API Key
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"  # Using 2.5 flash

async def generate_analysis_report(sector: str, market_data_context: str) -> str:
    """
    Uses Google Gemini REST API to analyze the collected information and generate
    a structured markdown report for trade opportunities in the given sector.
    """
    if not API_KEY or API_KEY == "your_copied_key_here":
        raise HTTPException(status_code=500, detail="AI Model not configured. Please ensure GEMINI_API_KEY is correctly set in .env")

    prompt = f"""
You are an expert market analyst focusing on the Indian market.
Your task is to analyze the trade opportunities for the '{sector}' sector in India.
Below is some recent market data/news context retrieved from web search:

<Market_Data>
{market_data_context}
</Market_Data>

Based on this data and your own expert knowledge, generate a structured markdown report.
The report should include:
1. An Executive Summary
2. Current Market Trends in the {sector} Sector
3. Key Trade Opportunities (Imports/Exports or Internal Trade)
4. Potential Risks and Challenges
5. Conclusion/Recommendations

The output MUST be strongly formatted using Markdown headers (##, ###), bullet points, and bold text for emphasis.
Do not include any <Market_Data> tags in your output. Just output the final Markdown report.
"""

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                logger.error(f"Unexpected response format from Gemini: {data}")
                raise HTTPException(status_code=502, detail="Unexpected response format from Gemini API.")
            
    except httpx.HTTPError as e:
        logger.error(f"Gemini generation failed: {str(e)}")
        raise HTTPException(status_code=502, detail=f"AI API integration failure: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred during AI analysis.")
