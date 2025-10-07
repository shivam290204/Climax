import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000
});

api.interceptors.response.use(
  r => r,
  err => {
    console.error('API error', err?.response?.data || err.message);
    return Promise.reject(err);
  }
);

// Simple in‑memory cache for GETs during a session
const cache = new Map();
async function cachedGet(url, params) {
  const key = url + JSON.stringify(params||{});
  if (cache.has(key)) return cache.get(key);
  const { data } = await api.get(url, { params });
  cache.set(key, data);
  return data;
}

export const ForecastAPI = {
  current: () => cachedGet('/forecast/current'),
  hyperlocal: (lat, lon) => cachedGet('/forecast/hyperlocal', { lat, lon }),
  route: (waypoints) => api.post('/forecast/route', { waypoints }).then(r=>r.data),
  historical: (start, end) => cachedGet('/forecast/historical', { start, end })
};

export const SourcesAPI = {
  current: () => cachedGet('/sources/current'),
  regional: () => cachedGet('/sources/regional'),
  trends: () => cachedGet('/sources/trends'),
  fires: () => cachedGet('/sources/fires')
};

export const PolicyAPI = {
  simulate: (payload) => api.post('/policy/simulate', payload).then(r=>r.data),
  recommendations: () => cachedGet('/policy/recommendations'),
  ongoing: () => cachedGet('/policy/ongoing-interventions'),
  emergency: () => cachedGet('/policy/emergency-response'),
  costBenefit: (payload) => api.post('/policy/cost-benefit-analysis', payload).then(r=>r.data)
};

export const HealthAPI = {
  recommendations: (segment) => cachedGet('/health/recommendations', { segment }),
  alerts: () => cachedGet('/health/alerts'),
};

export const AlertsAPI = {
  active: () => cachedGet('/alerts/active')
};

export default api;
