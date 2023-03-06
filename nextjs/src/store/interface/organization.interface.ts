import { Department } from "@/types/organization";

export interface IOrganizationState {
  departmentList: Department[]
  setDepartment: (departmentList: Department[]) => void
}
