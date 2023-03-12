import { StateCreator } from "zustand";
import { IOrganizationProjectState } from "../interface/organization-project.interface";

export const OrganizationProjectSlice: StateCreator<IOrganizationProjectState> = (set, get) => ({
  selectedDepartmentId: null,
  departmentIdToProject: {},

  currentDepartmentProject() {
    const { departmentIdToProject, selectedDepartmentId } = get()

    if (selectedDepartmentId == null) {
      return null
    }

    return departmentIdToProject?.[selectedDepartmentId] ?? null
  },

  addDepartmentProject(departmentId, departmentProject) {
    const departmentIdToProject = get().departmentIdToProject
    set({
      departmentIdToProject: {
        ...departmentIdToProject,
        [departmentId]: departmentProject
      }
    })
  },

  setSelectedDepartmentId(departmentId) {
    set({ selectedDepartmentId: departmentId })
  },
})