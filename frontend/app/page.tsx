'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'
import RouteSelector from '@/components/RouteSelector'

const Map = dynamic(() => import('@/components/Map'), {
  ssr: false,
})

export default function Home() {
  const [path, setPath] = useState([])

  return (
    <div className="flex flex-col h-screen relative">
      <Map path={path} />
      <RouteSelector onPathFound={setPath} />
    </div>
  )
}
