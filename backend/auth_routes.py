from fastapi import APIRouter, HTTPException

from models import EmailRequest, OTPVerifyRequest
from otp_service import (
    generate_otp,
    send_otp_email,
    store_otp,
    verify_otp,
)


# ============================================================
# CREATE AUTHENTICATION ROUTER
# ============================================================

# The /auth prefix is added in main.py.
#
# Final endpoints:
#   POST /auth/send-otp
#   POST /auth/verify-otp

router = APIRouter()


# ============================================================
# SEND OTP
# ============================================================

@router.post("/send-otp", tags=["Authentication"])
async def send_otp_endpoint(request: EmailRequest):
    """
    Generate an OTP, send it to the user's email,
    and store it for later verification.
    """

    email = request.email.strip().lower()

    # --------------------------------------------------------
    # Basic email validation
    # --------------------------------------------------------

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email address is required",
        )

    # --------------------------------------------------------
    # Generate OTP
    # --------------------------------------------------------

    try:
        otp = generate_otp()
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate OTP: {str(error)}",
        ) from error

    # --------------------------------------------------------
    # Send OTP email
    # --------------------------------------------------------

    try:
        send_otp_email(email, otp)

    except RuntimeError as error:
        # Email configuration / SMTP errors
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error

    except Exception as error:
        # Unexpected email errors
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send OTP email: {str(error)}",
        ) from error

    # --------------------------------------------------------
    # Store OTP only after successful email sending
    # --------------------------------------------------------

    try:
        store_otp(email, otp)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to store OTP: {str(error)}",
        ) from error

    # --------------------------------------------------------
    # Successful response
    # --------------------------------------------------------

    return {
        "message": "OTP sent successfully",
        "email": email,
    }


# ============================================================
# VERIFY OTP
# ============================================================

@router.post("/verify-otp", tags=["Authentication"])
async def verify_otp_endpoint(request: OTPVerifyRequest):
    """
    Verify the OTP entered by the user.

    If the OTP is valid and has not expired,
    return a session token.
    """

    email = request.email.strip().lower()
    otp = str(request.otp).strip()

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email address is required",
        )

    if not otp:
        raise HTTPException(
            status_code=400,
            detail="OTP is required",
        )

    # --------------------------------------------------------
    # Verify OTP
    # --------------------------------------------------------

    try:
        token = verify_otp(email, otp)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"OTP verification failed: {str(error)}",
        ) from error

    # --------------------------------------------------------
    # Invalid or expired OTP
    # --------------------------------------------------------

    if token is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP",
        )

    # --------------------------------------------------------
    # Successful authentication
    # --------------------------------------------------------

    return {
        "message": "Authentication successful",
        "session_token": token,
        "email": email,
    }
