from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import TaskCountResponseModel, OrganizationModel, 
from app.helper import api_key_auth, get_organizations, get_workgroups

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

@app.get("/api/get_tasks_count/{dep_id}", response_model=TaskCountResponseModel, dependencies=[Depends(api_key_auth)])
async def get_tasks_count(dep_id:str):
    all_workgroups, focused_projects = get_workgroups(dep_id)
    return TaskCountResponseModel(all_workgroups=all_workgroups.data_list, focused_projects=focused_projects.data_list)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
