export interface IOrganizationResponse {
  dep_list: Department[]
}

export interface IDepartmentTaskListResponse {
  all_workgroups: Project[]
  focused_projects: Project[]
}

export type Department = {
  dep_id: string,
  dep_name: string,
  dep_head_id: string,
  dep_head_name: string,
  dep_head_pos: string,
  parent: string | null
}

export type DepartmentProject = IDepartmentTaskListResponse

export type Project = {
  dep_id: string,
  workgroup_id: string,
  workgroup_name: string,
  num_not_start: number,
  num_delay: number,
  num_on_plan: number,
  num_completed: number,
  status1: string | null,
  status2: string | null
}
