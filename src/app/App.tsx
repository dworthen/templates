import { FC, memo, StrictMode } from 'react'
import { BrowserRouter } from 'react-router-dom'

import Routes from './Routes'

export const App: FC = memo(function App() {
  return (
    <StrictMode>
      <BrowserRouter>
        <Routes />
      </BrowserRouter>
    </StrictMode>
  )
})
