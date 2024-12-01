import React from 'react'
import { Routes, Route, Link } from 'react-router-dom';
import AuthForm from '../../../auth/login/auth';
export default function LoginBtn() {
    return (
        <>
            <Link className='landing-link' to='/login'>
                <div className='landing-login-btn'>
                    <img className='user-interface-login' src={process.env.PUBLIC_URL + '/user-interface-login.png'} alt='user-icon'></img>
                    <p>Sing In</p>
                </div>
            </Link>
            <Routes >
                <Route path="/login" element={<AuthForm />} />
            </Routes>
        </>
    )
}
