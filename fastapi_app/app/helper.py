import os
import time
import requests
import json
import datetime
from random import randint
from math import ceil
from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Depends
from typing import List, Dict

from app.models import DepartmentModel, OrganizationModel, TaskDataListModel, TaskDataModel, TaskCountResponseModel

X_API_KEY = APIKeyHeader(name="X-API-Key")
api_key = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BT_HOOK_URL")

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, 'config.json')) as f:
    config = json.load(f)


def _generate_kpi():
    ''' this function returns kpi output for mock data
    '''

    return {
        "Safety": {"actual": randint(40, 90), "plan": randint(40, 90), "unit": "Cases"},
        "Internal loss": {"actual": randint(40, 90), "plan": randint(40, 90), "unit": "kB"},
        "De-carbon": {"actual": randint(40, 90), "plan": randint(40, 90), "unit": "tCo2"},
        "MH/MP saving": {"actual": randint(40, 90), "plan": randint(40, 90), "unit": "HC"},
        "Investment": {"actual": randint(40, 90), "plan": randint(40, 90), "unit": "kB"},
        "Expense": {"actual": randint(40, 90), "plan": randint(40, 90), "unit": "kB"},
        "Cost down": {"actual": randint(40, 90), "plan": randint(40, 90), "unit": "kB/M"},
        "Overtime": {"actual": randint(40, 90), "plan": randint(40, 90), "unit": "Hrs"},
    }


def _generate_budget():
    ''' this function returns budget for mock data
    '''

    return {
        'FY': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        '1st': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        '2nd': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Jan': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Feb': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Mar': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Apr': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'May': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Jun': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Jul': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Aug': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Sep': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Oct': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Nov': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
        'Dec': {"actual": randint(3000, 6000), "plan": randint(3000, 6000)},
    }


