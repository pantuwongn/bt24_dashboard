import { StateCreator } from "zustand";
import { IUserState } from "../interface/user.interface";

export const UserSlice: StateCreator<IUserState> = (set, get) => ({
  user: { name: 'Voramet.C' },

  setUser(user) {
    set({ user })
  },
})