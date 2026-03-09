from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    email: EmailStr

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str

class FolderPathRequest(BaseModel):
    folder_path: str

class ScanResponse(BaseModel):
    images: int
    documents: int
    videos: int
    code: int
    others: int
    total: int

class OrganizeResponse(BaseModel):
    message: str
    organized_count: int