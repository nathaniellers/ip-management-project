import api from '../utils/axios'

export const getLogs = (params: { page: number, limit: number, search?: string }) => {
  return api.get('/logs/', { params })
}

