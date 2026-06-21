import type { LoginResponse } from "../types/login"

export const mockLoginResponse: LoginResponse = {
  access_token:
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impkb2UiLCJyZWFsbV9uYW1lIjoibWFpbiIsInR5cCI6ImFjY2VzcyIsImV4cCI6MTc4MjAzODE4OSwic2Vzc2lvbl9pZCI6IjY1NjNlY2JjLTM0ZGItNDQyMi1iOWJjLTI4YWQ4N2I1ZDU2YyIsInBlcm1pc3Npb25zIjpbXSwicmxzIjp7fX0.jAEoypBMzptqPh6gV73QIdDD96mO0TwWJN3y9SII9lc",
  refresh_token:
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impkb2UiLCJyZWFsbV9uYW1lIjoibWFpbiIsInR5cCI6InJlZnJlc2giLCJleHAiOjE3ODIwMzkwODksInNlc3Npb25faWQiOiI2NTYzZWNiYy0zNGRiLTQ0MjItYjliYy0yOGFkODdiNWQ1NmMifQ.waqcHBqNeTLfXifjYE2qk3RsMzpyep3Y3laO9b97eN0",
  token_type: "bearer",
  user: {
    sub: null,
    preferred_username: "User",
    given_name: "Mock",
    family_name: "Admin",
    name: "Mock Admin",
    email: "user@mail.com",
    email_verified: true,
    permissions: [],
  },
}
