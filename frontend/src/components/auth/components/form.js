import React from 'react';
import { Link, Routes, Route } from 'react-router-dom';
import Garden from '../../main-page/Garden/Garden';

export default function Form() {
  return (
    <div className='wrapper'>
      <form action=''>
        <h1>Login</h1>
        <div className='input-box'>
          <input className='' type='text' required />
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
          <input className='' type='password' required />
          <label>Enter your password</label>
          <img
            style={{
              position: 'absolute', left: '10px', top: '50%',
              transform: 'translateY(-50%)',
              width: '24px', 
              height: '24px'
            }}
            src={process.env.PUBLIC_URL + '/lock.png'} alt='text'>
          </img>
        </div>

        <div className='remember'>
          <label htmlFor=''> <input type='checkbox' /> Remember me</label>
          <a href="/">Forgot password?</a>
        </div>

        <button type='submit' className='btn'>Login</button>
        <div className='register-link'>
          <p>Don't have an account?
            <Link to='/garden'>Register</Link> 
          </p>
        </div>
      </form>

      <Routes>
        <Route path='/garden' element={<Garden />} />
      </Routes>
    </div>
  );
}
