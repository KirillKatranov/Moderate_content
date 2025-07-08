from typing import Union
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
import requests
from Schemas import ModerateResponseOK, ModerateResponseRejected
from config import settings  # settings.HF_TOKEN



if not settings.HF_TOKEN:
    raise RuntimeError("HF_TOKEN не загружен")

app = FastAPI()

url = "https://api-inference.huggingface.co/models/giacomoarienti/nsfw-classifier"
headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}

@app.post("/moderate", response_model=Union[ModerateResponseOK, ModerateResponseRejected])
async def moderate_image(file: UploadFile = File(...)):
    # Проверка формата
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only .jpg and .png files are allowed.")

    image_bytes = await file.read()

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {settings.HF_TOKEN}",
            "Content-Type": file.content_type
        },
        data=image_bytes
    )

    if response.status_code != 200:
        print("Hugging Face status code:", response.status_code)
        print("Hugging Face response text:", response.text)
        raise HTTPException(status_code=500, detail="Failed to process image with Hugging Face API.")

    result = response.json()
    print("Hugging Face result:", result)

    # Проверка структуры ответа
    # Пример: [{'label': 'nsfw', 'score': 0.9876}, ...]
    nsfw_score = 0
    for p in result:
        if p["label"].lower() == "nsfw":
            nsfw_score = p["score"]

    if nsfw_score > 0.7:
        return JSONResponse(content={"status": "REJECTED", "reason": "NSFW content"})
    else:
        return {"status": "OK"}
