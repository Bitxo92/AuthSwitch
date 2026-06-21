import type { AuthContextType } from "@/auth/types/auth_context"
import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from "react"
import { authService } from "@/auth/service/auth_service"
import type { User } from "@/auth/types/user"

const AuthContext = createContext<AuthContextType | undefined>(undefined)

// The Provider component that maintains React state
export function AuthProvider({ children }: { children?: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const isAuthenticated = !!user

  // Synchronize initial session state on application mount / page refresh
  useEffect(() => {
    async function initializeSession() {
      const storedUser = authService.getUserInfo()
      const hasRefreshToken = authService.getRefreshToken()

      if (storedUser && hasRefreshToken) {
        setUser(storedUser)

        try {
          await authService.refreshTokens()
          // Update user state just in case the background token refresh changed anything
          setUser(authService.getUserInfo())
        } catch (error) {
          console.error("Session restoration failed, logging out...", error)
          await authService.logoutUser()
          setUser(null)
        }
      }
      setLoading(false)
    }

    initializeSession()
  }, [])

  // --- Onboarding Authservice wrappers ---

  const login = async (username: string, password: string) => {
    setLoading(true)
    try {
      await authService.loginUser(username, password)
      setUser(authService.getUserInfo())
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    setLoading(true)
    try {
      await authService.logoutUser()
    } catch (error) {
      console.error("API logout failed, clearing local state anyway", error)
    } finally {
      setUser(null)
      setLoading(false)
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

// 3. Custom Hook exposes the context to components for use
export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
