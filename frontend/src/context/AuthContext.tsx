import { createContext, useContext, useState } from 'react'
import { UserPayload } from '../types/user'

interface AuthContextProps {
  token: string | null
  user: UserPayload | null
  login: (token: string, user: UserPayload) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextProps | null>(null)

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [user, setUser] = useState<UserPayload | null>(
    localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null
  )

  const login = (token: string, user: UserPayload) => {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
    setToken(token)
    setUser(user)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
