import { useEffect, useState } from 'react'
import { getLogs } from '../api/audit'
import { AuditEntry } from '../types/audit'

export function useFetchAuditLogs(page: number, limit: number, search: string) {
  const [logs, setLogs] = useState<AuditEntry[]>([])
  const [total, setTotal] = useState(0)

  const fetch = async () => {
    try {
      const res = await getLogs({ page: page + 1, limit, search })
      setLogs(res.data.data)
      setTotal(res.data.total)
    } catch (err) {
      console.error('Failed to fetch audit logs:', err)
    }
  }

  useEffect(() => {
    fetch()
  }, [page, limit, search])

  return { logs, total, refetch: fetch }
}
