from fastapi import APIRouter, BackgroundTasks, HTTPException
from models import EmailRequest, OTPVerifyRequest
from otp_service import generate_otp, send_otp_email, store_otp, verify_otp

router = APIRouter()

@router.post("/send-otp")
async def send_otp(request: EmailRequest, background_tasks: BackgroundTasks):
    """Generate OTP, store it, and send via email."""
    email = request.email
    otp = generate_otp()
    store_otp(email, otp)
    send_otp_email(background_tasks, email, otp)
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
async def verify_otp_endpoint(request: OTPVerifyRequest):
    """Verify OTP and return session token if correct."""
    email = request.email
    otp = request.otp
    token = verify_otp(email, otp)
    if token is None:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return {"message": "Authentication successful", "session_token": token}