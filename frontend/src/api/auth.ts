import api from '../utils/axios'

export const loginUser = async (email: string, password: string) => {
  const res = await api.post('/login', { email, password }, {
    withCredentials: true,
  })
  return res.data
}

export const registerUser = async (
  email: string,
  password: string,
  full_name: string
) => {
  const res = await api.post('/register', { email, password, full_name })
  return res.data
}

export const logoutUser = async () => {
  const res = await api.post('/logout', {})
  return res.data
}


