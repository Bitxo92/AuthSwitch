import { Navigate, Outlet } from "react-router-dom"
import { useAuth } from "@/auth/context/auth_context"

export function ProtectedRoute() {
  const { user, loading } = useAuth()

  if (loading) {
    return <FullPageLoader />
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  // logged in → render child routes
  return <Outlet />
}

function FullPageLoader() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-white/30 border-t-white" />
    </div>
  )
}
