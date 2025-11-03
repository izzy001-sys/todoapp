from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import init_db
from app.routers import auth, todos
from app.config import CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS

app = FastAPI(title="Todo App")

# Health check endpoint for Kubernetes
@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes liveness and readiness probes"""
    try:
        # Check database connection
        from app.database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return JSONResponse(
            status_code=200,
            content={"status": "healthy", "service": "todo-app"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize database
init_db()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)

