import os
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auction Marketplace")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/var/data/uploads")
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

# Mount static files for uploaded images
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "service": "auction-marketplace"}


@app.post("/test-upload")
async def test_upload(file: UploadFile = File(...)):
    """Test upload endpoint to verify persistent disk"""
    # Generate random filename
    file_extension = file.filename.split(".")[-1]
    random_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = Path(UPLOAD_DIR) / random_filename
    
    # Save file
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return {
            "message": "File uploaded successfully",
            "filename": random_filename,
            "path": str(file_path),
            "url": f"/uploads/{random_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/test-upload/{filename}")
async def get_uploaded_file(filename: str):
    """Retrieve uploaded file to verify persistence"""
    file_path = Path(UPLOAD_DIR) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Auction Marketplace API",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "test_upload": "/test-upload (POST)",
            "get_file": "/test-upload/{filename} (GET)"
        }
    }
