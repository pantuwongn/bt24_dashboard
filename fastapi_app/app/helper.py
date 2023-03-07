import os
import requests
import json
from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Depends
from typing import List, Dict

from app.models import DepartmentModel, OrganizationModel

X_API_KEY = APIKeyHeader(name="X-API-Key")
api_key = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BT_HOOK_URL")

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, 'config.json')) as f:
    config = json.load(f)


def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
    # this function is used to validate X-API-KEY in request header
    # if the sent X-API-KEY in header is not existed in the config file
    #   reject access
    if x_api_key != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )

def get_user( uid: str ) -> dict:
    ''' This function get user data from Bitrix24 backend from user id
    '''
    url = f'{BASE_URL}/user.get.json?ID={uid}'     
    r = requests.get(url)
    rj = r.json()
    if r.status_code != 200 or 'result' not in rj:
        return None
    else:
        return rj['result']

def get_user_in_dep( dep_id: str ) ->List[dict]
    ''' This function returns all user in department with department id
    '''
    url = f'{BASE_URL}/user.get.json?order[ID]=ASC&UF_DEPARTMENT={dep_id}'
    r = requests.get(url)
    rj = r.json()
    if r.status_code != 200 or 'result' not in rj:
        return None
    else:
        all_users = rj['result']
        while 'next' in rj:
            last_id = all_users[-1]['ID']
            url = f'{url}&filter[>ID]={last_id}'
            r = requests.get(url)
            rj = r.json()
            if r.status_code != 200 or 'result' not in rj:
                break
            else:
                all_users.extend(rj['result'])
        return all_users

def get_workgroup_in_dep( dep_id:str ) -> List[dict]
    ''' This function returns a list of workgroup(project) in department
    '''

    # get user in department
    all_users = get_user_in_dep( dep_id )
    all_user_ids = [x['ID'] for x in all_users]

    # query workgroup (project) where owner_id in all_user_ids
    url = f'{BASE_URL}/sonet_group.get.json?order[ID]=ASC&OWNER_ID={all_user_ids}'
    r = requests.get(url)
    rj = r.json()
    if r.status_code != 200 or 'result' not in rj:
        return None
    else:
        all_workgroups = rj['result']
        while 'next' in rj:
            last_id = all_workgroups[-1]['ID']
            url = f'{url}&filter[>ID]={last_id}'
            r = requests.get(url)
            rj = r.json()
            if r.status_code != 200 or 'result' not in rj:
                break
            else:
                all_workgroups.extend(rj['result'])
        return all_workgroups

def get_users_in_workgroup( wg_id:str ) -> List[dict]
    ''' This function returns a list of users in department
    '''

    # get user data in workgroup
    url = f'{BASE_URL}/sonot_group.user.get.json?ID={wg_id}&order[ID]=ASC'
    r = requests.get(url)
    rj = r.json()
    if r.status_code != 200 or 'result' not in rj:
        return None
    else:
        all_user_data = rj['result']
        all_user_ids = [x['USER_ID'] for x in all_user_data]
        url = f'{BASE_URL}/user.get.json?order[ID]=ASC&ID={all_user_ids}'
        all_users = rj['result']
        while 'next' in rj:
            last_id = all_users[-1]['ID']
            url = f'{url}&filter[>ID]={last_id}'
            r = requests.get(url)
            rj = r.json()
            if r.status_code != 200 or 'result' not in rj:
                break
            else:
                all_users.extend(rj['result'])
        return all_users

def get_organizations():
    ''' This function call Bitrix24 endpoints to get organization information
    '''

    # transfrom data from config
    dep_data_dict = {}
    all_dep_data = config.get('org', None)
    if all_dep_data:
        for dep_data in all_dep_data:
            dep_data_dict[dep_data['department_id']] = dep_data

    # get all departments
    url = f'{BASE_URL}/department.get.json?order[ID]=ASC'
    r = requests.get(url)
    rj = r.json()
    if r.status_code != 200 or 'result' not in rj:
        return OrganizationModel(dep_list = None)
    else:
        all_deps = rj['result']
        while 'next' in rj:
            last_id = all_deps[-1]['ID']
            url = f'{url}&filter[>ID]={last_id}'
            r = requests.get(url)
            rj = r.json()
            if r.status_code != 200 or 'result' not in rj:
                break
            else:
                all_deps.extend(rj['result'])

        dep_list = []
        for dep in all_deps:
            dep_id = dep.get('ID', None)
            if dep_id not in dep_data_dict:
                continue
            dep_name = dep_data_dict[dep_id].get('description', None)
            dep_head_id = dep_data_dict[dep_id].get('manager_id', None)
            dep_head_pos = dep_data_dict[dep_id].get('position_text', None)
            parent = dep.get('PARENT', None)
            dep_head = get_user(dep_head_id)
            if not dep_head:
                dep_head_name = None
            else:
                dep_head_name = dep_head.get('name', None)
            
            dep_obj = DepartmentModel(dep_id = dep_id,
                                        dep_name = dep_name,
                                        dep_head_id = dep_head_id,
                                        dep_head_name = dep_head_name,
                                        dep_head_pos = dep_head_pos,
                                        parent = parent
                                    )
            dep_list.append(dep_obj)
        return OrganizationModel(dep_list = dep_list)