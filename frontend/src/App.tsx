import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ProtectedRoute from './components/ProtectedRoute'
import Navbar from './components/Navbar/Navbar'
import { useAuth } from './context/AuthContext'
import AuditLog from './pages/AuditLog'

function App() {
  const { token } = useAuth()
  
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to={token ? "/dashboard" : "/login"} replace />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />  
        <Route
          path="/audit-logs"
          element={
            <ProtectedRoute>
              <AuditLog />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </>
  )
}

export default App
