import {
  Container,
  Typography,
  Box,
  Select,
  MenuItem,
  TextField,
} from '@mui/material'
import { useState } from 'react'
import DataTable from '../components/DataTable'
import { useFetchAuditLogs } from '../hooks/fetchAuditLogs'
import { AuditEntry } from '../types/audit'

const AuditLog = () => {
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(10)
  const [search, setSearch] = useState('')
  const [resource, setResource] = useState('')
  const [action, setAction] = useState('')
  const [session, setSession] = useState('')
  const [ip, setIp] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const { logs, total } = useFetchAuditLogs(
    page + 1,
    rowsPerPage,
    search,
    resource,
    session,
    ip,
    startDate,
    endDate,
    action // pass action to hook
  )

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
        const date = new Date(row.timestamp)
        const formatter = new Intl.DateTimeFormat('en-PH', {
          timeZone: 'Asia/Manila',
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          hour12: true,
        })
        return formatter.format(date)
      },
    },
    { id: 'name', label: 'User' },
    { id: 'ip', label: 'IP Address' },
    { id: 'session_id', label: 'Session ID' },
    { id: 'action', label: 'Action' },
    { id: 'resource', label: 'Resource' },
    { id: 'details', label: 'Details' },
  ]

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        Audit Logs
      </Typography>

      {/* Filter Controls */}
      <Box display="flex" gap={2} my={2} flexWrap="wrap">
        <Select
          value={resource}
          onChange={(e) => {
            setResource(e.target.value)
            setPage(0)
          }}
          displayEmpty
          size="small"
        >
          <MenuItem value="">All Resources</MenuItem>
          <MenuItem value="auth">Auth</MenuItem>
          <MenuItem value="ip">IP Address</MenuItem>
          <MenuItem value="user">User</MenuItem>
        </Select>

        <Select
          value={action}
          onChange={(e) => {
            setAction(e.target.value)
            setPage(0)
          }}
          displayEmpty
          size="small"
        >
          <MenuItem value="">All Actions</MenuItem>
          <MenuItem value="login">Login</MenuItem>
          <MenuItem value="logout">Logout</MenuItem>
          <MenuItem value="create">Create</MenuItem>
          <MenuItem value="update">Update</MenuItem>
          <MenuItem value="delete">Delete</MenuItem>
        </Select>

        <TextField
          label="Start Date"
          type="date"
          size="small"
          InputLabelProps={{ shrink: true }}
          value={startDate}
          onChange={(e) => {
            setStartDate(e.target.value)
            setPage(0)
          }}
        />
        <TextField
          label="End Date"
          type="date"
          size="small"
          InputLabelProps={{ shrink: true }}
          value={endDate}
          onChange={(e) => {
            setEndDate(e.target.value)
            setPage(0)
          }}
        />
      </Box>

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
        placeholder='Search for Session ID, IP Address, User...'
      />
    </Container>
  )
}

export default AuditLog
