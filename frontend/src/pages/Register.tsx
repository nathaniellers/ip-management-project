import { useNavigate } from 'react-router-dom'
import { registerUser } from '../api/auth'
import { showSuccess } from '../components/dialog/Success'
import { showError } from '../components/dialog/Error'
import ValidatedTextField from '../components/validatedTextField'
import { validateRequired, validateEmail, validatePassword } from '../components/validation/registerValidation'
import { handleInputChange } from '../utils/setter'
import { Container, Typography, Button, Box } from '@mui/material'
import { useState } from 'react'

export default function RegisterForm() {
  const navigate = useNavigate()

  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [nameError, setNameError] = useState('')
  const [emailError, setEmailError] = useState('')
  const [passwordError, setPasswordError] = useState('')

  const handleRegister = async () => {
    const nameErr = validateRequired(fullName, 'Full Name')
    const emailErr = validateEmail(email)
    const passwordErr = validatePassword(password)

    setNameError(nameErr)
    setEmailError(emailErr)
    setPasswordError(passwordErr)

    if (nameErr || emailErr || passwordErr) return

    try {
      await registerUser(email, password, fullName)
      showSuccess('Registration Successful', 'You may now log in.')
      navigate('/login')
    } catch (err) {
      showError('Registration Failed')
    }
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Typography variant="h4" gutterBottom>Register</Typography>

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

      <Box mt={2}>
        <Button variant="contained" fullWidth onClick={handleRegister}>
          Register
        </Button>
      </Box>
    </Container>
  )
}
