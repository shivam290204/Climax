// Central configuration for the mobile app API base URL.
// Priority:
// 1. EXPO_PUBLIC_API_BASE (at build/runtime via Expo)
// 2. Hardcoded fallback to localhost (simulator only)
// 3. NOTE: Physical devices cannot reach 127.0.0.1/localhost on your PC; replace with LAN IP.

const DEFAULT_FALLBACK = 'http://127.0.0.1:8000/api/v1';

// On Expo you can define EXPO_PUBLIC_API_BASE in app config or .env.*
export const API_BASE = (process.env.EXPO_PUBLIC_API_BASE || DEFAULT_FALLBACK).replace(/\/$/, '');

export const buildUrl = (path) => `${API_BASE}${path.startsWith('/') ? path : '/' + path}`;

export const configInfo = () => ({
  API_BASE,
  note: 'Set EXPO_PUBLIC_API_BASE for production or device testing.'
});
