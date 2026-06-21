import { LoginForm } from "@/components/blocks/login_form"

export function LoginPage() {
  return (
    <div className="fixed inset-0 flex items-center justify-center">
      <LoginForm className="w-full max-w-md" />
    </div>
  )
}
