import os
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from dotenv import load_dotenv
import tempfile
import shutil
from pathlib import Path

# Import our distance calculation module
from ..get_distance import process_csv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("Google Maps API key not found in environment variables")

app = FastAPI(title="Address Distance Calculator")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a temporary directory for file storage
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

@app.post("/api/upload")
async def upload_file(file: UploadFile):
    """
    Upload a CSV file containing address pairs.
    The CSV must have columns: address1, address2
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    # Save uploaded file
    input_path = TEMP_DIR / f"input_{file.filename}"
    output_path = TEMP_DIR / f"output_{file.filename}"
    
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Validate CSV structure
        df = pd.read_csv(input_path)
        required_columns = ['address1', 'address2']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400,
                detail=f"CSV must contain columns: {', '.join(required_columns)}"
            )
        
        # Process the file
        process_csv(str(input_path), str(output_path), API_KEY)
        
        return {"message": "File processed successfully", "filename": file.filename}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download the processed CSV file."""
    file_path = TEMP_DIR / f"output_{filename}"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=f"processed_{filename}",
        media_type="text/csv"
    )

@app.on_event("startup")
async def startup_event():
    """Create temporary directory on startup if it doesn't exist."""
    TEMP_DIR.mkdir(exist_ok=True)

# Optional: Clean up old files periodically
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up temporary files on shutdown."""
    shutil.rmtree(TEMP_DIR, ignore_errors=True) 