import React from 'react'
import './style.css'
import Form from './form'

export default function AuthFormBackgroundComponent() {
  return (
    <div className='intro'>
      <div className='video'>
        <video autoPlay muted loop='loop' className="background-video">
          <source src={process.env.PUBLIC_URL + '/background1.mp4'} type="video/mp4" />
        </video>
      </div>
      <div className='main-wrapper'>
        <Form />
      </div>
    </div>
  )
}
