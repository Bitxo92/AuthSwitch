import { useAuth } from "@/auth/context/auth_context"
import { Button } from "@/components/ui/button"
import { Loader } from "lucide-react"
export function HomePage() {
  const { user, loading, logout } = useAuth()
  return (
    <div className="fixed inset-0 flex flex-col items-center justify-center">
      {loading ? (
        <Loader className="size-20 animate-spin" />
      ) : (
        <div className="overflow-auto-y flex min-h-0 flex-1 flex-col items-center justify-center gap-2 p-4">
          <div className="flex flex-col items-start gap-2 rounded-lg border-2 border-gray-300 p-8 shadow-md">
            {" "}
            <h1 className="text-2xl font-bold">Welcome, {user?.username}!</h1>
            <span className="text-sm text-gray-500">
              Full Name: {user?.full_name}
            </span>
            <span className="text-sm text-gray-500">Email: {user?.email}</span>
            <span className="text-sm text-gray-500">
              Role:{" "}
              {user?.roles.length === 0 ? "N/A" : user?.roles.join(", ")}{" "}
            </span>
            <span className="text-sm text-gray-500">
              Status: {user?.is_active ? "Active" : "Inactive"}
            </span>
            <div className="mt-2 flex w-full justify-center gap-2">
              <Button
                className="hover:cursor-pointer hover:bg-red-600 hover:text-white"
                onClick={logout}
              >
                Logout
              </Button>
              <Button
                className="hover:cursor-pointer hover:bg-red-600 hover:text-white"
                onClick={() => {
                  window.location.href = "/gestion-usuarios"
                }}
              >
                Gestion Usuarios Page
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
