from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API Working"}

@app.post("/analyze")
async def analyze(audio: UploadFile = File(...)):
    
    # Just proving the upload works
    file_name = audio.filename

    return {
        "stress_level": "Moderate",
        "emotion": "Neutral",
        "confidence": 82,
        "received_file": file_name
    }
