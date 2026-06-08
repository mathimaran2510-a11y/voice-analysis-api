from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API Working"}

@app.post("/analyze")
def analyze():
    return {
        "stress_level": "Moderate",
        "emotion": "Neutral",
        "confidence": 82
    }