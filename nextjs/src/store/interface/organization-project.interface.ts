import { DepartmentProject } from "@/types/organization";

export interface IOrganizationProjectState {
  selectedDepartmentId: string | null
  departmentIdToProject: Record<string, DepartmentProject>

  currentDepartmentProject: () => DepartmentProject | null

  addDepartmentProject: (departmentId: string, departmentProject: DepartmentProject) => void
  setSelectedDepartmentId: (departmentId: string) => void
}