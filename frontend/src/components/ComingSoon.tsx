import { useEffect, useState } from 'react'

export default function ComingSoon() {
  const [dots, setDots] = useState('...')

  useEffect(() => {
    setTimeout(() => {
      switch (dots) {
        case dots.length === 3 ? dots : false:
          setDots('')
          break
        case dots.length === 2 ? dots : false:
          setDots('...')
          break
        case dots.length === 1 ? dots : false:
          setDots('..')
          break
        case dots.length === 0 ? dots : false:
          setDots('.')
          break
      }
    }, 750)
  }, [dots])

  return (
    <div className="flex flex-col justify-center h-screen">
      <h1 className="text-4xl font-semibold ml-[40vw] relative">
        DocsGPT Coming Soon{dots} <span className="absolute left-112">🦖</span>
      </h1>
    </div>
  )
}
