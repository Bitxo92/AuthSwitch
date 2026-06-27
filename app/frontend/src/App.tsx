import { BrowserRouter, Routes } from "react-router-dom"
import { AuthProvider } from "./auth/context/auth_context"
import { renderRoutes } from "./routes/routes"

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>{renderRoutes()}</Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
