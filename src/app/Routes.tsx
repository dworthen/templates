import { FC, lazy, memo, Suspense } from 'react'
import { Route, Routes as R } from 'react-router-dom'

import Layout from './Layout'

const Home = lazy(async () => await import('../pages/home/Home'))

const Routes: FC = function Routes() {
  return (
    <R>
      <Route path="/" element={<Layout />}>
        <Route
          path=""
          element={
            <Suspense fallback={<>Loading...</>}>
              <Home />
            </Suspense>
          }
        />
      </Route>
    </R>
  )
}

export default memo(Routes)
