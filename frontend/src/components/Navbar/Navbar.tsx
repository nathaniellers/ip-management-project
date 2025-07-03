// src/components/Navbar/Navbar.tsx
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Link as MuiLink,
  useMediaQuery,
  Drawer
} from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'
import { useTheme } from '@mui/material/styles'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { useColorMode } from '../../theme/ThemeContext'
import NavbarButtons from './NavbarButtons'
import NavbarDrawer from './NavbarDrawer'

const Navbar = () => {
  const { token, user, logout } = useAuth()
  const { toggleColorMode } = useColorMode()
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))
  const navigate = useNavigate()

  const [drawerOpen, setDrawerOpen] = useState(false)
  const toggleDrawer = (open: boolean) => () => setDrawerOpen(open)

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <MuiLink
            underline="none"
            sx={{ flexGrow: 1, color: '#fff', cursor: 'pointer' }}
            onClick={() => navigate('/')}
          >
            <Typography variant="h6" component="span">
              IP Management
            </Typography>
          </MuiLink>

          {isMobile ? (
            <IconButton
              color="inherit"
              edge="end"
              onClick={toggleDrawer(true)}
            >
              <MenuIcon />
            </IconButton>
          ) : (
            <NavbarButtons
              token={token}
              user={user}
              toggleColorMode={toggleColorMode}
              onLogout={logout}
            />
          )}
        </Toolbar>
      </AppBar>

      <Drawer anchor="right" open={drawerOpen} onClose={toggleDrawer(false)}>
        <NavbarDrawer
          token={token}
          user={user}
          toggleColorMode={toggleColorMode}
          onLogout={logout}
          onNavigate={navigate}
        />
      </Drawer>
    </>
  )
}

export default Navbar