def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """

    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return str(int(ceil(adjusted_dom/7.0))) + ' ' + datetime.datetime.strftime(dt, '%b')

def get_start_and_end_date_from_calendar_week(year, calendar_week):       
    sunday = datetime.datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
    return sunday,sunday + datetime.timedelta(days=6.9)

def get_workload_period():

    period = []
    week_list = []

    today = datetime.datetime.now()
    current_week_year = datetime.datetime.strftime(today, '%W %Y')
    week = int(current_week_year.split()[0])
    year = int(current_week_year.split()[1])
    f_day, l_day = get_start_and_end_date_from_calendar_week(year, week)
    
    prev = -1
    for i in range(-2,10):
        wm = week_of_month(f_day + datetime.timedelta(days=(7*i)))
        cur = int(wm.split()[0])
        if cur < prev and cur != 1:
            cur = 1
        elif cur > prev and cur != prev + 1:
            cur -= 1
        period.append(f'{cur} {wm.split()[1]}')
        week_list.append((
            datetime.datetime.strftime(f_day + datetime.timedelta(days=(7*i)), '%Y-%m-%d'),
            datetime.datetime.strftime(l_day + datetime.timedelta(days=(7*i)), '%Y-%m-%d')
        ))
        prev = cur
    return period, week_list

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
    ''' this function returns all comments in task by task id
    '''
    url = f'{BASE_URL}/task.commentitem.getlist?TASKID={task_id}'
    r = requests.get(url)
    rj = r.json()
    if r.status_code != 200 or 'result' not in rj:
        return None
    else:
        all_comments = rj['result']
        while 'next' in rj:
            last_id = all_comments[-1]['ID']
            url = f'{url}&FILTER[>ID]={last_id}'
            r = requests.get(url)
            rj = r.json()
            if r.status_code != 200 or 'result' not in rj:
                break
            else:
                all_comments.extend(rj['result'])
        return all_comments

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

    # period and weeklist
    period, week_list = get_workload_period()
    init_workload_list = [{x:0} for x in period]


    # get workgroup in department with department with dep_id
    #   we check if owner_id of each workgroup in the department
    workgroups = get_workgroup_in_dep( dep_id )

    # for each workgroup, construct data and put in list
    all_data_list = []
    focus_data_list = []
    for workgroup in workgroups:
        workgroup_id = workgroup.get('ID', None)
        workgroup_name = workgroup.get('NAME', None)

        if not workgroup_id:
            continue

        # get tasks in workgroup
        all_tasks = get_tasks_in_workgroup( workgroup_id )

        # get user in workgroup
        all_users = get_users_in_workgroup( workgroup_id )
        workload_dict = {}
        for user in all_users:
            f_name = user[0].get('NAME', None)
            l_name = user[0].get('LAST_NAME', None)
            if f_name and l_name:
                responsible_name = f'{f_name} {l_name}'
            elif f_name:
                responsible_name = f_name
            elif l_name:
                responsible_name = l_name
            else:
                responsible_name = ''
            workload_dict[user[0]['ID']] = {
                'name': responsible_name,
                'workload': init_workload_list
            }

        # count taks status
        num_not_start = 0
        num_delay = 0
        num_on_plan = 0
        num_completed = 0
        status1 = None
        status2 = None
        comment_list = []
        for task in all_tasks:
            task_id = task.get('ID', None)
            status = task.get('STATUS', None)
            real_status = task.get('REAL_STATUS', None)
            if not status or not real_status or not task_id:
                continue

            if real_status == '5':
                num_completed += 1
            elif status == '-1':
                num_delay += 1
            elif real_status in ['1', '2']:
                num_not_start += 1
            elif real_status in ['3', '4', '6', '7']:
                num_on_plan += 1


            responsible_id = task.get('RESPONSIBLE_ID', None)
            if responsible_id in workload_dict:
                start_date_str = task.get('START_DATE_PLAN', None)
                deadline_date_str = task.get('DEADLINE', None)
                if start_date_str:
                    start_date_str = start_date_str[:10]
                if deadline_date_str:
                    deadline_date_str = deadline_date_str[:10]
                for idx, w in enumerate(week_list):
                    if ( start_date_str and w[0] >= start_date_str and deadline_date_str and w[0] <= deadline_date_str ) or \
                        ( start_date_str and w[0] >= start_date_str ) or \
                        ( deadline_date_str and w[0] <= deadline_date_str ) or \
                        ( not start_date_str and not deadline_date_str ):
                        for key in workload_dict[responsible_id]['workload'][idx].keys():
                            workload_dict[responsible_id]['workload'][idx][key] += 1

            # get comment in task
            all_comments = get_comment_in_task( task['ID'] )
            for comment in all_comments:
                d = comment['POST_DATE']
                t = comment['POST_MESSAGE']
                if '[USER' not in t:
                    comment_list.append((d,t))
        comment_list.sort()
        if comment_list:
            status1 = comment_list[0][1]
        if len(comment_list) > 2:
            status2 = comment_list[1][1]
        taskDataObj = TaskDataModel( dep_id = dep_id,
                                        workgroup_id = workgroup_id,
                                        workgroup_name = workgroup_name,
                                        num_not_start = num_not_start,
                                        num_delay = num_delay,
                                        num_on_plan = num_on_plan,
                                        num_completed = num_completed,
                                        status1 = status1,
                                        status2 = status2,
                                        workload = workload_dict,
                                        kpi = _generate_kpi(),
                                        budget = _generate_budget()
                                    )
        all_data_list.append(taskDataObj)
        if 'focused_project_id' not in config or \
            dep_id not in config['focused_project_id'] or \
            workgroup_id in config['focused_project_id'][dep_id] or \
            not config['focused_project_id'][dep_id]:
            focus_data_list.append(taskDataObj)

    return TaskDataListModel(data_list=all_data_list), TaskDataListModel(data_list=focus_data_list)

def query_task(dep_list, wg_list):

    try:
        # get organization
        s = time.time()
        ok = False
        while not ok:
            try:
                org_list = get_organizations()
                ok = True
            except Exception as e:
                print(f'Error ===> {e}')
        print(f'[thread] Get org_list ({time.time()-s} secs)')
        # for each organization
        workgroup_dict = {}
        for org in org_list.dep_list:
            dep_id = org.dep_id
            s = time.time()
            ok = False
            try:
                while not ok:
                    all_workgroups, focused_projects = get_workgroups(dep_id)
                    ok = True
            except Exception as e:
                print(f'Error ===> {e}')           
            all_obj = TaskCountResponseModel (
                all_workgroups=all_workgroups.data_list,
                focused_projects=focused_projects.data_list
            )
            workgroup_dict[dep_id] = all_obj
            print(f'[thread] Get workgroup for {org.dep_name} ({time.time()-s} secs)')
        print('[thread] Get all workgroups')
        if len(dep_list) < 10:
            dep_list.append(org_list)
        else:
            dep_list = dep_list[1:]
            dep_list.append(org_list)
    
        if len(wg_list) < 10:
            wg_list.append(workgroup_dict)
        else:
            wg_list = wg_list[1:]
            wg_list.append(workgroup_dict)

    except Exception as e:
        print(f'Error ===> {e}')

