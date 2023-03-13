from pydantic import BaseModel
from typing import List, Optional, Dict


class DepartmentModel( BaseModel ):
    ''' A model of department which is an element of 
         a list of organization 
    '''

    dep_id: Optional[str]
    dep_name: Optional[str]
    dep_head_id: Optional[str]
    dep_head_name: Optional[str]
    dep_head_pos: Optional[str]
    parent: Optional[str]

class OrganizationModel( BaseModel ):
    ''' A model of organization section
    '''

    # organization is a list of deparntment
    dep_list: Optional[List[DepartmentModel]]


class TaskDataModel( BaseModel ):
    ''' A model of data to be shown for each workgroup
    '''

    dep_id: str
    workgroup_id: Optional[str]
    workgroup_name: Optional[str]
    num_not_start: int
    num_delay: int
    num_on_plan: int
    num_completed: int
    status1: Optional[str]
    status2: Optional[str]
    workload: Optional[Dict]
    kpi: Optional[Dict]
    budget: Optional[Dict]

class TaskDataListModel( BaseModel ):
    ''' A model for workgroup section
    '''

    data_list: Optional[List[TaskDataModel]]

class TaskCountResponseModel( BaseModel ):
    ''' A model to response about task count
    '''
    all_workgroups: Optional[List[TaskDataModel]]
    focused_projects: Optional[List[TaskDataModel]]