import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000', // Адрес твоего FastAPI
    withCredentials: true, // ВАЖНО: разрешает передачу cookies
});

export default api;