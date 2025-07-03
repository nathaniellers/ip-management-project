export interface UserPayload {
  id: string
  email: string
  full_name: string
  role: 'admin' | 'user'
}