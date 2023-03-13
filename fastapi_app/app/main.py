import threading
import time
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import TaskCountResponseModel, OrganizationModel
from app.helper import api_key_auth, get_organizations, get_workgroups, query_task

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEP_LIST = []
WG_LIST = []

class BackgroundTasks(threading.Thread):
    def run(self):
        while True:
            query_task(DEP_LIST, WG_LIST)
            time.sleep(120)
t = BackgroundTasks()
t.start()

@app.get("/api/ping", dependencies=[Depends(api_key_auth)])
async def pong():
    print(len(DEP_LIST))
    print(len(WG_LIST))
    return {"ping": "pong!"}

@app.get("/api/get_organizations", response_model=OrganizationModel, dependencies=[Depends(api_key_auth)])
async def get_organizations_wrapper():
    idx = min(len(DEP_LIST), len(WG_LIST))
    if idx > 0:
        return DEP_LIST[idx-1]
    else:
        return OrganizationModel(dep_list=None)

@app.get("/api/get_tasks_count/{dep_id}", response_model=TaskCountResponseModel, dependencies=[Depends(api_key_auth)])
async def get_tasks_count(dep_id:str):
    idx = min(len(DEP_LIST), len(WG_LIST))
    if idx > 0 and dep_id in WG_LIST[idx-1]:
        return WG_LIST[idx-1][dep_id]
    else:
        return TaskCountResponseModel(all_workgroups=None, focused_projects=None)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
