import React from 'react'
import { Routes, Route, Link } from 'react-router-dom';
import RegisterForm from '../../../auth/register/RegisterForm';
export default function RegisterBtn() {
    return (
        <>
            <Link className='landing-link' to='/register'>
                <div className='landing-login-btn'>
                    <p>Sing Up</p>
                    <img className='user-interface-login' src={process.env.PUBLIC_URL + '/user-interface-login.png'} alt='user-icon'></img>
                </div>
            </Link>
            <Routes >
                <Route path="/register" element={<RegisterForm />} />

            </Routes>
        </>
    )
}
