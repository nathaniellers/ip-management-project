export interface AuditLogParams {
  page: number
  limit: number
  search?: string
  action?: string
  resource?: string
  session_id?: string
  ip?: string
  start_date?: string
  end_date?: string
}