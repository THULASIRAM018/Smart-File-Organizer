import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from auth_routes import router as auth_router
from file_routes import router as file_router
from watchdog_monitor import start_monitoring, stop_monitoring


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# EMAIL CONFIGURATION CHECK
# ============================================================

print("EMAIL_USER:", os.getenv("EMAIL_USER"))
print("EMAIL_PASSWORD SET:", bool(os.getenv("EMAIL_PASSWORD")))


# ============================================================
# INITIALIZE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Smart File Organizer System",
    description="Smart File Organizer backend API",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

# Add every frontend origin that is allowed to access
# this FastAPI backend.

origins = [
    # Current Vercel frontend
    "https://smart-file-organizer-dbltamn4y-thulasiram018s-projects.vercel.app",

    # Current/previous Vercel deployment
    "https://smart-file-organizer-flax.vercel.app",

    # Older Vercel deployment
    "https://smart-file-organizer-hiyizpw9g-thulasiram018s-projects.vercel.app",

    # Local Vite development
    "http://localhost:5173",

    # Local Vite development using 127.0.0.1
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,

    # Allowed frontend URLs
    allow_origins=origins,

    # Allow cookies/authentication credentials
    allow_credentials=True,

    # Allow GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_methods=["*"],

    # Allow Content-Type, Authorization, etc.
    allow_headers=["*"],
)


# ============================================================
# AUTHENTICATION ROUTES
# ============================================================

# Final endpoints:
#
# POST /auth/send-otp
# POST /auth/verify-otp
# POST /auth/login
# etc.

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)


# ============================================================
# FILE OPERATION ROUTES
# ============================================================

# File routes keep their existing paths.

app.include_router(
    file_router,
    prefix="",
    tags=["File Operations"]
)


# ============================================================
# STARTUP EVENT
# ============================================================

@app.on_event("startup")
async def startup_event():
    """
    Start watchdog monitoring if WATCH_FOLDER
    is configured and the folder exists.
    """

    watch_folder = os.getenv("WATCH_FOLDER")

    if watch_folder:
        if os.path.isdir(watch_folder):
            try:
                start_monitoring(watch_folder)
                print(f"Started monitoring: {watch_folder}")
            except Exception as e:
                print(f"Failed to start monitoring: {e}")
        else:
            print(
                f"WATCH_FOLDER does not exist or is invalid: "
                f"{watch_folder}"
            )
    else:
        print("WATCH_FOLDER not configured. Monitoring disabled.")


# ============================================================
# SHUTDOWN EVENT
# ============================================================

@app.on_event("shutdown")
async def shutdown_event():
    """
    Stop all watchdog observers when the application shuts down.
    """

    try:
        stop_monitoring()
        print("Stopped all monitors")
    except Exception as e:
        print(f"Error while stopping monitors: {e}")


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Smart File Organizer System API",
        "status": "running"
    }


# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Smart File Organizer API"
    }
