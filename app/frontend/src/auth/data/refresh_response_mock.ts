import type { RefreshResponse } from "../types/refresh"

export const mockRefreshResponse: RefreshResponse = {
  access_token:
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impkb2UiLCJyZWFsbV9uYW1lIjoibWFpbiIsInR5cCI6ImFjY2VzcyIsImV4cCI6MTc4MjAzODMzMywic2Vzc2lvbl9pZCI6IjY1NjNlY2JjLTM0ZGItNDQyMi1iOWJjLTI4YWQ4N2I1ZDU2YyIsInBlcm1pc3Npb25zIjpbXSwicmxzIjp7fX0.lNn5R4cOrN9EYUqGWCjDIeuZ_d-6LVqNjylZtITWLmU",
  refresh_token:
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impkb2UiLCJyZWFsbV9uYW1lIjoibWFpbiIsInR5cCI6InJlZnJlc2giLCJleHAiOjE3ODIwMzkyMzMsInNlc3Npb25faWQiOiI2NTYzZWNiYy0zNGRiLTQ0MjItYjliYy0yOGFkODdiNWQ1NmMifQ.eCMQkvMRtvV6WBE7khTzT8w1sYrE1_oHWWlqAPfYtpI",
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
