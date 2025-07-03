import {
  Container,
  Button,
  Typography,
  Box,
  Link,
} from '@mui/material'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginUser } from '../api/auth'
import { useAuth } from '../context/AuthContext'
import { decodeJwt } from 'jose'
import { showSuccess } from '../components/dialog/Success'
import { showError } from '../components/dialog/Error'
import { UserPayload } from '../types/user'
import ValidatedTextField from '../components/validatedTextField'
import { handleInputChange } from '../utils/setter'
import { validateEmail, validatePassword } from '../components/validation/registerValidation'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [emailError, setEmailError] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async () => {
    const emailErr = validateEmail(email)
    const passwordErr = validatePassword(password)

    setEmailError(emailErr)
    setPasswordError(passwordErr)

    if (emailErr || passwordErr) return

    try {
      const response = await loginUser(email, password)
      const { access_token } = response
      const decoded: any = decodeJwt(access_token)

      const { id, name: full_name, email: user_email, role } = decoded.user
      
      const user: UserPayload = { id, full_name, email: user_email, role }

      login(access_token, user)
      showSuccess('Login Successful', 'You may now proceed to dashboard.')
      navigate('/dashboard')
    } catch (err) {
      showError('Login Failed')
    }
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Typography variant="h4" gutterBottom>Login</Typography>
       <ValidatedTextField
          label="Email"
          value={email}
          onChange={handleInputChange(setEmail, setEmailError)}
          error={emailError}
        />
        <ValidatedTextField
          label="Password"
          value={password}
          onChange={handleInputChange(setPassword, setPasswordError)}
          error={passwordError}
          type="password"
        />
      <Box mt={2}>
        <Button variant="contained" fullWidth onClick={handleSubmit}>Login</Button>
      </Box>
      <Link href="/register" sx={{ fontWeight: 'bold', marginTop: '10px', textAlign: 'center', display: 'block' }}>
        Create Account
      </Link>
    </Container>
  )
}

export default Login
