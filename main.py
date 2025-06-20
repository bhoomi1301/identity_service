from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import IdentifyRequest
from database import SessionLocal, engine
from models import Base
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def custom_http_error_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Access Denied. You do not have clearance for this operation."}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Anomaly Detected. Transmission incomplete."}
    )

@app.post("/identify")
def identify(data: IdentifyRequest):
    if not data.email and not data.phoneNumber:
        raise HTTPException(status_code=400, detail="Either email or phoneNumber must be provided.")
    
    with SessionLocal() as db:
        return crud.handle_identify_logic(db, data.email, data.phoneNumber)
