'use client'

import { useMemo } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup, Polyline, useMap } from 'react-leaflet'
import { LatLngBounds } from 'leaflet'
import { useStations } from '@/hooks/useStations'
import { Station } from '@/lib/types'
import 'leaflet/dist/leaflet.css'

const COLOR_MAP: Record<string, string> = {
  blue: '#0455A1',
  green: '#007E5E',
  red: '#EE372F',
  yellow: '#FDD000',
  purple: '#9B3894',
  silver: '#C0C0C0',
  gray: '#808080',
}

interface MapProps {
  path?: string[]
}

function ResetViewControl({ stations }: { stations: Station[] }) {
  const map = useMap()

  const handleReset = () => {
    if (stations.length === 0) return

    const bounds = new LatLngBounds(
      stations.map(s => [s.lat, s.lon])
    )
    map.fitBounds(bounds, { padding: [50, 50] })
  }

  return (
    <div className="absolute top-2.5 right-2.5 z-[1000]">
      <button
        onClick={handleReset}
        className="bg-white border-2 border-black/20 rounded px-3 py-2 cursor-pointer text-sm font-medium shadow-md text-gray-800 hover:bg-gray-50 transition-colors"
      >
        Reset View
      </button>
    </div>
  )
}

function PathPolyline({ path, stationsMap }: { path: string[], stationsMap: Record<string, Station> }) {
  const pathCoords = useMemo(() => {
    return path
      .map(stationId => stationsMap[stationId])
      .filter(station => station)
      .map(station => [station.lat, station.lon] as [number, number])
  }, [path, stationsMap])

  if (pathCoords.length < 2) return null

  return (
    <Polyline
      positions={pathCoords}
      pathOptions={{
        color: '#FF6B00',
        weight: 4,
        opacity: 0.8,
      }}
    />
  )
}

export default function Map({ path = [] }: MapProps) {
  const { stations, stationsMap, loading, error } = useStations()

  if (loading) {
    return (
      <div className="h-[85vh] flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" />
          <p className="mt-2 text-gray-600">Loading stations...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="h-[85vh] flex items-center justify-center">
        <div className="text-center text-red-600">
          <p className="text-lg font-semibold">Failed to load stations</p>
          <p className="text-sm mt-1">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-[85vh] flex justify-center pt-2">
      <MapContainer
        center={[-23.550520, -46.633308]}
        zoom={12}
        style={{ height: '100%', width: '70%' }}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
        />
        {stations.map((station) => {
          const isInPath = path.includes(station.station)
          return (
            <CircleMarker
              key={station.station}
              center={[station.lat, station.lon]}
              radius={isInPath ? 10 : 6}
              fillColor={isInPath ? '#FF6B00' : (COLOR_MAP[station.color] || '#808080')}
              color="#fff"
              weight={isInPath ? 3 : 2}
              opacity={1}
              fillOpacity={isInPath ? 1 : 0.8}
            >
              <Popup>{station.name}</Popup>
            </CircleMarker>
          )
        })}
        {path.length > 0 && <PathPolyline path={path} stationsMap={stationsMap} />}
        <ResetViewControl stations={stations} />
      </MapContainer>
    </div>
  )
}
