import React from 'react'
import { Link, Routes, Route, useNavigate } from 'react-router-dom';
export default function Logout() {
    return (
        <Link
            to='/'
        >
            <button className='login-btn'>Выйти</button>
        </Link>
    )
}
