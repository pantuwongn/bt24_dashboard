from pydantic import BaseModel
from typing import List, Union


class DepartmentModel( BaseModel ):
    ''' A model of department which is an element of 
         a list of organization 
    '''

    dep_id: str
    dep_name: str
    dep_head_id: str
    dep_head_name: str
    dep_head_pos: str
    dep_member: List[str]

class OrganizationModel( BaseModel ):
    ''' A model of organization section
    '''

    # organization is a list of deparntment
    dep_list: List[DepartmentModel]