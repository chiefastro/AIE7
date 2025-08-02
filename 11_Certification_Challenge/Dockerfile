FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the backend source code
COPY backend/ ./backend/

# Copy data directory
COPY data/ ./data/

# Copy .env file if it exists
COPY .env* ./

# Set environment variables
ENV PYTHONPATH=/app/backend/src
ENV PORT=8000

# Expose port
EXPOSE 8000

# Default command to run the service
CMD ["uv", "run", "uvicorn", "mimi.asgi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 