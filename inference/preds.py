from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from flair.data import Sentence
from flair.models import TextClassifier
from api_utils import get_latest_model_version_from_s3,download_model_from_s3
import os

app = FastAPI()

def check_or_get_latest_model():
    model_version=get_latest_model_version_from_s3()
    if os.path.exists(f"model_v{model_version}.pt"):
        model_path = f"model_v{model_version}.pt"
        classifier = TextClassifier.load(model_path)
        return classifier
    download_model_from_s3(s3_bucket=os.get_env("model_bucket"),s3_path=f"models/{f'model_v{model_version}.pt'}")
    model_path = f"model_v{model_version}.pt"
    classifier = TextClassifier.load(model_path)
    return classifier

@app.get("/api/health")
def api_ping():
    return "server is up & running"

class InputText(BaseModel):
    text: str

@app.post("api/predict")
async def predict(input_text: InputText):
    try:
        classifier = check_or_get_latest_model()
        sentence = Sentence(input_text.text)
        classifier.predict(sentence)
        predicted_label = sentence.labels[0].value
        confidence = sentence.labels[0].score
        return {"predicted_label": predicted_label, "confidence": confidence}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
