export const validateRequired = (value: string, fieldName: string): string => {
  if (!value.trim()) return `${fieldName} is required`
  return ''
}

export const validateEmail = (email: string): string => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!email.trim()) return 'Email is required'
  if (!regex.test(email)) return 'Invalid email format'
  return ''
}

export const validatePassword = (password: string): string => {
  if (!password.trim()) return 'Password is required'
  if (password.length < 6) return 'Password must be at least 6 characters'
  return ''
}
