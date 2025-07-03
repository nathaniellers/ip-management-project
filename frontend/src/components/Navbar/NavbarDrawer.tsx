// src/components/Navbar/NavbarDrawer.tsx
import {
  List,
  ListItem,
  ListItemText,
  Divider,
  Box
} from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { logoutUser } from '../../api/auth'

interface Props {
  token: string | null
  user: { role: string } | null
  toggleColorMode: () => void
  onLogout: () => void
  onNavigate: (path: string) => void
}

const NavbarDrawer = ({
  token,
  user,
  toggleColorMode,
  onLogout,
  onNavigate
}: Props) => {
  const theme = useTheme()

  const handleLogout = async () => {
    await logoutUser()
    onLogout()
  }

  return (
    <Box sx={{ width: 250 }} role="presentation">
      <List>
        <ListItem color="inherit" component="a" onClick={() => onNavigate('/')}>
          <ListItemText primary="Home" />
        </ListItem>

        {token ? (
          <ListItem color="inherit" component="a" onClick={handleLogout}>
            <ListItemText primary="Logout" />
          </ListItem>
        ) : (
          <ListItem color="inherit" component="a" onClick={() => onNavigate('/login')}>
            <ListItemText primary="Login" />
          </ListItem>
        )}

        {user?.role === 'admin' && (
          <ListItem color="inherit" component="a" onClick={() => onNavigate('/audit-logs')}>
            <ListItemText primary="Audit Logs" />
          </ListItem>
        )}

        <Divider />

        <ListItem color="inherit" component="a" onClick={toggleColorMode}>
          <ListItemText
            primary={theme.palette.mode === 'dark' ? 'Light Mode' : 'Dark Mode'}
          />
        </ListItem>
      </List>
    </Box>
  )
}

export default NavbarDrawer
