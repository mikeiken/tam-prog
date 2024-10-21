import React from 'react'
import './auth-style.css'
import Form from './form'

export default function AuthFormBackgroundComponent() {
  return (
    <div className='intro'>
      <div className='video'>
        {/* Заменяем тег video на img */}
        <img 
          src={process.env.PUBLIC_URL + '/tenor.gif'} 
          alt="Background GIF" 
          className="background-video"
        />
      </div>
      <div className='main-wrapper'>
        <Form />
      </div>
    </div>
  )
}
