from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import DepartmentModel, OrganizationModel
from app.helper import api_key_auth

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping", dependencies=[Depends(api_key_auth)])
async def pong():
    return {"ping": "pong!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
