from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import structlog
from prometheus_client import make_asgi_app
import os
from dotenv import load_dotenv

from app.api.routes import forecast, sources, health, policy, alerts, historical
from app.database import init_db
from app.services.data_pipeline import DataPipelineService

# Load environment variables
load_dotenv()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting Delhi-NCR Pollution Platform API")

    # Initialize database
    await init_db()

    # Start data pipeline service
    data_pipeline = DataPipelineService()
    await data_pipeline.start()

    yield

    # Cleanup
    await data_pipeline.stop()
    logger.info("Shutting down Delhi-NCR Pollution Platform API")


# Create FastAPI application
app = FastAPI(
    title="Delhi-NCR Pollution Intelligence Platform",
    description="AI-powered platform for real-time pollution monitoring, forecasting, and policy recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
DEV_ORIGINS = [
    "http://localhost:19006",  # Expo web (some ports vary)
    "http://127.0.0.1:19006",
    "http://localhost:8081",   # Metro bundler
    "http://127.0.0.1:8081",
    "http://localhost:5173",   # Vite dashboard if used
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    f"http://{os.getenv('LAN_IP')}:19006" if os.getenv('LAN_IP') else None,
]
DEV_ORIGINS = [o for o in DEV_ORIGINS if o]

app.add_middleware(
    CORSMiddleware,
    allow_origins=DEV_ORIGINS if os.getenv("ENVIRONMENT") != "production" else [
        "https://pollution-platform.com",
        "https://www.pollution-platform.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["pollution-platform.com", "*.pollution-platform.com"],
    )

"""Route registration

Primary versioned API under /api/v1/*
Provide backward-compatible short aliases (/forecast, /sources, /health) because user attempted calls without version prefix.
Long term: encourage clients to use /api/v1/* and deprecate unversioned paths.
"""

# Versioned routers
app.include_router(forecast.router, prefix="/api/v1/forecast", tags=["forecast"])
app.include_router(sources.router, prefix="/api/v1/sources", tags=["sources"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(policy.router, prefix="/api/v1/policy", tags=["policy"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(historical.router, prefix="/api/v1/historical", tags=["historical"])

# Backward-compatible aliases (non-versioned)
app.include_router(forecast.router, prefix="/forecast", tags=["forecast-legacy"])
app.include_router(sources.router, prefix="/sources", tags=["sources-legacy"])
app.include_router(health.router, prefix="/healthz", tags=["health-legacy"])  # /health already used below

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Delhi-NCR Pollution Intelligence Platform API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "forecast": "/api/v1/forecast",
            "sources": "/api/v1/sources",
            "health": "/api/v1/health",
            "policy": "/api/v1/policy",
            "alerts": "/api/v1/alerts",
            "historical": "/api/v1/historical",
            "docs": "/docs",
            "metrics": "/metrics",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "pollution-platform-api"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("DEBUG") == "True" else False,
        log_level="info",
    )
