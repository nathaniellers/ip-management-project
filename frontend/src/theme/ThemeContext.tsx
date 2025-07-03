import { createContext, useContext, useMemo, useState } from 'react'
import { createTheme, ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'

const ColorModeContext = createContext({ toggleColorMode: () => {} })

export const useColorMode = () => useContext(ColorModeContext)

export const CustomThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [mode, setMode] = useState<'light' | 'dark'>('light')

  const toggleColorMode = () => setMode(prev => (prev === 'light' ? 'dark' : 'light'))

  const theme = useMemo(() =>
    createTheme({
      palette: {
        mode,
      },
      typography: {
        fontFamily: `'Poppins', sans-serif`,
      },
    }), [mode])

  return (
    <ColorModeContext.Provider value={{ toggleColorMode }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ColorModeContext.Provider>
  )
}
