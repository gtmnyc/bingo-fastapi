from fastapi import FastAPI, HTTPException
import dropbox
from docx import Document
import json
import os
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

# Root endpoint to confirm API is running
@app.get("/")
def read_root():
    return {"message": "FastAPI is running successfully!"}

# Dropbox credentials
APP_KEY = '99hl0e4g22uysd1'
APP_SECRET = 'w16oh618rf7u56i'
REFRESH_TOKEN = 'IJrcOdm637AAAAAAAAAAAfpY8pX22gQCwy03vc_Cg6L5m4x4yBYovmjk7aQRbQSP'
DROPBOX_FILE_PATH = '/Apps/bingo lotto/Bingo-Lotto-board.docx'
LOCAL_FILE_PATH = 'Bingo-Lotto-board.docx'

def authenticate_dropbox():
    return dropbox.Dropbox(
        oauth2_refresh_token=REFRESH_TOKEN,
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )

@app.get("/download")
def download_file():
    try:
        dbx = authenticate_dropbox()
        with open(LOCAL_FILE_PATH, "wb") as f:
            metadata, res = dbx.files_download(path=DROPBOX_FILE_PATH)
            f.write(res.content)
        return {"message": "File downloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
def process_file(numbers: list[int]):
    try:
        doc = Document(LOCAL_FILE_PATH)
        # Placeholder: Implement highlighting logic here
        doc.save(LOCAL_FILE_PATH)
        return {"message": "File processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
def upload_file():
    try:
        dbx = authenticate_dropbox()
        with open(LOCAL_FILE_PATH, "rb") as f:
            dbx.files_upload(f.read(), DROPBOX_FILE_PATH, mode=dropbox.files.WriteMode('overwrite'))
        return {"message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
