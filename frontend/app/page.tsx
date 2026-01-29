'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'
import RouteSelector from '@/components/RouteSelector'

const Map = dynamic(() => import('@/components/Map'), {
  ssr: false,
})

export default function Home() {
  const [path, setPath] = useState<string[]>([])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', position: 'relative' }}>
      <Map path={path} />
      <RouteSelector onPathFound={setPath} />
    </div>
  )
}
