import axios from 'axios'

// function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
// }

// const xsrfToken = getCookie('XSRF-TOKEN');


const Instance = axios.create({
    baseURL: 'http://localhost/api/v1',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
})


export default Instance