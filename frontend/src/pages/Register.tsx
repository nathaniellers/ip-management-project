import { useNavigate } from 'react-router-dom'
import { registerUser } from '../api/auth'
import { showSuccess } from '../components/dialog/Success'
import { showError } from '../components/dialog/Error'
import ValidatedTextField from '../components/validatedTextField'
import {
  validateRequired,
  validateEmail,
  validatePassword
} from '../components/validation/registerValidation'
import { handleInputChange } from '../utils/setter'
import { 
  Container,
  Typography,
  Button,
  Box 
} from '@mui/material'
import { useState } from 'react'
import { confirmAction } from '../components/dialog/Confirm'

export default function RegisterForm() {
  const navigate = useNavigate()

  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const [nameError, setNameError] = useState('')
  const [emailError, setEmailError] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [confirmPasswordError, setConfirmPasswordError] = useState('')

  const handleRegister = async () => {
    const nameErr = validateRequired(fullName, 'Full Name')
    const emailErr = validateEmail(email)
    const passwordErr = validatePassword(password)
    const confirmErr =
      confirmPassword !== password ? 'Passwords do not match' : ''

    setNameError(nameErr)
    setEmailError(emailErr)
    setPasswordError(passwordErr)
    setConfirmPasswordError(confirmErr)

    if (nameErr || emailErr || passwordErr || confirmErr) return

    const result = await confirmAction({
      title: 'Confirm Registration',
      text: 'Are you sure you want to create this account?',
      icon: 'question',
      confirmButtonText: 'Yes, register me!'
    })
    if (result.isConfirmed) {
      try {
        await registerUser(email, password, fullName)
        await showSuccess('Registration Successful', 'You may now log in.')
        navigate('/login')
      } catch (err) {
        await showError('Registration Failed')
      }
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleRegister()
    }
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Typography variant="h4" gutterBottom>
        Register
      </Typography>

      <Box onKeyDown={handleKeyDown}>
        <ValidatedTextField
          label="Full Name"
          value={fullName}
          onChange={handleInputChange(setFullName, setNameError)}
          error={nameError}
        />

        <ValidatedTextField
          label="Email"
          value={email}
          onChange={handleInputChange(setEmail, setEmailError)}
          error={emailError}
        />

        <ValidatedTextField
          label="Password"
          type="password"
          value={password}
          onChange={handleInputChange(setPassword, setPasswordError)}
          error={passwordError}
        />

        <ValidatedTextField
          label="Confirm Password"
          type="password"
          value={confirmPassword}
          onChange={handleInputChange(setConfirmPassword, setConfirmPasswordError)}
          error={confirmPasswordError}
        />
      </Box>

      <Box mt={2}>
        <Button variant="contained" fullWidth onClick={handleRegister}>
          Register
        </Button>
      </Box>
    </Container>
  )
}
