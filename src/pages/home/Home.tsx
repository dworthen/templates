import { FC, memo } from 'react'

const Home: FC = function Home() {
  return (
    <div>
      <h1 className="text-3xl font-bold underline">Hello, world!</h1>
    </div>
  )
}

export default memo(Home)
