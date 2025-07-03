// components/IPTable.tsx
import DataTable from './DataTable'
import { IPEntry } from '../types/ip'

interface Props {
  data: IPEntry[]
  total: number
  page: number
  rowsPerPage: number
  onDelete: (id: string) => void
  onEdit: (id: string) => void
  userId: string
  userRole: string
  search: string
  onSearch: (value: string) => void
  onPageChange: (event: unknown, newPage: number) => void
  onRowsPerPageChange: (event: React.ChangeEvent<HTMLInputElement>) => void
}

export default function IPTable({
  data,
  total,
  page,
  rowsPerPage,
  onDelete,
  onEdit,
  userId,
  userRole,
  search,
  onSearch,
  onPageChange,
  onRowsPerPageChange,
}: Props) {
  const columns = [
    { id: 'ip', label: 'IP Address' },
    { id: 'label', label: 'Label' },
    { id: 'comment', label: 'Comment' },
  ]

  return (
    <DataTable
      columns={columns}
      data={data}
      total={total}
      page={page}
      rowsPerPage={rowsPerPage}
      search={search}
      onSearchChange={onSearch}
      onPageChange={onPageChange}
      onRowsPerPageChange={onRowsPerPageChange}
      onEdit={onEdit}
      onDelete={onDelete}
      userId={userId}
      userRole={userRole}
    />
  )
}
