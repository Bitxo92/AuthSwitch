import type { User } from "@/auth/types/user"

export const mockUserResponse: User = {
  username: "User",
  first_name: "Mock",
  last_name: "Admin",
  full_name: "Mock Admin",
  email: "user@mail.com",
  is_active: true,
  roles: ["Administrator"],
  permissions: [],
  password_expiration: "2026-06-21T10:30:24.750Z",
}
