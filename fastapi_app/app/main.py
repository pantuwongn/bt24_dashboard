from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import DepartmentModel, OrganizationModel
from app.helper import api_key_auth, get_organizations

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

@app.get("/api/get_organizations", response_model=OrganizationModel, dependencies=[Depends(api_key_auth)])
async def get_organizations_wrapper():
    org_obj = get_organizations()
    return org_obj

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
