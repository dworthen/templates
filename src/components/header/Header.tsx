import { FC, memo } from 'react'
import { Link } from 'react-router-dom'

import { Flex } from '../flexbox/index.js'

export const Header: FC = memo(function Header() {
  return (
    <div>
      <Flex align="center">
        <Link to="/">Home</Link>
      </Flex>
    </div>
  )
})
