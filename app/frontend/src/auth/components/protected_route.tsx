import { Navigate, Outlet, useLocation } from "react-router-dom"
import { useAuth } from "@/auth/context/auth_context"
import { Page404 } from "@/components/placeholder/404_page"

type ProtectedRouteProps = {
  requiredPermission?: string
}

function FullPageLoader() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-white/30 border-t-white" />
    </div>
  )
}

export function ProtectedRoute({ requiredPermission }: ProtectedRouteProps) {
  const { user, loading, hasRequiredPermission } = useAuth()
  const location = useLocation()

  if (loading) {
    return <FullPageLoader />
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location }} />
  } else if (requiredPermission && !hasRequiredPermission(requiredPermission)) {
    return <Page404 />
  }

  return <Outlet />
}
