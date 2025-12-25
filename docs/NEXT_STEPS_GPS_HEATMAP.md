# Next Steps: GPS Route Heatmap with Pace-Based Coloring

## What's Been Completed ✅

1. **Fixed React white screen issue** - Added missing `import React from 'react'` to all components
2. **Converted units to miles** - All API endpoints and frontend now display miles and feet instead of km and meters
3. **Committed changes to GitHub** - Latest commit includes the miles conversion

## What Still Needs to Be Done 🔄

### 1. Fetch GPS Polyline Data from Strava API

The current data doesn't include GPS coordinates for routes. You need to:

**Option A: Use Strava API to fetch detailed activity streams**
```python
# Add to api.py
@app.route('/api/routes')
def get_routes():
    """Fetch GPS polylines with pace data for each activity"""
    import requests
    access_token = os.getenv('STRAVA_ACCESS_TOKEN')

    routes = []
    for activity_id in activity_ids[:50]:  # Limit to 50 most recent
        # Fetch activity streams (latlng and time)
        stream_url = f'https://www.strava.com/api/v3/activities/{activity_id}/streams'
        params = {'keys': 'latlng,time,distance', 'key_by_type': True}
        response = requests.get(stream_url, headers={'Authorization': f'Bearer {access_token}'}, params=params)

        if response.status_code == 200:
            streams = response.json()
            latlng = streams.get('latlng', {}).get('data', [])
            time = streams.get('time', {}).get('data', [])
            distance = streams.get('distance', {}).get('data', [])

            # Calculate pace for each segment
            pace_data = []
            for i in range(1, len(time)):
                time_diff = time[i] - time[i-1]  # seconds
                dist_diff = (distance[i] - distance[i-1]) / 1000  # km
                if dist_diff > 0:
                    pace_min_per_km = (time_diff / 60) / dist_diff
                    pace_min_per_mi = pace_min_per_km / 0.621371
                    pace_data.append(pace_min_per_mi)
                else:
                    pace_data.append(None)

            routes.append({
                'activity_id': activity_id,
                'coordinates': latlng,
                'paces': pace_data
            })

    return jsonify({'routes': routes})
```

**Option B: Use existing data with start/end coordinates**
- The raw JSON has `start_latlng` and `end_latlng` for each activity
- Could draw straight lines between start/end points as a simple visualization
- Won't show actual routes but gives a sense of running locations

### 2. Update Heatmap Component to Draw Polylines

Replace the current point-based heatmap with polyline routes:

