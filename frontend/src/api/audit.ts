import { AuditLogParams } from '../types/logs'
import api from '../utils/axios'

export const getLogs = (params: AuditLogParams) => {
  return api.get('/logs/', { params })
}

