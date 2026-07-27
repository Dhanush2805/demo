#Added new file
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import get_logger
from app.router import upload_router, chat_router, dashboard_router, data_source_router, operation_team_view_route, cdp_nlq_router

# Initialize logger
logger = get_logger('api')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events
    """
    # Startup
    logger.info("Knowledge Graph Chatbot API starting up...")
    logger.info("Upload endpoints available at /api/v1/upload/")
    logger.info("Chat endpoints available at /api/v1/chat/")
    logger.info("API documentation available at /docs")
    logger.info("Application startup completed successfully")
    
    yield
    
    # Shutdown
    logger.info("Knowledge Graph Chatbot API shutting down...")
    logger.info("Application shutdown completed")


# Create FastAPI application
app = FastAPI(
    title="Knowledge Graph Chatbot API",
    description="""
    ## Knowledge Graph Chatbot API

    A powerful agentic system for creating knowledge graphs from S3 data and enabling intelligent chat interactions.

    ### Features

    #### 📤 Upload Workflow
    - **S3 Integration**: Download CSV and Excel files from S3 buckets (supports both public and authenticated access)
    - **Local File Upload**: Process CSV and Excel files from local file paths
    - **Multipart Upload**: Upload files directly via browser using multipart form data
    - **Smart Processing**: Convert Excel to CSV, analyze structure
    - **Vector Creation**: Generate embeddings for semantic search
    - **LLM-Powered**: Use AWS Bedrock to generate Cypher queries
    - **Graph Creation**: Automatically create nodes and relationships in Neo4j

    #### 💬 Chat Workflow  
    - **Vector Search**: Find relevant context from uploaded data
    - **Schema-Aware**: Understand current graph structure
    - **Query Generation**: Convert natural language to Cypher
    - **Smart Answers**: Summarize results into natural language

    ### Agentic Architecture

    The system uses autonomous agents that coordinate with each other:
    
    - **Upload Agent**: Orchestrates the entire upload workflow
    - **Chat Agent**: Handles question processing and response generation
    - **S3 Agent**: Manages file discovery and download from S3
    - **Processing Agent**: Handles file conversion and vector creation
    - **LLM Agent**: Manages all interactions with AWS Bedrock
    - **Neo4j Agent**: Handles all database operations

    ### Getting Started

    1. **Upload Data**: Choose one of the upload methods:
       - S3: Use `/api/v1/upload/s3-knowledge-graph` for files in S3 buckets
       - Local Files: Use `/api/v1/upload/local-knowledge-graph` for local file paths
       - Direct Upload: Use `/api/v1/upload/multipart-knowledge-graph` for browser uploads
    2. **Ask Questions**: Use `/api/v1/chat/query` to interact with your data
    3. **Monitor Status**: Use status endpoints to check system health

    ### Requirements

    - **Neo4j Database**: Running and accessible
    - **AWS Credentials**: For Bedrock LLM (S3 access optional for public URLs)
    - **S3 Data**: CSV or Excel files in an accessible S3 bucket (public or private)
    """,
    version="1.0.0",
    root_path="/chatbot",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ma-insights.usefulbi.com/",
    ],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router.router)
app.include_router(chat_router.router)
app.include_router(dashboard_router.router)
app.include_router(data_source_router.router)
app.include_router(operation_team_view_route.router)
app.include_router(cdp_nlq_router.router)

@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Knowledge Graph Chatbot API",
        "version": "1.0.0",
        "description": "Agentic system for S3 to Knowledge Graph conversion and intelligent chat",
        "docs": "/docs",
        "upload_endpoints": {
            "s3": "/api/v1/upload/s3-knowledge-graph",
            "local": "/api/v1/upload/local-knowledge-graph", 
            "multipart": "/api/v1/upload/multipart-knowledge-graph"
        },
        "chat_endpoint": "/api/v1/chat/query",
        "cdp_nlq_endpoints": {
            "query": "/api/v1/cdp-nlq/query",
            "health": "/api/v1/cdp-nlq/health",
            "schema": "/api/v1/cdp-nlq/schema"
        },
        "dashboard_endpoints": {
            "insights": "/api/insights",
            "publications": "/api/publications",
            "projects": "/api/projects",
            "kols": "/api/kols",
            "kol": "/api/kol"
        },
        "status": "running"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """
    Overall health check endpoint
    """
    return {
        "status": "healthy",
        "service": "knowledge-graph-chatbot",
        "components": {
            "upload_service": "available",
            "chat_service": "available",
            "logging": "active"
        }
    }



if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    logger.info("Starting Knowledge Graph Chatbot API server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disabled to prevent continuous file watching logs
        log_level="warning",  # Reduced to prevent system noise
        access_log=False  # Disable access logs for cleaner output
    ) 
