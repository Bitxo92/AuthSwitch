import type { LoginResponse } from "@/auth/types/login"
import type { AuthInterface } from "@/auth//interfaces/auth_interface"
import type { User } from "@/auth/types/user"
import type { RefreshResponse } from "../types/refresh"
import { mockLoginResponse } from "../data/login_response_mock"
import { mockUserResponse } from "../data/user_mock"
import { mockRefreshResponse } from "../data/refresh_response_mock"

export class MockAuthClient implements AuthInterface {
  async login(username: string, password: string): Promise<LoginResponse> {
    localStorage.clear()
    if (username === "user" && password === "user") {
      return mockLoginResponse
    }
    return Promise.reject(new Error("Invalid username or password"))
  }

  async refreshToken(refreshToken: string): Promise<RefreshResponse> {
    console.log(
      "MockAuthClient: refreshToken called with refreshToken:",
      refreshToken
    )
    return mockRefreshResponse
  }

  async logout(accessToken: string, refreshToken: string): Promise<void> {
    console.log("MockAuthClient: logout called with accessToken:", accessToken)
    console.log(
      "MockAuthClient: logout called with refreshToken:",
      refreshToken
    )
    localStorage.clear()
    return Promise.resolve()
  }

  async getLoggedUserInfo(accessToken: string): Promise<User | null> {
    console.log(
      "MockAuthClient: getLoggedUserInfo called with accessToken:",
      accessToken
    )
    return mockUserResponse
  }
}
