# getgetget
my REST API practice repo

## Features
   - Search bar for querying topics or keywords
   - Results page displaying relevant content
   - Fast and minimal interface
   - Built with modern web technologies (Svelte + FastAPI)

## Tools/Technologies
### Frontend
    - Svelte – Frontend framework for building reactive UI
    - JavaScript – General scripting
    - HTML5 – Markup structure
    - CSS3 – Styling and layout
    - Fetch API / async-await – For making HTTP requests to the backend
    - Vite – Build tool (used implicitly with modern Svelte setup)

### Backend
    - FastAPI – Python web framework for building REST APIs
    - httpx – Async HTTP client used to call external APIs like Reddit
    - Python 3.10
    - dotenv (python-dotenv) – For loading environment variables (like API keys)

### Reddit API Integration
    - Reddit public API (unauthenticated for now) – To fetch subreddits, threads, and comments
    - Query parameters – Used for custom searches

### Testing & Development Tools
    - Uvicorn – ASGI server to run FastAPI app
    - Virtualenv – Python environment isolation
    - npm – Node.js package manager for frontend
    - npx – For running Svelte scaffolding commands

## TODO:
    - Integrate OAUTH2
    - Algorithmically modify searches for best query
