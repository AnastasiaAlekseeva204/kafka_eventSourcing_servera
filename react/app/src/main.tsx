import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

import { createTheme, ThemeProvider} from '@mui/material/styles'
import { CssBaseline } from '@mui/material'
import { RouterProvider } from 'react-router-dom'
import { router } from './routes.tsx'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const theme = createTheme({})
const queryClient = new QueryClient()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline/>
        <RouterProvider router={router}/>
      </ThemeProvider>
    </QueryClientProvider>
  </StrictMode>,
)