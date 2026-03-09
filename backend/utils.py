import os
import uuid
import time

def generate_otp():
    """Generate a 6-digit numeric OTP."""
    import random
    return f"{random.randint(0, 999999):06d}"

def generate_session_token():
    """Generate a random session token."""
    return str(uuid.uuid4())

def get_file_extension(filename: str) -> str:
    """Return the file extension without the dot, lowercased."""
    return os.path.splitext(filename)[1].lower().lstrip('.')

def get_category(ext: str) -> str:
    """Return the category name based on file extension."""
    image_exts = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'}
    doc_exts = {'pdf', 'docx', 'doc', 'txt', 'xlsx', 'xls', 'pptx', 'odt'}
    video_exts = {'mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv'}
    code_exts = {'py', 'js', 'html', 'css', 'cpp', 'java', 'php', 'rb'}

    if ext in image_exts:
        return "Images"
    elif ext in doc_exts:
        return "Documents"
    elif ext in video_exts:
        return "Videos"
    elif ext in code_exts:
        return "Code"
    else:
        return "Others"