import React, { useState } from 'react';
import { Link, Routes, Route, useNavigate } from 'react-router-dom';
import AuthForm from '../login/auth';
import '../login/components/auth-style.css'
import axios from '../../api/instance';
import Alert from '../alert/Alert';

export default function RegisterForm() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [passwordFirst, setPasswordFirst] = useState('');
    const [passwordSecond, setPasswordSecond] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (passwordFirst !== passwordSecond) {
            setErrorMessage('Passwords do not match');
            setShowAlert(true);
            return;
        }

        try {
            const response = await axios.post('/register/', {
                username,
                passwordFirst,
                email,
            });
            localStorage.setItem('accessToken', response.data.access);
            localStorage.setItem('refreshToken', response.data.refresh);
            navigate('/login');
        } catch (error) {
            console.error('Register failed:', error);
            setErrorMessage('Registration failed. Please try again.');
            setShowAlert(true);
        }
    };

    const handleChange = (setter) => (event) => {
        setter(event.target.value);
        setShowAlert(false);
    };

    const [showAlert, setShowAlert] = useState(false);


    return (
        <div className='intro'>
            <div className='video'>
                <img
                    src={process.env.PUBLIC_URL + '/tenor.gif'}
                    alt="Background GIF"
                    className="background-video"
                />
            </div>

            <div className='main-wrapper'>

                <div className='wrapper'>
                    {showAlert && <Alert text={errorMessage} className={showAlert ? '' : 'hide'} />}


                    <form onSubmit={handleSubmit}>
                        <h1>Register</h1>
                        <div className='input-box'>
                            <input className='' type='text' required onChange={handleChange(setUsername)} />
                            <label>Enter your name</label>
                            <img style={{
                                position: 'absolute', left: '10px', top: '50%',
                                transform: 'translateY(-50%)',
                                width: '24px',
                                height: '24px'
                            }}
                                src={process.env.PUBLIC_URL + '/user.png'} alt='text'></img>
                        </div>

                        <div className='input-box'>
                            <input className='' type='email' required onChange={handleChange(setEmail)} />
                            <label>Enter your email</label>
                            <img style={{
                                position: 'absolute', left: '10px', top: '50%',
                                transform: 'translateY(-50%)',
                                width: '24px',
                                height: '24px'
                            }}
                                src={process.env.PUBLIC_URL + '/email.png'} alt='text'></img>
                        </div>

                        <div className='input-box'>
                            <input className='' type='password' required onChange={handleChange(setPasswordFirst)} />
                            <label>Enter your password</label>
                            <img
                                style={{
                                    position: 'absolute', left: '10px', top: '50%',
                                    transform: 'translateY(-50%)',
                                    width: '24px',
                                    height: '24px'
                                }}
                                src={process.env.PUBLIC_URL + '/key-chain.png'} alt='text'>
                            </img>
                        </div>

                        <div className='input-box'>
                            <input className='' type='password' required onChange={handleChange(setPasswordSecond)} />
                            <label>Repeat your password</label>
                            <img
                                style={{
                                    position: 'absolute', left: '10px', top: '50%',
                                    transform: 'translateY(-50%)',
                                    width: '24px',
                                    height: '24px'
                                }}
                                src={process.env.PUBLIC_URL + '/key-chain.png'} alt='text'>
                            </img>
                        </div>

                        <button type='submit' className='btn'>Register</button>
                        <div className='register-link'>
                            <Link to='/'>← Go back</Link>
                        </div>
                    </form>

                    <Routes>
                        <Route path='/login' element={<AuthForm />} />
                    </Routes>
                </div>
            </div >
        </div >
    );
}
