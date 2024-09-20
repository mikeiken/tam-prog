import React from 'react'

export default function Form() {
  return (
    <div className='wrapper'>
      <form action=''>
        <h1>Login</h1>

        <div className='input-box'>
          <input className='' placeholder='name' type='text' required />
          <img style={{
            position: 'absolute', left: '10px', top: '50%',
            transform: 'translateY(-50%)'
          }}
            src={process.env.PUBLIC_URL + '/user-24.png'}></img>
        </div>

        <div className='input-box'>
          <input className='' placeholder='password' type='password' required />
          <img
            style={{
              position: 'absolute', left: '10px', top: '50%',
              transform: 'translateY(-50%)'
            }}
            src={process.env.PUBLIC_URL + '/lock-24.png'}></img>
        </div>

        <div className='remember'>
          <label for=""> <input type="checkbox" /> Remember me</label>
          <a href="/">Forgot password?</a>
        </div>

        <button type='submit' className='btn'>Login</button>
        <div className='register-link'>
          <p>Don't have an account? <a href='/'>Register</a></p>
        </div>
      </form>
    </div>
  )
}
