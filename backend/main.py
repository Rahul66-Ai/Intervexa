from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil


app = FastAPI()


# Resume upload folder
UPLOAD_FOLDER = Path("backend/uploads")

# Folder doesn't exist, create it
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Welcome to Intervexa!",
        "status": "Backend is running"
    }


@app.post("/upload-resume")
def upload_resume(file: UploadFile = File(...)):

    # Allowed file types
    allowed_extensions = [".pdf", ".docx"]

    file_extension = Path(file.filename).suffix.lower()

    # Check file type
    if file_extension not in allowed_extensions:
        return {
            "success": False,
            "message": "Only PDF and DOCX files are allowed."
        }

    # Create file path
    file_path = UPLOAD_FOLDER / file.filename

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "message": "Resume uploaded successfully!",
        "filename": file.filename
    }