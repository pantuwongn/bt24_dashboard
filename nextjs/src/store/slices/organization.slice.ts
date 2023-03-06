import { StateCreator } from "zustand";
import { IOrganizationState } from "../interface/organization.interface";

export const OrganizationSlice: StateCreator<IOrganizationState> = (set, get) => ({
  departmentList: [],

  setDepartment(departmentList) {
    set({ departmentList })
  },
})
