import axiosInstance from "@/lib/axios";
import { useOrganizationStore } from "@/store/organization.store";
import { IDepartmentTaskListResponse, IOrganizationResponse } from "@/types/organization";

export async function fetchOrganization(): Promise<IOrganizationResponse> {
  const { setDepartment } = useOrganizationStore.getState()
  const { data } = await axiosInstance.get<IOrganizationResponse>('/get_organizations')
  setDepartment(data.dep_list)
  return data
}

export async function fetchTaskByDepartmentId(departmentId: string): Promise<IDepartmentTaskListResponse> {
  const { addDepartmentProject } = useOrganizationStore.getState()
  const { data } = await axiosInstance.get<IDepartmentTaskListResponse>(`/get_tasks_count/${departmentId}`)
  addDepartmentProject(departmentId, data)
  return data
}
