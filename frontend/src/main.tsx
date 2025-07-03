import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material'
import { AuthProvider } from './context/AuthContext'
import { CustomThemeProvider } from './theme/ThemeContext'
import './App.css'

const theme = createTheme()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <CustomThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </AuthProvider>
      </CustomThemeProvider>
    </ThemeProvider>
  </React.StrictMode>
)
