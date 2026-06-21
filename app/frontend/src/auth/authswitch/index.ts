import { AuthHttpClient } from "@/auth/authswitch/httpclient"
import { MockAuthClient } from "./mockclient"

// const authswitch_config = import.meta.env.VITE_USE_AUTH_MOCK
const authswitch_config = true

export const ApiClient = authswitch_config
  ? new MockAuthClient()
  : new AuthHttpClient()
