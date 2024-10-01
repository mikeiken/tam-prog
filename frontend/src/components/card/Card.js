import React from 'react'
import './style-card.css'
import { useState, useEffect } from 'react'
import Modal from './modal/Modal'
export default function Card(props) {
    const [modalActive, setModalActive] = useState(false)
    return (
        <>
        <div className='card-wrapper' onClick={() => setModalActive(true) }>
            <img src={process.env.PUBLIC_URL + '/CannibalPirate.png'} alt='Placeholder' />
            <h1>{props.label}</h1>
            <p>{props.description}</p>
        </div>
        <Modal active={modalActive} setActive={setModalActive}/>

        </>
    )
}
