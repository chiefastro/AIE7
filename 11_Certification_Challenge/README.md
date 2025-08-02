# Mimi - AI Strategy Assistant

Mimi is an AI-powered assistant that helps you develop an AI strategy for your business. This service provides a FastAPI backend with a LangGraph-based agent system.

## Prerequisites

- Docker and Docker Compose
- Make (optional, for using Makefile commands)
- `.env` file with your API keys (see Environment Variables section)

## Quick Start

### 1. Build the Service

```bash
make build
```

Or manually:
```bash
docker-compose build
```

### 2. Populate the Vector Database

Before running the service, you need to populate the vector database with your documents:

```bash
make populate
```

Or manually:
```bash
docker-compose run --rm mimi-backend uv run python -m mimi.pipe.pipe
```

### 3. Run the Service

```bash
make run
```

Or manually:
```bash
docker-compose up
```

The service will be available at `http://localhost:8000`

## Available Make Commands

- `make help` - Show available commands
- `make build` - Build the Docker image
- `make up` - Run the service
- `make populate` - Populate the vector database
- `make clean` - Stop and remove containers
- `make logs` - View service logs
- `make up-background` - Run service in background
- `make rebuild` - Clean, build, and run

## API Endpoints

- `GET /` - Health check
- `POST /copilotkit` - CopilotKit endpoint for AI interactions

## Development

### Running Locally (without Docker)

If you prefer to run the service locally:

1. Install uv: `pip install uv`
2. Install dependencies: `uv sync`
3. Set PYTHONPATH: `export PYTHONPATH=backend/src`
4. Run the service: `uv run python -m mimi.asgi`

### Project Structure

```
backend/
├── src/
│   └── mimi/
│       ├── agents/          # LangGraph agents
│       ├── pipe/            # Document processing pipeline
│       ├── tools/           # Agent tools
│       └── asgi.py          # FastAPI application
data/                        # Document storage
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

- `PORT` - Service port (default: 8000)
- `OPENAI_API_KEY` - Your OpenAI API key (required for embeddings and LLM)
- Any other API keys required by your application

## Troubleshooting

- If you encounter permission issues, ensure Docker has proper permissions
- Check logs with `make logs` for debugging information
- Use `make up-background` to run in background
