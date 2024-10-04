import React from 'react'
import './style.css'

export default function Header() {
    return (
        <>
            <div className='header'>
                <img className='logo' src={process.env.PUBLIC_URL + '/logo.png'}></img>
                <nav className='navbar'>
                    <a href='#'>Участки</a>
                    <a href='#'>Подрядчики</a>
                    <a href='#'>Лицензия</a>
                    <a href='#'>О нас</a>
                </nav>
                <button className='login-btn'>Войти</button>
            </div>
        </>
    )
}
