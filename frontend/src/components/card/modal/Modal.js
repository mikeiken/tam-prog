import React from 'react'
import './modal-card-style.css'

export default function Modal({ active, setActive }) {
  return (
    <div className={active ? "modal active" : "modal"} onClick={() => setActive(false)}>
      <div className={active ? "modal-content active" : "modal-content"} onClick={e => e.stopPropagation()}>
        <h1>Component</h1>
        <img src={process.env.PUBLIC_URL + '/CannibalPirate.png'} alt={''}></img>
        <p>Description</p>
        <div className='horizontal-direction'>
          <button className='btn-1'>Удобрить</button>
          <button className='btn-2'>Полить</button>
          <button className='btn-3'>Удалить</button>
        </div>
      </div>

    </div>
  )
}
