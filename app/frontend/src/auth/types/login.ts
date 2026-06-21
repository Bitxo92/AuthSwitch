export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

interface User {
  sub: string | null
  preferred_username: string
  given_name: string
  family_name: string
  name: string
  email: string
  email_verified: boolean
  permissions: string[]
}
