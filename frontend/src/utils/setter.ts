// utils/setter.ts
import { ChangeEvent, Dispatch, SetStateAction } from 'react'

export const handleInputChange = (
  setter: Dispatch<SetStateAction<string>>,
  errorSetter: Dispatch<SetStateAction<string>>
) => (e: ChangeEvent<HTMLInputElement>) => {
  const value = e.target.value
  setter(value)
  if (value.trim()) errorSetter('')
}
