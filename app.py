from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import librosa
import numpy as np
import joblib

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

# Load AI Model
model = joblib.load("emotion_model.pkl")
encoder = joblib.load("label_encoder.pkl")

@app.get("/")
def home():
    return {"message": "Emotion AI API Running"}

@app.post("/analyze")
async def analyze(audio: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, audio.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await audio.read())

    # Load Audio
    y, sr = librosa.load(file_path, sr=None)

    # Extract MFCC
    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=13
    )

    mfcc_mean = np.mean(mfcc.T, axis=0)

    # Predict Emotion
    prediction = model.predict([mfcc_mean])

    emotion = encoder.inverse_transform(prediction)[0]

    return {
        "emotion": emotion,
        "confidence": 77
    }
