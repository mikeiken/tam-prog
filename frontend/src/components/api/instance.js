import axios from 'axios'

export const Instance = axios.create({
    baseURL: 'localhost:8000',
    timeout: 5000,
    headers: {
        Accept: 'application/json',
        xsrfCookieName: 'XSRF-TOKEN',
        xsrfHeaderName: 'X-XSRF-TOKEN',
    }
})

export const Routes = {
    AUTH_ROUTES: {
        login: '/login',
        logout: '/logout',
    },
    PRODUCTS: {
        plant: '/plant',
        
    },
}
