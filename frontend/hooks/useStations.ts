import { useState, useEffect } from 'react'
import Papa from 'papaparse'
import { Station, StationCSVRow } from '@/lib/types'

interface UseStationsReturn {
  stations: Station[]
  stationsMap: Record<string, Station>
  loading: boolean
  error: string | null
}

export function useStations(): UseStationsReturn {
  const [stations, setStations] = useState<Station[]>([])
  const [stationsMap, setStationsMap] = useState<Record<string, Station>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadStations = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch('/data/metrosp_stations.csv')

        if (!response.ok) {
          throw new Error('Failed to load stations data')
        }

        const csvText = await response.text()

        Papa.parse<StationCSVRow>(csvText, {
          header: true,
          dynamicTyping: true,
          complete: (results) => {
            const parsedStations = results.data
              .filter((row) => row.name && row.station)
              .map((row) => ({
                name: row.name,
                station: row.station,
                lat: row.lat,
                lon: row.lon,
                color: row.cor,
              }))

            setStations(parsedStations)

            const map: Record<string, Station> = {}
            parsedStations.forEach((station) => {
              map[station.station] = station
            })
            setStationsMap(map)
            setLoading(false)
          },
          error: (err: Error) => {
            setError(err.message)
            setLoading(false)
          },
        })
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error occurred')
        setLoading(false)
      }
    }

    loadStations()
  }, [])

  return { stations, stationsMap, loading, error }
}
