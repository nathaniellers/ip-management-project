export interface AuditEntry {
  id: string
  ip: string
  actor_id: string
  ip_id: string | null
  action: 'login' | 'logout' | 'create' | 'update' | 'delete'
  timestamp: string
  details?: string
}