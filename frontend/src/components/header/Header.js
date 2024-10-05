import React from 'react'
import './style.css'
import { Routes, Route, Link } from 'react-router-dom';
import AuthForm from '../auth/auth';

export default function Header() {
    return (
        <>
            <div className='header'>
                <img className='logo' src={process.env.PUBLIC_URL + '/logo.png'}></img>
                <nav className='navbar'>

                    <Link to='#'>Участки</Link>
                    <Link to='#'>Подрядчики</Link>
                    <Link to='#'>Лицензия</Link>
                    <Link to='#'>О нас</Link>

                </nav>
                <Link to='/login'>
                    <button className='login-btn'>Войти</button>
                </Link>

            </div>
            <Routes>
                <Route path='/login' element={<AuthForm />} />
            </Routes>
        </>
    )
}
