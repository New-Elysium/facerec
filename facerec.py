import asyncio
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import aiohttp
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

async def fetch_image_bytes(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=400, detail=f"Failed to fetch image from {url}")
            return await response.read()

def image_to_encoding(file: UploadFile):
    image = face_recognition.load_image_file(file.file)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        raise HTTPException(status_code=400, detail=f"No face found in {file.filename}")
    return encodings[0]



@app.post("/compare")
async def compare_faces(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        encoding1 = image_to_encoding(file1)
        encoding2 = image_to_encoding(file2)
        result = face_recognition.compare_faces([encoding1], encoding2)[0]
        return {"match": bool(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare_urls")
async def compare_faces_by_url(request: Request):

    body = await request.json()
    url1 = body.get("url1")
    url2 = body.get("url2")

    if not url1 or not url2:
        raise HTTPException(status_code=422, detail="Both 'url1' and 'url2' must be provided.")

    # Concurrent image downloads using anyio
    img_bytes1, img_bytes2 = await asyncio.gather(
        fetch_image_bytes(url1),
        fetch_image_bytes(url2)
    )

    # Load using face_recognition (internally uses PIL + numpy)
    img1 = face_recognition.load_image_file(io.BytesIO(img_bytes1))
    img2 = face_recognition.load_image_file(io.BytesIO(img_bytes2))


    enc1 = face_recognition.face_encodings(img1)
    enc2 = face_recognition.face_encodings(img2)

    if not enc1 or not enc2:
        raise HTTPException(status_code=400, detail="No face found in one or both images.")

    match = face_recognition.compare_faces([enc1[0]], enc2[0])[0]
    return JSONResponse(content={"match": bool(match)})


@app.get("/")
async def root():
    return FileResponse("index.html")