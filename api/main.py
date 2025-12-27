from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from .database.database import engine
from .api import auth, todos


# Create the FastAPI app
app = FastAPI(
    title="Todo Web Application API",
    description="API for the Full-Stack Secure Todo Web Application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose the authorization header to allow frontend to access JWT
    expose_headers=["Access-Control-Allow-Origin"]
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])

@app.on_event("startup")
async def on_startup():
    # Create database tables
    SQLModel.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Todo Web Application API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}