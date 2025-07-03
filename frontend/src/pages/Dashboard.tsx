import { Container, Typography, Button } from '@mui/material'
import { useState } from 'react'
import IPTable from '../components/IPTable'
import IPDialog from '../components/IPDialog'
import { useAuth } from '../context/AuthContext'
import { addIP, updateIP, deleteIP } from '../api/ip'
import { IPEntry } from '../types/ip'
import { useFetchIPs } from '../hooks/fetchIps'
import { useDebounce } from 'use-debounce'

const Dashboard = () => {
  const { user } = useAuth()
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingEntry, setEditingEntry] = useState<IPEntry | null>(null)
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(10)
  const [search, setSearch] = useState('')
  const [debouncedSearch] = useDebounce(search, 500)

  const { ipList, total, refetch } = useFetchIPs(page, rowsPerPage, debouncedSearch)

  const handleAddClick = () => {
    setEditingEntry(null)
    setDialogOpen(true)
  }

  const handleEditClick = (id: string) => {
    const entry = ipList.find((ip) => ip.id === id)
    if (entry) {
      setEditingEntry(entry)
      setDialogOpen(true)
    }
  }

  const handleDelete = async (id: string) => {
    try {
      await deleteIP(id)
      refetch()
    } catch (err) {
      console.error('Failed to delete IP:', err)
    }
  }

  const handleSubmitDialog = async (data: { ip: string; label: string; comment?: string }) => {
    try {
      if (editingEntry) {
        await updateIP(editingEntry.id, { label: data.label, comment: data.comment })
      } else {
        await addIP(data)
      }
      refetch()
      setDialogOpen(false)
      setEditingEntry(null)
    } catch (err) {
      console.error('Failed to submit IP:', err)
    }
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 5 }}>
      <Typography variant="h5" fontWeight="semibold" gutterBottom>
        IP Address Dashboard
      </Typography>

      <Button variant="contained" onClick={handleAddClick} sx={{ mb: 2 }}>
        Add IP Address
      </Button>

      <IPDialog
        open={dialogOpen}
        onClose={() => {
          setDialogOpen(false)
          setEditingEntry(null)
        }}
        onSubmit={handleSubmitDialog}
        initialData={
          editingEntry
            ? {
                ip: editingEntry.ip,
                label: editingEntry.label,
                comment: editingEntry.comment,
              }
            : undefined
        }
        isEdit={!!editingEntry}
      />

      <IPTable
        data={ipList}
        total={total}
        page={page}
        rowsPerPage={rowsPerPage}
        search={search}
        onSearch={(value) => {
          setSearch(value)
          setPage(0)
          setRowsPerPage(10)
        }}
        onPageChange={(_, newPage) => setPage(newPage)}
        onRowsPerPageChange={(e) => {
          setRowsPerPage(parseInt(e.target.value, 10))
          setPage(0)
        }}
        onDelete={handleDelete}
        onEdit={handleEditClick}
        userId={user?.id || ''}
        userRole={user?.role || 'user'}
      />
    </Container>
  )
}

export default Dashboard
