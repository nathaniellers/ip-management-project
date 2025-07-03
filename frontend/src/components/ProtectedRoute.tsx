import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { ReactNode } from 'react'

interface Props {
  children: ReactNode
  allowedRoles?: string[]
}

const ProtectedRoute = ({ children, allowedRoles }: Props) => {
  const { token, user } = useAuth()

  if (!token) return <Navigate to="/login" replace />
  if (allowedRoles && (!user || !allowedRoles.includes(user.role))) {
    return <Navigate to="/unauthorized" replace />
  }

  return children
}

export default ProtectedRoute
