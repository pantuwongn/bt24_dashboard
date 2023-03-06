import { create } from "zustand";
import { IOrganizationState } from "./interface/organization.interface";
import { OrganizationSlice } from "./slices/organization.slice";

export const useOrganizationStore = create<IOrganizationState>((...args) => ({
  ...OrganizationSlice(...args)
}))
