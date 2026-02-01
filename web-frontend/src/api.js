import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/',
});

// Add a request interceptor if we implement token auth later
// For now, Basic Auth is handled in components or global config if needed
// Or we can set a default Authorization header if we have a token

export default api;
