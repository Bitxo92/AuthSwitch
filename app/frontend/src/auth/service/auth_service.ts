import { ApiClient } from "@/auth/authswitch/index"
import type { User } from "../types/user"

class AuthService {
  private static instance: AuthService
  private constructor() {}

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService()
    }
    return AuthService.instance
  }

  //Getters and Setters for Access Token, Refresh Token and User Info
  getAccessToken(): string | null {
    return localStorage.getItem("accessToken")
  }

  getRefreshToken(): string | null {
    return localStorage.getItem("refreshToken")
  }

  getUserInfo(): User | null {
    const userInfo = localStorage.getItem("userInfo")
    return userInfo ? (JSON.parse(userInfo) as User) : null
  }

  setAccessToken(token: string): void {
    localStorage.setItem("accessToken", token)
  }

  setRefreshToken(token: string): void {
    localStorage.setItem("refreshToken", token)
  }

  setUserInfo(user: User): void {
    localStorage.setItem("userInfo", JSON.stringify(user))
  }

  //Onboarding Methods
  async loginUser(username: string, password: string) {
    localStorage.clear() // Clear any existing tokens and user info before login
    const login_response = await ApiClient.login(username, password)
    // destructure the login response to get access_token and refresh_token
    const { access_token, refresh_token } = login_response
    // set the access_token and refresh_token in sessionStorage to be retreived for use in authorization headers for API calls
    this.setAccessToken(access_token)
    this.setRefreshToken(refresh_token)

    // get the user info from the API and set it in localStorage
    const user_response = await ApiClient.getLoggedUserInfo(access_token)
    this.setUserInfo(user_response!)
  }

  async refreshTokens() {
    const refreshToken = this.getRefreshToken()
    if (!refreshToken) {
      throw new Error("No refresh token found")
    }
    const refresh_response = await ApiClient.refreshToken(refreshToken)
    const { access_token, refresh_token } = refresh_response
    this.setAccessToken(access_token)
    this.setRefreshToken(refresh_token)
  }

  async logoutUser() {
    const accessToken = this.getAccessToken()
    await ApiClient.logout(accessToken ?? "")
    localStorage.clear()
  }

  //Fetch Wrapper that on 401 (Unauthorized) will attempt to refresh the access token and retry the request
  async authorizedFetch<TArgs extends unknown[], TReturn>(
    fn: (...args: TArgs) => Promise<TReturn>,
    ...args: TArgs
  ): Promise<TReturn> {
    try {
      return await fn(...args)
    } catch (error) {
      if (error instanceof Error && (error as any).response?.status === 401) {
        try {
          await authService.refreshTokens()
          return await fn(...args)
        } catch {
          await authService.logoutUser()
          throw error
        }
      }
      throw error
    }
  }

  //Auth Helper Methods

  hasRequiredRole(RequiredRole: string): boolean {
    let user_role: string = this.getUserInfo()?.roles[0] || ""

    return RequiredRole.toLowerCase() === user_role.toLowerCase().trim()
  }

  hasRequiredPermission(RequiredPermission: string): boolean {
    let user_permissions = this.getUserInfo()?.permissions || []

    return user_permissions.includes(RequiredPermission)
  }
}

// Export only a singleton instance of AuthService to be used in AuthcontextProvider
export const authService = AuthService.getInstance()
