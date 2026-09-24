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
    version="1.0.0",
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

# IMPORTANT:
# Add the EXACT frontend origin that is shown in the browser.
#
# Current Vercel deployment:
# https://smart-file-organizer-a9zkpcsro-thulasiram018s-projects.vercel.app
#
# Previous deployments are also included so they continue to work.

origins = [
    # --------------------------------------------------------
    # CURRENT VERCEL FRONTEND
    # --------------------------------------------------------
    "https://smart-file-organizer-a9zkpcsro-thulasiram018s-projects.vercel.app",

    # --------------------------------------------------------
    # PREVIOUS VERCEL FRONTEND
    # --------------------------------------------------------
    "https://smart-file-organizer-dbltamn4y-thulasiram018s-projects.vercel.app",

    # --------------------------------------------------------
    # OTHER VERCEL DEPLOYMENT
    # --------------------------------------------------------
    "https://smart-file-organizer-flax.vercel.app",

    # --------------------------------------------------------
    # OLDER VERCEL DEPLOYMENT
    # --------------------------------------------------------
    "https://smart-file-organizer-hiyizpw9g-thulasiram018s-projects.vercel.app",

    # --------------------------------------------------------
    # LOCAL DEVELOPMENT
    # --------------------------------------------------------
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,

    # Allowed frontend origins
    allow_origins=origins,

    # Allow cookies / authentication credentials
    allow_credentials=True,

    # Allow all HTTP methods including OPTIONS
    allow_methods=["*"],

    # Allow all request headers
    allow_headers=["*"],
)


# ============================================================
# AUTHENTICATION ROUTES
# ============================================================

# Because prefix="/auth" is used here:
#
# auth_routes.py:
#     @router.post("/send-otp")
#
# becomes:
#
#     POST /auth/send-otp
#
# Similarly:
#
#     POST /auth/verify-otp

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)


# ============================================================
# FILE OPERATION ROUTES
# ============================================================

# File routes keep their existing paths.

app.include_router(
    file_router,
    prefix="",
    tags=["File Operations"],
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

    if not watch_folder:
        print("WATCH_FOLDER not configured. Monitoring disabled.")
        return

    if not os.path.isdir(watch_folder):
        print(
            f"WATCH_FOLDER does not exist or is invalid: "
            f"{watch_folder}"
        )
        return

    try:
        start_monitoring(watch_folder)
        print(f"Started monitoring: {watch_folder}")

    except Exception as error:
        print(
            f"Failed to start watchdog monitoring: {error}"
        )


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

    except Exception as error:
        print(
            f"Error while stopping monitors: {error}"
        )


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    """
    Basic API status endpoint.
    """

    return {
        "message": "Smart File Organizer System API",
        "status": "running",
    }


# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================

@app.get("/health")
def health_check():
    """
    Health check endpoint for Render or other monitoring services.
    """

    return {
        "status": "healthy",
        "service": "Smart File Organizer API",
    }