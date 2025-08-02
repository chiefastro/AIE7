from dotenv import load_dotenv
import os
import uvicorn
import logging
import time
from typing import Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from copilotkit.integrations.fastapi import add_fastapi_endpoint

from mimi.agents.supervisor import create_supervisor_graph
from mimi.agents.multi_tasker import create_multi_tasker_graph
from mimi.config.cors import ALLOWED_ORIGINS, ALLOWED_METHODS, ALLOWED_HEADERS

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # Force reconfiguration
)
logger = logging.getLogger(__name__)

# Ensure our logger is at INFO level
logger.setLevel(logging.INFO)

# Add a console handler if none exists
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    print("🚀 Starting Mimi backend application...")  # Debug print
    logger.info("🚀 Starting Mimi backend application...")
    yield
    print("🛑 Shutting down Mimi backend application...")  # Debug print
    logger.info("🛑 Shutting down Mimi backend application...")

app = FastAPI(
    title="Mimi Backend API",
    description="Backend API for Mimi AI Strategy Assistant",
    version="1.0.0",
    lifespan=lifespan
)

print("✅ FastAPI app created successfully")  # Debug print
logger.info("✅ FastAPI app created successfully")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)

@app.middleware("http")
async def logging_middleware(request: Request, call_next: Callable) -> Response:
    """Middleware to log all HTTP requests and responses."""
    print(f"🔍 MIDDLEWARE CALLED: {request.method} {request.url.path}")  # Debug print
    logger.info(f"🔍 MIDDLEWARE CALLED: {request.method} {request.url.path}")
    
    start_time = time.time()
    
    # Log request
    logger.info(f"📥 Request: {request.method} {request.url.path}")
    logger.info(f"📋 Headers: {dict(request.headers)}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(f"📤 Response: {response.status_code} - {process_time:.4f}s")
    
    return response

print("✅ Logging middleware added successfully")  # Debug print
logger.info("✅ Logging middleware added successfully")


sdk = CopilotKitRemoteEndpoint(
    agents=[
        # Register the LangGraph agent using the LangGraphAgent class
        LangGraphAgent(
            name="MimiTeam",
            description="Mimi Team can help you develop an AI strategy for your business.",
            graph=create_supervisor_graph()
        ),
        LangGraphAgent(
            name="Mimi",
            description="Mimi can help you develop an AI strategy for your business.",
            graph=create_multi_tasker_graph()
        ),
    ]
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

# Add health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "Mimi Backend API",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint."""
    logger.info("Root endpoint accessed")
    return {
        "message": "Mimi Backend API is running",
        "docs": "/docs",
        "health": "/health"
    }


def main():
    """Run the uvicorn server."""
    print("🎯 Starting uvicorn server...")  # Debug print
    logger.info("🎯 Starting uvicorn server...")
    
    port = int(os.getenv("PORT", "8000"))
    print(f"🌐 Server will run on port {port}")  # Debug print
    logger.info(f"🌐 Server will run on port {port}")
    
    uvicorn.run(
        "mimi.asgi:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info",
        access_log=True,
    )

if __name__ == "__main__":
    main()

