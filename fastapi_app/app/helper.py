import os
import requests
import json
from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Depends
from typing import List, Dict

from app.models import DepartmentModel, OrganizationModel, TaskDataListModel, TaskDataModel

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
            status_code=401,
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

def get_user_in_dep( dep_id: str ) -> List[dict]:
    ''' This function returns all user in department with department id
    '''
    url = f'{BASE_URL}/user.get.json?ORDER[ID]=ASC&UF_DEPARTMENT={dep_id}'
    r = requests.get(url)
    rj = r.json()
    if r.status_code != 200 or 'result' not in rj:
        return None
    else:
        all_users = rj['result']
        while 'next' in rj:
            last_id = all_users[-1]['ID']
            url = f'{url}&FILTER[>ID]={last_id}'
            r = requests.get(url)
            rj = r.json()
            if r.status_code != 200 or 'result' not in rj:
                break
            else:
                all_users.extend(rj['result'])
        return all_users

def get_workgroup_in_dep( dep_id:str ) -> List[dict]:
    ''' This function returns a list of workgroup(project) in department
    '''

    # get user in department
    all_users = get_user_in_dep( dep_id )
    all_user_ids = [x['ID'] for x in all_users]

    # query workgroup (project) where owner_id in all_user_ids
    all_workgroups = []
    for user_id in all_user_ids:
        url = f'{BASE_URL}/sonet_group.get.json?ORDER[ID]=ASC&FILTER[OWNER_ID]={user_id}'
        r = requests.get(url)
        rj = r.json()
        if r.status_code != 200 or 'result' not in rj:
            continue
        else:
            all_workgroups.extend( rj['result'] )
            while 'next' in rj:
                last_id = all_workgroups[-1]['ID']
                url = f'{url}&FILTER[>ID]={last_id}'
                r = requests.get(url)
                rj = r.json()
                if r.status_code != 200 or 'result' not in rj:
                    break
                else:
                    all_workgroups.extend(rj['result'])
    return all_workgroups

def get_users_in_workgroup( wg_id:str ) -> List[dict]:
    ''' This function returns a list of users in department
    '''

    # get user data in workgroup
    url = f'{BASE_URL}/sonet_group.user.get.json?ID={wg_id}&ORDER[ID]=ASC'
    r = requests.get(url)
    rj = r.json()
    if r.status_code != 200 or 'result' not in rj:
        return None
    else:
        all_user_data = rj['result']
        all_user_ids = [x['USER_ID'] for x in all_user_data]
        all_user = []
        for user_id in all_user_ids:
            user = get_user(user_id)
            if user:
                all_user.append(user)

        return all_user

def get_tasks_in_workgroup( wg_id: str ) -> List[dict]:
    ''' This function returns a list of tasks in workgroup
    '''

    url = f'{BASE_URL}/task.item.list?ORDER[ID]=ASC&FILTER[GROUP_ID]={wg_id}'
    r = requests.get(url)
    rj = r.json()
    if r.status_code != 200 or 'result' not in rj:
        return None
    else:
        all_tasks = rj['result']
        while 'next' in rj:
            last_id = all_tasks[-1]['ID']
            url = f'{url}&FILTER[>ID]={last_id}'
            r = requests.get(url)
            rj = r.json()
            if r.status_code != 200 or 'result' not in rj:
                break
            else:
                all_tasks.extend(rj['result'])
        return all_tasks

def get_comment_in_task( task_id: str ) -> List[dict]:
    pass

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
    url = f'{BASE_URL}/department.get.json'
    r = requests.get(url)
    rj = r.json()
    if r.status_code != 200 or 'result' not in rj:
        return OrganizationModel(dep_list = None)
    else:
        all_deps = rj['result']

        dep_list = []
        for dep in all_deps:
            dep_id = dep.get('ID', None)
            if dep_id not in dep_data_dict:
                continue
            dep_name = dep_data_dict[dep_id].get('description', None)
            dep_head_id = dep_data_dict[dep_id].get('manager_id', None)
            dep_head_pos = dep_data_dict[dep_id].get('position_text', None)
            parent = dep.get('PARENT', None)
            dep_head = get_user(dep_head_id)[0]
            if not dep_head:
                dep_head_name = None
            else:
                f_name = dep_head.get('NAME', None)
                l_name = dep_head.get('LAST_NAME', None)
                if f_name and l_name:
                    dep_head_name = f'{f_name} {l_name}'
                elif f_name:
                    dep_head_name = f_name
                elif l_name:
                    dep_head_name = l_name
                else:
                    dep_head_name = None

            dep_obj = DepartmentModel(dep_id = dep_id,
                                        dep_name = dep_name,
                                        dep_head_id = dep_head_id,
                                        dep_head_name = dep_head_name,
                                        dep_head_pos = dep_head_pos,
                                        parent = parent
                                    )
            dep_list.append(dep_obj)
        return OrganizationModel(dep_list = dep_list)

def get_workgroups( dep_id: str ) -> List[dict]:
    ''' This function returns workgroups information to display in dashboard
    '''

    # get workgroup in department with department with dep_id
    #   we check if owner_id of each workgroup in the department
    workgroups = get_workgroup_in_dep( dep_id )

    # for each workgroup, construct data and put in list
    all_data_list = []
    focus_data_list = []
    for workgroup in workgroups:
        workgroup_id = workgroup.get('ID', None)
        workgroup_name = workgroup.get('NAME', None)

        # get tasks in workgroup
        all_tasks = get_tasks_in_workgroup( workgroup_id )

        # count taks status
        num_not_start = 0
        num_delay = 0
        num_on_plan = 0
        num_completed = 0
        comment_dict = {}
        for task in all_tasks:
            task_id = task.get('ID', None)
            status = task.get('STATUS', None)
            real_status = taks.get('REAL_STATUS', None)
            if not status or not real_status or not task_id
                continue

            if real_status == '5':
                num_completed += 1
            elif status == '-1':
                num_delay += 1
            elif real_status in ['1', '2']
                num_not_start += 1
            elif real_status in ['3', '4', '6', '7']:
                num_on_plan += 1
        
            # get comment in task
            all_comments = get_comment_in_task( task['ID'] )

        taskDataObj = TaskDataModel( dep_id = dep_id,
                                        workgroup_id = workgroup_id,
                                        workgroup_name = workgroup_name,
                                        num_not_start = num_not_start,
                                        num_delay = num_delay,
                                        num_on_plan = num_on_plan,
                                        num_completed = num_completed,
                                        status1 = ''
                                        status2 = ''
                                    )
        all_data_list.append(taskDataObj)
        if workgroup_id in config['focused_project_id'] or \
            'focused_project_id' not in config or \
            not config['focused_project_id']:
            focus_data_list.append(taskDataObj)
    return TaskDataListModel(data_list=all_data_list), TaskDataListModel(data_list=focus_data_list)