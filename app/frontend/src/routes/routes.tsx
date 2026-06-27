import { LoginPage } from "@/pages/login/page"
import type { ReactElement } from "react"
import { ProtectedRoute } from "@/auth/components/protected_route"
import { Route } from "react-router-dom"
import UnderConstruction from "@/components/placeholder/under_construction"
import { HomePage } from "@/pages/home/page"
import { Page404 } from "@/components/placeholder/404_page"

interface RouteConfig {
  path: string
  element: ReactElement
  enabled: boolean
  protected?: boolean
  permission?: string
}

const routes: RouteConfig[] = [
  {
    path: "/login",
    element: <LoginPage />,
    protected: false,
    enabled: true,
  },
  {
    path: "/",
    element: <HomePage />,
    protected: true,
    enabled: true,
  },
  {
    path: "*",
    element: <Page404 />,
    protected: false,
    enabled: true,
  },
]

export function renderRoutes() {
  return routes.map((route) => {
    const element = route.enabled ? route.element : <UnderConstruction />

    // PUBLIC ROUTE
    if (!route.protected) {
      return <Route key={route.path} path={route.path} element={element} />
    }

    // PROTECTED ROUTE
    return (
      <Route
        key={route.path}
        element={<ProtectedRoute requiredPermission={route.permission} />}
      >
        <Route path={route.path} element={element} />
      </Route>
    )
  })
}
