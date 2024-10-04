import React from 'react'
import './style-card.css'
import { useState, useEffect } from 'react'
import Modal from './modal/Modal'
export default function Card(props) {
    const [modalActive, setModalActive] = useState(false)

    const [isVisible, setIsVisible] = useState(false);
    useEffect(() => {
        const timer = setTimeout(() => {
            setIsVisible(true); // Устанавливаем видимость через 0.1 секунды после монтирования
        }, 100);

        return () => clearTimeout(timer); // Очищаем таймер при размонтировании
    }, []);

    return (
        <>
            <div className={`card-wrapper ${isVisible ? 'fade-in' : ''}`} onClick={() => setModalActive(true)}>
                <img src={process.env.PUBLIC_URL + '/man.jpg'} alt='Placeholder' />
                <h1>{props.label}</h1>
                <p>{props.description}</p>
            </div>
            <Modal active={modalActive} setActive={setModalActive} 
                label={props.label} description={props.description}/>

        </>
    )
}
