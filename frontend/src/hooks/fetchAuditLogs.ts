import { useEffect, useState } from 'react'
import { getLogs } from '../api/audit'
import { AuditEntry } from '../types/audit'
import { AuditLogParams } from '../types/logs'

export const useFetchAuditLogs = (
  page: number,
  rowsPerPage: number,
  search: string,
  resource: string,
  session?: string,
  ip?: string,
  startDate?: string,
  endDate?: string,
  action?: string
) => {
  const [logs, setLogs] = useState<AuditEntry[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)

  const fetch = async () => {
    setLoading(true)

    const filters: AuditLogParams = {
      page,
      limit: rowsPerPage,
      ...(search.trim() && { search: search.trim() }),
      ...(resource && { resource }),
      ...(session && { session_id: session }),
      ...(ip && { ip }),
      ...(startDate && { start_date: startDate }),
      ...(endDate && { end_date: endDate }),
      action,
    }

    try {
      const res = await getLogs(filters)
      setLogs(res.data.logs || [])
      setTotal(res.data.total || 0)
    } catch (error) {
      console.error('Failed to fetch audit logs:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetch()
  }, [page, rowsPerPage, search, resource, session, ip, startDate, endDate, action])

  return { logs, total, loading }
}
