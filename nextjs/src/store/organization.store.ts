import { create } from "zustand";
import { IOrganizationState } from "./interface/organization.interface";
import { OrganizationSlice } from "./slices/organization.slice";
import { OrganizationProjectSlice } from "./slices/organization-project.slice";
import { IOrganizationProjectState } from "./interface/organization-project.interface";

export const useOrganizationStore = create<IOrganizationState & IOrganizationProjectState>((...args) => ({
  ...OrganizationSlice(...args),
  ...OrganizationProjectSlice(...args)
}))
