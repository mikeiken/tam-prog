import React from 'react'
import './modal-card-style.css'

export default function Modal(props) {
  return (
    <div className={props.active ? "modal active" : "modal"} onClick={() => props.setActive(false)}>
      <div className={props.active ? "modal-content active" : "modal-content"} onClick={e => e.stopPropagation()}>
        <h1>{props.label}</h1>
        <img src={process.env.PUBLIC_URL + '/man.jpg'} alt={''}></img>
        <p>{props.description}</p>
        <div className='horizontal-direction'>
          <button className='btn-1'>Удобрить</button>
          <button className='btn-2'>Полить</button>
          <button className='btn-3'>Удалить</button>
        </div>
      </div>

    </div>
  )
}
