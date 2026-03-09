from fastapi import APIRouter, HTTPException
from models import FolderPathRequest, ScanResponse, OrganizeResponse
from file_scanner import scan_folder
from file_organizer import organize_folder

router = APIRouter()

@router.post("/scan", response_model=ScanResponse)
async def scan_endpoint(request: FolderPathRequest):
    """Scan the given folder and return file statistics."""
    try:
        counts, total = scan_folder(request.folder_path)
        # Convert category names to lowercase keys for response
        response = {
            "images": counts["Images"],
            "documents": counts["Documents"],
            "videos": counts["Videos"],
            "code": counts["Code"],
            "others": counts["Others"],
            "total": total
        }
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/organize", response_model=OrganizeResponse)
async def organize_endpoint(request: FolderPathRequest):
    """Organize files in the given folder into category subfolders."""
    try:
        moved = organize_folder(request.folder_path)
        return {"message": "Folder organized successfully", "organized_count": moved}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))