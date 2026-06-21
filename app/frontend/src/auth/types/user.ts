// this interface is used when calling the /auth/me endpoint to get the logged user information

export interface User {
  username: string
  first_name: string
  last_name: string
  full_name: string
  email: string
  is_active: boolean
  roles: string[]
  permissions: string[]
  password_expiration: string
}
