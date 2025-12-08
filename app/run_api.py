import os
import sys
import uvicorn


def main():
    """Run the FastAPI application with uvicorn."""
    host = os.getenv("API_HOST", "127.0.0.1")

    try:
        api_port = os.getenv("API_PORT", "8000")
        port = int(api_port)
    except ValueError:
        print(f"Error: API_PORT must be a valid integer, got '{api_port}'", file=sys.stderr)
        sys.exit(1)

    # Only enable reload in development (when API_ENV is not 'production')
    api_env = os.getenv("API_ENV", "development")
    reload = api_env.lower() != "production"

    uvicorn.run(
        "app.api.app:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    main()
