import { Container, Typography } from '@mui/material'
import { useState } from 'react'
import DataTable from '../components/DataTable'
import { useFetchAuditLogs } from '../hooks/fetchAuditLogs'
import { AuditEntry } from '../types/audit'

const AuditLog = () => {
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(10)
  const [search, setSearch] = useState('')

  const { logs, total } = useFetchAuditLogs(page, rowsPerPage, search)

  const handlePageChange = (_: unknown, newPage: number) => setPage(newPage)
  const handleRowsPerPageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(e.target.value, 10))
    setPage(0)
  }

  const columns = [
    {
      id: 'timestamp',
      label: 'Timestamp',
      render: (row: AuditEntry) => {
        const date = new Date(row.timestamp); // Assumes this is UTC
        const formatter = new Intl.DateTimeFormat('en-PH', {
          timeZone: 'Asia/Manila',
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          hour12: true,
        });
        return formatter.format(date);
      },
    },
    { id: 'name', label: 'User' },
    {
      id: 'ip',
      label: 'IP Address',
    },
    { id: 'action', label: 'Action' },
    { id: 'details', label: 'Details' },
  ];

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom>Audit Logs</Typography>
      <DataTable
        columns={columns}
        data={logs}
        total={total}
        page={page}
        rowsPerPage={rowsPerPage}
        onPageChange={handlePageChange}
        onRowsPerPageChange={handleRowsPerPageChange}
        search={search}
        onSearchChange={setSearch}
      />
    </Container>
  )
}

export default AuditLog
