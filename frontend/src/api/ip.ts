import api from '../utils/axios'

export const getIPs = async (params: { page: number; limit: number; search?: string }) => {
  const res = await api.get('/ip/', { params })
  return res.data
}

export const addIP = async (data: any) => {
  const res = await api.post('/ip/', data)
  return res.data
}

export const updateIP = async (id: string, data: any) => {
  const res = await api.put(`/ip/${id}`, data)
  return res.data
}

export const deleteIP = async (id: string) => {
  const res = await api.delete(`/ip/${id}`)
  return res.data
}
