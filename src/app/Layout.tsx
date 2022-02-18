import { FC, memo } from 'react'
import { Outlet } from 'react-router-dom'

import { Flex } from '../components/flexbox'
import { Header } from '../components/header'

const Layout: FC = function Layout() {
  return (
    <Flex style={{ height: '100%' }} vertical>
      <Flex.Box>
        <Header />
      </Flex.Box>
      <Flex.Box grow={1}>
        <div>
          <Outlet />
        </div>
      </Flex.Box>
    </Flex>
  )
}

export default memo(Layout)
