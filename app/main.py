import os
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import shutil

app = FastAPI()

origins = [
    "http://localhost:3000",  # URL de tu aplicación Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory="files"), name="files")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    os.makedirs("files", exist_ok=True)
    file_location = f"files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"url": f"http://localhost:8000/files/{file.filename}"}

@app.get("/get_report/")
async def get_report(image_url: str):
    radiological_report = """
    Informe Radiológico:

    Paciente: Juan Pérez
    Fecha del Estudio: 12 de junio de 2024
    Modalidad: Radiografía de Tórax

    Hallazgos:
    - Pulmones: Volúmenes pulmonares dentro de los límites normales. No se observan infiltrados, consolidaciones
      ni masas.
    - Corazón: Tamaño y silueta cardíaca normales.
    - Mediastino: No se observan adenopatías ni masas mediastínicas.
    - Diafragma: Contornos diafragmáticos normales.
    - Pleura: No se observa derrame pleural ni neumotórax.

    Impresión:
    - Radiografía de tórax normal. No se identifican hallazgos patológicos significativos.

    Recomendaciones:
    - Continuar con controles rutinarios según indicación médica.
    """
    return JSONResponse(content={"report": radiological_report})