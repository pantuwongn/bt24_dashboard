import { create } from "zustand";
import { IUserState } from "./interface/user.interface";
import { UserSlice } from "./slices/user.slice";

export const useUserStore = create<IUserState>((...args) => ({
  ...UserSlice(...args)
}))
