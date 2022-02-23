import classnames from 'classnames'
import { FC, memo, useEffect, useState } from 'react'

const cn = classnames({
  'bg-slate-500': true,
})

const Home: FC = function Home() {
  const [classes, setClasses] = useState(cn)

  useEffect(() => {
    setTimeout(() => {
      setClasses(
        classnames({
          'border-4': true,
        }),
      )
    }, 5000)
  }, [])

  return (
    <div className={classes}>
      <h1 className="text-3xl font-bold underline">Hello, world!</h1>
    </div>
  )
}

export default memo(Home)
