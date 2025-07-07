import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button
} from '@mui/material'
import { useEffect, useState } from 'react'
import { validateIPForm } from './validation/ipValidation'
import { confirmAction } from './dialog/Confirm'
import { showSuccess } from './dialog/Success'

interface Props {
  open: boolean
  onClose: () => void
  onSubmit: (data: { ip: string; label: string; comment?: string }) => void
  initialData?: { ip: string; label: string; comment?: string }
  isEdit?: boolean
}

export default function IPDialog({
  open,
  onClose,
  onSubmit,
  initialData,
  isEdit = false
}: Props) {
  const [ipAddress, setIpAddress] = useState('')
  const [label, setLabel] = useState('')
  const [comment, setComment] = useState('')
  const [errors, setErrors] = useState<{ ip?: string; label?: string }>({})

  useEffect(() => {
    setIpAddress(initialData?.ip || '')
    setLabel(initialData?.label || '')
    setComment(initialData?.comment || '')
    setErrors({})
  }, [initialData, open])

  const handleSubmit = async () => {
    const formErrors = validateIPForm({
      ip: ipAddress,
      label,
      isEdit
    })

    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors)
      return
    }

    const payload = {
      ip: ipAddress.trim(),
      label: label.trim(),
      comment: comment.trim()
    }

    if (isEdit) {
      const result = await confirmAction({
        title: 'Confirm Update',
        text: 'Are you sure you want to update this IP address?',
        icon: 'warning',
        confirmButtonText: 'Yes, update it!',
      })

      if (result.isConfirmed) {
        onSubmit(payload)
        onClose()
        showSuccess()
      }

    } else {
      onSubmit(payload)
      onClose()
    }
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth disableEnforceFocus>
      <DialogTitle>{isEdit ? 'Edit IP' : 'Add New IP'}</DialogTitle>
      <DialogContent>
        <TextField
          fullWidth
          label="IP Address"
          margin="dense"
          value={ipAddress}
          onChange={(e) => setIpAddress(e.target.value)}
          error={!!errors.ip}
          helperText={errors.ip}
          disabled={isEdit}
        />
        <TextField
          fullWidth
          label="Label"
          margin="dense"
          value={label}
          onChange={(e) => setLabel(e.target.value)}
          error={!!errors.label}
          helperText={errors.label}
        />
        <TextField
          fullWidth
          label="Comment (optional)"
          margin="dense"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained">
          {isEdit ? 'Update' : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}
