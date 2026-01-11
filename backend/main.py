"""
FastAPI Main Application
Constitutional Engine for ONOE Analysis
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import articles, analysis, admin

# Create FastAPI app
app = FastAPI(
    title="Constitutional Engine for ONOE",
    description="Advanced AI-powered analysis of One Nation One Election feasibility",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default + React default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(articles.router)
app.include_router(analysis.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Constitutional Engine for ONOE Analysis",
        "version": "1.0.0",
        "endpoints": {
            "articles": "/api/articles",
            "analysis": "/api/analysis/overall",
            "priorities": "/api/analysis/priorities",
            "critical_356": "/api/articles/356/critical"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
