import axiosInstance from "@/lib/axios";
import { useLayoutStore } from "@/store/layout.store";
import { useOrganizationStore } from "@/store/organization.store";
import { IOrganizationResponse } from "@/types/organization";

export async function fetchOrganization(): Promise<IOrganizationResponse> {
  const { setIsLoading } = useLayoutStore.getState()
  const { setDepartment } = useOrganizationStore.getState()
  setIsLoading(true)
  const { data } = await axiosInstance.get<IOrganizationResponse>('/get_organizations')
  setDepartment(data.dep_list)
  setIsLoading(false)
  return data
}
