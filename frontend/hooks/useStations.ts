import { useState, useEffect } from 'react'
import Papa from 'papaparse'
import { Station, StationCSVRow } from '@/lib/types'

export function useStations() {
  const [stations, setStations] = useState<Station[]>([])
  const [stationsMap, setStationsMap] = useState<Record<string, Station>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadStations = async () => {
      const response = await fetch('/data/metrosp_stations.csv')

      if (!response.ok) {
        setError('Could not load station data')
        setLoading(false)
        return
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
              neigh: row.neigh || '',
            }))

          setStations(parsedStations)
          setStationsMap(
            Object.fromEntries(parsedStations.map(s => [s.station, s]))
          )
          setLoading(false)
        },
        error: () => {
          setError('Invalid CSV format')
          setLoading(false)
        },
      })
    }

    loadStations()
  }, [])

  return { stations, stationsMap, loading, error }
}
