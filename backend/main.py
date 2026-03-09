import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from auth_routes import router as auth_router
from file_routes import router as file_router
from watchdog_monitor import start_monitoring, stop_monitoring

load_dotenv()

app = FastAPI(title="Smart File Organizer System")

# CORS for React frontend
origins = [
    "https://smart-file-organizer-orhn.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(file_router, prefix="", tags=["File Operations"])

@app.on_event("startup")
async def startup_event():
    """Start watchdog monitoring if a folder is configured."""
    watch_folder = os.getenv("WATCH_FOLDER")
    if watch_folder and os.path.isdir(watch_folder):
        start_monitoring(watch_folder)
        print(f"Started monitoring {watch_folder}")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop all watchdog observers."""
    stop_monitoring()
    print("Stopped all monitors")

@app.get("/")
def root():
    return {"message": "Smart File Organizer System API"}