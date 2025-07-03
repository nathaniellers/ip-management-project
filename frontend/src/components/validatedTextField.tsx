// components/ValidatedTextField.tsx
import { TextField } from '@mui/material'
import { ChangeEvent } from 'react'

interface Props {
  label: string
  value: string
  onChange: (event: ChangeEvent<HTMLInputElement>) => void
  error?: string
  type?: string
  disabled?: boolean
  multiline?: boolean
  required?: boolean
}

export default function ValidatedTextField({
  label,
  value,
  onChange,
  error = '',
  type = 'text',
  disabled = false,
  multiline = false,
  required = false,
}: Props) {
  return (
    <TextField
      fullWidth
      margin="normal"
      label={label}
      type={type}
      value={value}
      onChange={onChange}
      error={!!error}
      helperText={error}
      disabled={disabled}
      multiline={multiline}
      required={required}
    />
  )
}
