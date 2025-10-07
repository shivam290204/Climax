# Delhi-NCR AQI Mobile App

Minimal React Native (Expo) starter consuming the backend FastAPI forecast endpoint.

## Features (initial)
- Fetch current AQI + category
- Display next 6 hourly AQI predictions
- Refresh button

## Running
Install dependencies:
```bash
npm install
```
Start Expo:
```bash
npm start
```
Open in Expo Go on your device (ensure the backend API at http://localhost:8000 is reachable or replace API_BASE in `src/hooks/useAqi.js`).

## Next Steps
- Add geolocation and pass current coordinates
- Show source attribution pie chart
- Implement health recommendations screen
- Offline caching with AsyncStorage
- Push notifications when AQI crosses threshold