```javascript
// frontend/src/pages/Heatmap.jsx
import { Polyline, useMap } from 'react-leaflet'

// Helper function to get color based on pace
const getPaceColor = (paceMinPerMile) => {
  if (!paceMinPerMile) return '#808080' // gray for missing data

  // Color scale: 6min/mi = red (fast), 11min/mi = blue (slow)
  if (paceMinPerMile <= 6) return '#ff0000'      // Red - very fast
  if (paceMinPerMile <= 7) return '#ff6600'      // Orange-red
  if (paceMinPerMile <= 8) return '#ffaa00'      // Orange
  if (paceMinPerMile <= 9) return '#ffff00'      // Yellow
  if (paceMinPerMile <= 10) return '#00ff00'     // Green
  if (paceMinPerMile <= 11) return '#0000ff'     // Blue
  return '#000088'                                 // Dark blue - very slow
}

function Heatmap() {
  const [routes, setRoutes] = useState(null)

  useEffect(() => {
    axios.get(`${API_URL}/routes`)
      .then(res => setRoutes(res.data.routes))
      .catch(err => console.error(err))
  }, [])

  return (
    <MapContainer>
      <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" />

      {/* Pace Legend */}
      <div style={{
        position: 'absolute',
        top: '10px',
        right: '10px',
        background: 'rgba(0,0,0,0.8)',
        padding: '1rem',
        borderRadius: '8px',
        zIndex: 1000
      }}>
        <h4 style={{color: '#fff', marginBottom: '0.5rem'}}>Pace (min/mi)</h4>
        <div style={{display: 'flex', flexDirection: 'column', gap: '0.25rem'}}>
          <div><span style={{color: '#ff0000'}}>■</span> ≤6:00 (Very Fast)</div>
          <div><span style={{color: '#ff6600'}}>■</span> 6-7</div>
          <div><span style={{color: '#ffaa00'}}>■</span> 7-8</div>
          <div><span style={{color: '#ffff00'}}>■</span> 8-9</div>
          <div><span style={{color: '#00ff00'}}>■</span> 9-10</div>
          <div><span style={{color: '#0000ff'}}>■</span> 10-11</div>
          <div><span style={{color: '#000088'}}>■</span> ≥11 (Recovery)</div>
        </div>
      </div>

      {/* Draw polylines for each route */}
      {routes && routes.map((route, idx) => {
        // Group coordinates by pace to create colored segments
        const segments = []
        let currentSegment = []
        let currentPace = null

        route.coordinates.forEach((coord, i) => {
          const pace = route.paces[i]
          if (pace !== currentPace) {
            if (currentSegment.length > 1) {
              segments.push({
                coords: currentSegment,
                pace: currentPace
              })
            }
            currentSegment = [coord]
            currentPace = pace
          } else {
            currentSegment.push(coord)
          }
        })

        if (currentSegment.length > 1) {
          segments.push({
            coords: currentSegment,
            pace: currentPace
          })
        }

        // Render each segment with its pace color
        return segments.map((segment, segIdx) => (
          <Polyline
            key={`${idx}-${segIdx}`}
            positions={segment.coords}
            pathOptions={{
              color: getPaceColor(segment.pace),
              weight: 3,
              opacity: 0.7
            }}
          />
        ))
      })}
    </MapContainer>
  )
}
```

### 3. Alternative: Heatmap Overlay

If you want actual heat density instead of individual routes:

```javascript
import { HeatmapLayer } from 'react-leaflet-heatmap-layer-v3'

// Collect all GPS points with pace as intensity
const heatmapPoints = routes.flatMap(route =>
  route.coordinates.map((coord, i) => ({
    lat: coord[0],
    lng: coord[1],
    intensity: route.paces[i] ? (11 - route.paces[i]) / 5 : 0.5  // Invert so faster = hotter
  }))
)

<HeatmapLayer
  points={heatmapPoints}
  longitudeExtractor={p => p.lng}
  latitudeExtractor={p => p.lat}
  intensityExtractor={p => p.intensity}
  radius={15}
  blur={25}
  max={1}
  gradient={{
    0.0: 'blue',    // Slow pace
    0.5: 'yellow',
    1.0: 'red'      // Fast pace
  }}
/>
```

## Testing Your Strava API Access

First, verify you have an access token:

```bash
# Check if token exists
cd "/Users/louissader/Strava Project"
grep STRAVA .env

# Test API access
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://www.strava.com/api/v3/athlete/activities?per_page=1"
```

## Quick Implementation Path

**Easiest approach** (to get something working fast):
1. Use Option B above - draw straight lines between start/end points
2. Color based on overall activity pace
3. This shows running locations without detailed GPS data

**Best approach** (for full feature):
1. Implement the `/api/routes` endpoint to fetch detailed streams
2. Update Heatmap component to draw polylines
3. Add pace-based coloring and legend

## Current Status

Your app now has:
- ✅ Working React frontend with custom cyberpunk design
- ✅ All units in miles and feet
- ✅ Dashboard with impressive activities
- ✅ Race predictions
- ⚠️ Heatmap showing simulated data (needs GPS polylines)
- ⚠️ Analytics page (placeholder - needs charts)
- ⚠️ Timeline page (placeholder - needs implementation)

Choose which feature you want to tackle next!