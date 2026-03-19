# Trade Opportunities API

A robust FastAPI backend service that analyzes market data and provides trade opportunity insights for specific sectors in India.

## Features
- **FastAPI Core**: Async endpoint with Pydantic path validation.
- **AI Integration**: Direct async REST integration with Google Gemini 2.5 Flash for market analysis.
- **Dynamic Content**: Asynchronous DuckDuckGo search ensures the AI model operates on real-time news constraints.
- **Security**: In-memory Session tracking and strict API Key Security (auto-generates strong random keys if missing).
- **Rate Limiting**: Custom implementation using SlowAPI restricting abuse on a per-session/API-Key level (5/minute).
- **Graceful Failures**: Propagates 502 Bad Gateway responses properly when upstream APIs (Google or DDG) fail.

## Environment Setup
It is recommended to run this project in a standard Python virtual environment.

```bash
# Clone or navigate to the repository
cd trade-api-folder

# Create a fresh virtual environment
python -m venv venv

# Activate it
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration
Requires a `.env` file in the root directory:

```env
# Required: Your Google AI Studio API Key (used for Gemini Integration)
GEMINI_API_KEY="your-gemini-key-goes-here"

# Recommended: The authentication key users need to provide to use your API.
# If you don't declare it, the application will securely auto-generate one on startup!
API_KEY="your-secure-backend-password-here"
```

## Running the Application
Run the local ASGI server using Uvicorn:

```bash
uvicorn main:app --reload
```
The server will be available at `http://127.0.0.1:8000`.

## Testing the Application
An included test script `test.py` validates the rate limiting, authentication headers, and core logic.
```bash
python test.py
```

## API Documentation
Once running, navigate to `http://127.0.0.1:8000/docs` to interact with the Swagger auto-generated documentation. The endpoint accepts the authentication token globally and offers intuitive interface testing.
