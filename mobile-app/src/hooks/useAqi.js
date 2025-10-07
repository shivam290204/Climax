// [file name]: useAqi.js - ENHANCED
import { useEffect, useState } from 'react';
import * as Location from 'expo-location';
import { API_BASE, buildUrl } from '../config';
import { createApiClient, categoryForAqi } from '../../../shared/src';

export function useAqi() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [location, setLocation] = useState(null);

  async function getCurrentLocation() {
    try {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setError('Location permission denied');
        return { latitude: 28.6139, longitude: 77.2090 }; // Default to Delhi
      }

      let location = await Location.getCurrentPositionAsync({});
      return {
        latitude: location.coords.latitude,
        longitude: location.coords.longitude
      };
    } catch (error) {
      console.error('Error getting location:', error);
      return { latitude: 28.6139, longitude: 77.2090 }; // Fallback to Delhi
    }
  }

  const api = createApiClient(API_BASE);

  async function fetchData() {
    setLoading(true);
    try {
      const currentLocation = await getCurrentLocation();
      setLocation(currentLocation);

      const [currentRes, hourlyRes, sourcesRes] = await Promise.all([
        api.get('/forecast/current', {
          params: {
            latitude: currentLocation.latitude,
            longitude: currentLocation.longitude,
            hours: 24
          }
        }),
        api.get('/forecast/hourly', {
          params: {
            latitude: currentLocation.latitude,
            longitude: currentLocation.longitude,
            hours: 24
          }
        }),
        api.get('/sources/current', {
          params: {
            latitude: currentLocation.latitude,
            longitude: currentLocation.longitude
          }
        })
      ]);

      // TODO: Add health recommendations endpoint integration when available
      // const healthRes = await axios.get(buildUrl('/health/recommendations'), { params: { latitude, longitude } })

      const current = currentRes.data || {};
      const hourly = hourlyRes.data?.hourly_forecast || hourlyRes.data || [];
      const sources = sourcesRes.data || {};
      setData({
        current_aqi: current.current_aqi ?? current.aqi ?? null,
        current_category: current.current_category || categoryForAqi(current.current_aqi),
        timestamp: current.timestamp || new Date().toISOString(),
        hourly_forecast: Array.isArray(hourly) ? hourly : [],
        source_breakdown: sources.source_breakdown || sources.breakdown || {},
        extended_forecast: current.extended_forecast || [],
        location: currentLocation,
        health_recommendations: current.health_recommendations || [],
      });
      setError(null);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchData(); }, []);

  return { data, loading, error, refresh: fetchData, location };
}