import type { LoginResponse } from "../types/login"
import type { RefreshResponse } from "../types/refresh"
import type { User } from "../types/user"

export interface AuthInterface {
  login: (username: string, password: string) => Promise<LoginResponse>
  refreshToken: (refreshToken: string) => Promise<RefreshResponse>
  logout: (accessToken: string, refreshToken: string) => void
  getLoggedUserInfo: (accessToken: string) => Promise<User | null>
}
