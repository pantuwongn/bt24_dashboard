export interface IOrganizationResponse {
  dep_list: Department[]
}

export type Department = {
  dep_id: string,
  dep_name: string,
  dep_head_id: string,
  dep_head_name: string,
  dep_head_pos: string,
  parent: string | null
}
