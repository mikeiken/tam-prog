import React from 'react'
import { Link } from 'react-router-dom';
export default function Logout() {
    return (
        <Link
            to='/'
        >
            <button className='login-btn'>Выйти</button>
        </Link>
    )
}
