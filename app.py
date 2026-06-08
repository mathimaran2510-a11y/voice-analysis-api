from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import librosa
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "API Working"}

@app.post("/analyze")
async def analyze(audio: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, audio.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await audio.read())

    y, sr = librosa.load(file_path, sr=None)

    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=13
    )

    mfcc_mean = np.mean(mfcc, axis=1)

    return {
        "message": "Audio Processed Successfully",
        "sample_rate": int(sr),
        "audio_length_seconds": round(len(y)/sr, 2),
        "mfcc_features": mfcc_mean.tolist()
    }
