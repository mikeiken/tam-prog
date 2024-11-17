import axios from 'axios';

const Instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

Instance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

Instance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (
            error.response.status === 401 &&
            !originalRequest._retry &&
            localStorage.getItem('refreshToken')
        ) {
            originalRequest._retry = true;
            try {
                const refreshToken = localStorage.getItem('refreshToken');
                const response = await axios.post('/token/refresh/', { refresh: refreshToken });
                localStorage.setItem('accessToken', response.data.access);
                originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
                return axios(originalRequest);
            } catch (refreshError) {
                console.error('Token refresh failed:', refreshError);
                // Handle refresh token failure (e.g., redirect to login)
            }
        }
        return Promise.reject(error);
    }
);


export default Instance;
