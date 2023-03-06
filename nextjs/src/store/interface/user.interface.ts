import { User } from "@/types/user.type";

export interface IUserState {
  user: User,

  setUser: (user: User) => void
}