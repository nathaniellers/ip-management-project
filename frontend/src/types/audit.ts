export interface AuditEntry {
  id: string
  timestamp: string
  session_id: string
  actor_id: string
  name: string
  ip: string
  action?: string
  resource?: string
  details: string
}
