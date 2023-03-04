from pydantic import BaseModel
from typing import List, Optional


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