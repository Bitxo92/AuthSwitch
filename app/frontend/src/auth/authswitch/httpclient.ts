import type { LoginResponse } from "@/auth/types/login"
import type { AuthInterface } from "@/auth//interfaces/auth_interface"
import type { User } from "@/auth/types/user"
import type { RefreshResponse } from "../types/refresh"

export class AuthHttpClient implements AuthInterface {
  private readonly BASE_URL = "http://localhost:8000"

  async login(username: string, password: string): Promise<LoginResponse> {
    const response = await fetch(`${this.BASE_URL}/auth/main/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error("Network error:", error)
        throw error
      })
    return response.data as LoginResponse
  }
  async refreshToken(refreshToken: string): Promise<RefreshResponse> {
    const response = await fetch(`${this.BASE_URL}/auth/refresh`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error("Network error:", error)
        throw error
      })
    return response.data as RefreshResponse
  }
  async logout(access_token: string): Promise<void> {
    fetch(`${this.BASE_URL}/auth/logout`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
    }).catch((error) => {
      console.error("Network error:", error)
      throw error
    })
  }
  async getLoggedUserInfo(access_token: string): Promise<User> {
    const response = await fetch(`${this.BASE_URL}/auth/me`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error("Network error:", error)
        throw error
      })
    return response.data as User
  }
}
