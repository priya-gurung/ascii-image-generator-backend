from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from bg_remove import remove_bg
import uuid
import os
from app import image_to_ascii, ascii_to_image
import shutil
from PIL import Image
from fastapi import HTTPException

app = FastAPI()

os.makedirs("uploads", exist_ok=True)

def cleanup(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ascii-image-generator-frontend-e7uzce6ev-priya-gurungs-projects.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp"
}

@app.get("/")
async def health():
    return {"status": "ok"}


@app.post("/generate")
async def generate_ascii(background_tasks: BackgroundTasks, file: UploadFile = File(...), width: int = Form(120), charset: str = Form("classic")):
    print("Request recieved")
    print(file.filename)

    file_id = str(uuid.uuid4())

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPG and WEBP images are allowed."
        )
    
    ext = os.path.splitext(file.filename)[1].lower()
    if not ext:
        ext = ".png"

    path = f"uploads/{file_id}_input{ext}"
    subject_path = f"uploads/{file_id}_subject.png"
    ascii_path = f"uploads/{file_id}_ascii.png"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        remove_bg(path, subject_path)

        #remove transparent padding
        img = Image.open(subject_path)
        bbox = img.getbbox()

        if bbox:
            img = img.crop(bbox)
        img.save(subject_path)

        #convert to ascii image
        ascii_art = image_to_ascii(subject_path, width, charset)

        ascii_to_image(
            ascii_art,
            ascii_path
        )
    
    except Exception as e:
        cleanup(path, subject_path, ascii_path)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    background_tasks.add_task(
        cleanup,
        path,
        subject_path,
        ascii_path
    )

    return FileResponse(
        ascii_path,
        media_type="image/png",
        filename="ascii_output.png"
    )