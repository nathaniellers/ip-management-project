// hooks/fetchIps.ts
import { useEffect, useState } from 'react'
import { getIPs } from '../api/ip'
import { IPEntry } from '../types/ip'

export const useFetchIPs = (
  page: number,
  limit: number,
  search: string
) => {
  const [ipList, setIpList] = useState<IPEntry[]>([])
  const [total, setTotal] = useState(0)

  const fetch = async () => {
    try {
      const res = await getIPs({ page: page + 1, limit, search }) // ✅ pass search
      setIpList(res.data)
      setTotal(res.total)
      console.log('Fetching with search:', search)
    } catch (err) {
      console.error('Error fetching IPs:', err)
    }
  }

  useEffect(() => {
    fetch()
  }, [page, limit, search])

  return {
    ipList,
    total,
    refetch: fetch,
  }
}
