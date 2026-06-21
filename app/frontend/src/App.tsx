import { BrowserRouter, Route, Routes } from "react-router-dom"
import { AuthProvider } from "./auth/context/auth_context"
import { ProtectedRoute } from "./auth/components/protected_route"
import { LoginPage } from "./pages/login/page"
import { HomePage } from "./pages/home/page"

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<HomePage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
