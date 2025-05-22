from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI()

# Define allowed origins (adjust as needed)
origins = [
    "http://localhost:3000",  # Local frontend
    "https://cargo-flowz-frontend-deploy.vercel.app/",  # Production frontend
    "https://admin.cargoflowz.com",
    "https://main.d2mfwhn26nhgf4.amplifyapp.com"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],        # Or specify like ["GET", "POST"]
    allow_headers=["*"],        # Or specify like ["Authorization", "Content-Type"]
)

# Include your API router
app.include_router(api_router)
