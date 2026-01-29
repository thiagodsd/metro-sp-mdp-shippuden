'use client'

import { useState } from 'react'
import { useStations } from '@/hooks/useStations'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'

interface RouteSelectorProps {
  onPathFound: (path: string[]) => void
}

export default function RouteSelector({ onPathFound }: RouteSelectorProps) {
  const { stations, loading: stationsLoading } = useStations()
  const [fromStation, setFromStation] = useState<string>('')
  const [toStation, setToStation] = useState<string>('')
  const [finding, setFinding] = useState(false)

  const handleFindPath = async () => {
    if (!fromStation || !toStation) return

    setFinding(true)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/route`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          start: fromStation,
          end: toStation,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to find route')
      }

      const data = await response.json()
      onPathFound(data.path || [])
    } catch (error) {
      console.error('Error finding route:', error)
      onPathFound([])
    } finally {
      setFinding(false)
    }
  }

  const isDisabled = !fromStation || !toStation || finding || stationsLoading

  const handleClear = () => {
    setFromStation('')
    setToStation('')
    onPathFound([])
  }

  return (
    <div className="mt-8 py-10 px-5 flex gap-8 items-center justify-center">
      <div>
        <label className="text-xs font-medium mb-1 block text-gray-700">
          From
        </label>
        <Select
          value={fromStation}
          onValueChange={setFromStation}
          disabled={stationsLoading}
        >
          <SelectTrigger className="w-[240px]">
            <SelectValue placeholder="Select station" />
          </SelectTrigger>
          <SelectContent>
            {stations.map((station) => (
              <SelectItem key={station.station} value={station.station}>
                {station.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div>
        <label className="text-xs font-medium mb-1 block text-gray-700">
          To
        </label>
        <Select
          value={toStation}
          onValueChange={setToStation}
          disabled={stationsLoading}
        >
          <SelectTrigger className="w-[240px]">
            <SelectValue placeholder="Select station" />
          </SelectTrigger>
          <SelectContent>
            {stations.map((station) => (
              <SelectItem key={station.station} value={station.station}>
                {station.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <Button
        onClick={handleFindPath}
        disabled={isDisabled}
        size="default"
        className="mt-5"
      >
        {finding ? 'Finding...' : 'Find Path'}
      </Button>

      <Button
        onClick={handleClear}
        variant="outline"
        size="default"
        className="mt-5"
      >
        Clear
      </Button>
    </div>
  )
}
