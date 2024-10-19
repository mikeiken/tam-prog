import axios from 'axios'

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const xsrfToken = getCookie('XSRF-TOKEN');


const Instance = axios.create({
    baseURL: 'http://homelab.kerasi.ru/api/v1',
    timeout: 5000,
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Accept': 'application/json',
        'X-XSRF-TOKEN': xsrfToken,
    },
    xsrfCookieName: 'XSRF-TOKEN',
    xsrfHeaderName: 'X-XSRF-TOKEN',
})


export default Instance