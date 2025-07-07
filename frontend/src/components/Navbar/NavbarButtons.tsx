// src/components/Navbar/NavbarButtons.tsx
import { Button, IconButton } from '@mui/material'
import { Brightness4, Brightness7, ReceiptLong } from '@mui/icons-material'
import { useTheme } from '@mui/material/styles'
import { useNavigate } from 'react-router-dom'
import { logoutUser } from '../../api/auth'
import LogoutIcon from '@mui/icons-material/Logout';
import LoginIcon from '@mui/icons-material/Login';

interface Props {
  token: string | null
  user: { role: string } | null
  toggleColorMode: () => void
  onLogout: () => void
}

const NavbarButtons = ({ token, user, toggleColorMode, onLogout }: Props) => {
  const theme = useTheme()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logoutUser()
    onLogout()
  }

  return (
    <>
      {user?.role === 'admin' && (
        <IconButton onClick={() => navigate('/audit-logs')} color="inherit">
          <ReceiptLong />
        </IconButton>
      )}

      <IconButton onClick={toggleColorMode} color="inherit">
        {theme.palette.mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
      </IconButton>

      {token ? (
        <IconButton color="inherit" onClick={handleLogout}>
          <LogoutIcon/>
        </IconButton>
      ) : (
        <Button color="inherit" onClick={() => navigate('/login')}>
          <LoginIcon/>
        </Button>
      )}
    </>
  )
}

export default NavbarButtons
