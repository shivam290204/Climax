import axios from 'axios';

// Basic axios instance factory; caller passes baseURL so each app can decide env.
export function createApiClient(baseURL) {
  const instance = axios.create({ baseURL, timeout: 10000 });
  instance.interceptors.response.use(r => r, err => {
    // Could add centralized logging later
    return Promise.reject(err);
  });
  return instance;
}
