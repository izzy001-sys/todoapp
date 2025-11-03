#!/bin/sh
# Health check script for Kubernetes liveness and readiness probes

# Check if the application is responding
if curl -f http://localhost:8000/health 2>/dev/null >/dev/null; then
    exit 0
fi

# Fallback: check if uvicorn process is running
if pgrep -f "uvicorn" > /dev/null; then
    exit 0
fi

exit 1

