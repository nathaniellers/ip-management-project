import {
  Table, TableHead, TableBody, TableRow, TableCell,
  TablePagination, TextField, IconButton, Box, TableSortLabel
} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import EditIcon from '@mui/icons-material/Edit'
import { useState } from 'react'

interface Column {
  id: string
  label: string
  render?: (row: any) => string
}

interface Props {
  columns: Column[]
  data: any[]
  total: number
  page: number
  rowsPerPage: number
  search: string
  onSearchChange: (value: string) => void
  onPageChange: (event: unknown, newPage: number) => void
  onRowsPerPageChange: (event: React.ChangeEvent<HTMLInputElement>) => void
  onEdit?: (id: string) => void
  onDelete?: (id: string) => void
  userId?: string
  userRole?: string
  placeholder?: string
}

export default function DataTable({
  columns,
  data,
  total,
  page,
  rowsPerPage,
  search,
  onSearchChange,
  onPageChange,
  onRowsPerPageChange,
  onEdit,
  onDelete,
  userId,
  userRole,
  placeholder
}: Props) {
  const [orderBy, setOrderBy] = useState<string>('')
  const [order, setOrder] = useState<'asc' | 'desc'>('asc')

  const handleSort = (columnId: string) => {
    const isAsc = orderBy === columnId && order === 'asc'
    setOrderBy(columnId)
    setOrder(isAsc ? 'desc' : 'asc')
  }

  const sortedData = [...data].sort((a, b) => {
    const aVal = a[orderBy]
    const bVal = b[orderBy]
    if (aVal == null || bVal == null) return 0
    if (aVal < bVal) return order === 'asc' ? -1 : 1
    if (aVal > bVal) return order === 'asc' ? 1 : -1
    return 0
  })

  return (
    <Box>
      <TextField
        label={placeholder}
        fullWidth
        margin="normal"
        value={search}
        onChange={e => onSearchChange(e.target.value)}
        sx={{ mb: 2, mt: 1 }}
      />

      <Box sx={{ overflowX: 'auto' }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              {columns.map(col => (
                <TableCell key={col.id} sortDirection={orderBy === col.id ? order : false}>
                  <TableSortLabel
                    active={orderBy === col.id}
                    direction={orderBy === col.id ? order : 'asc'}
                    onClick={() => handleSort(col.id)}
                  >
                    {col.label}
                  </TableSortLabel>
                </TableCell>
              ))}
              {(onEdit || onDelete) && <TableCell>Actions</TableCell>}
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedData.map((entry) => (
              <TableRow key={entry.id}>
                {columns.map(col => (
                  <TableCell key={col.id}>
                    {col.render ? col.render(entry) : entry[col.id]}
                  </TableCell>
                ))}
                {(onEdit || onDelete) && (
                  <TableCell>
                    {onEdit && (userRole === 'admin' || entry.created_by === userId) && (
                      <IconButton onClick={() => onEdit(entry.id)} size="small">
                        <EditIcon fontSize="small" />
                      </IconButton>
                    )}
                    {onDelete && userRole === 'admin' && (
                      <IconButton onClick={() => onDelete(entry.id)} color="error" size="small">
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    )}
                  </TableCell>
                )}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Box>

      <TablePagination
        component="div"
        count={total}
        page={page}
        onPageChange={onPageChange}
        rowsPerPage={rowsPerPage}
        onRowsPerPageChange={onRowsPerPageChange}
        sx={{
          mt: 2,
          '& .MuiTablePagination-selectLabel, & .MuiTablePagination-displayedRows': {
            fontSize: '0.875rem',
          }
        }}
      />
    </Box>
  )
}
