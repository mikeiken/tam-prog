import React from 'react'
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import AuthForm from '../../../auth/auth';
export default function LoginBtn() {
    return (
        <>
            <Link className='landing-link' to='/login'>
                <div className='landing-login-btn'>
                    <img className='user-interface-login' src={process.env.PUBLIC_URL + '/user-interface-login.png'} alt='user-icon'></img>
                    <p> Login</p>
                </div>
            </Link>
            <Routes >
                <Route path="/login" element={<AuthForm />} />

            </Routes>
        </>
    )
}
