import { useEffect, useMemo, useState } from 'react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

function App() {
  const [devices, setDevices] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [lastUpdated, setLastUpdated] = useState('')

  const fetchDevices = async () => {
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE_URL}/devices`)

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data = await response.json()
      setDevices(Array.isArray(data) ? data : [])
      setLastUpdated(new Date().toLocaleTimeString())
    } catch (fetchError) {
      setError(fetchError instanceof Error ? fetchError.message : 'Failed to load devices')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDevices()
  }, [])

  const offlineDevices = useMemo(
    () => devices.filter((device) => device.status === 'offline'),
    [devices],
  )

  return (
    <main className="dashboard">
      <header className="dashboard-header">
        <h1>Building Simulation Dashboard</h1>
        <button type="button" onClick={fetchDevices} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </header>

      {lastUpdated && <p className="meta">Last updated: {lastUpdated}</p>}

      {error && <p className="error">Error: {error}</p>}

      {offlineDevices.length > 0 && (
        <div className="alert" role="alert">
          Offline devices: {offlineDevices.map((device) => device.id).join(', ')}
        </div>
      )}

      <table>
        <thead>
          <tr>
            <th>Device ID</th>
            <th>Type</th>
            <th>Status</th>
            <th>Latest temperature</th>
            <th>Latest humidity</th>
          </tr>
        </thead>
        <tbody>
          {devices.length === 0 ? (
            <tr>
              <td colSpan="5">No devices available.</td>
            </tr>
          ) : (
            devices.map((device) => (
              <tr key={device.id}>
                <td>{device.id}</td>
                <td>{device.type}</td>
                <td>
                  <span className={`status status-${device.status}`}>{device.status}</span>
                </td>
                <td>{Number(device.temperature).toFixed(1)} °C</td>
                <td>{Number(device.humidity).toFixed(1)} %</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </main>
  )
}

export default App
