import React from 'react'
import { Routes, Route, Link, useLocation } from 'react-router-dom';
export default function LoginBtn() {
    return (
        <Link className='landing-link' to='/login'>
            <div className='landing-login-btn'>
                <img className='user-interface-login' src={process.env.PUBLIC_URL + '/user-interface-login.png'} alt='user-icon'></img>
                <a> Login</a>
            </div>
        </Link>
    )
}
