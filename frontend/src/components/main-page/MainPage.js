import React from 'react';
import './style.css';

export default function MainPage() {
    return (
        <>
            <header className='header-for-landing'> хуй
            </header>
            <div className='landing-page'>
                <center>
                    {/* Можете добавить контент хедера здесь */}
                    <div className='landing'>
                        <img src={process.env.PUBLIC_URL + '/field1.jpg'} alt='field1' />
                        <h1>Мы команда инженеров!</h1>
                        <img src={process.env.PUBLIC_URL + '/field2.jpg'} alt='field2' />
                        <h1>Что мы делаем?</h1>
                    </div>
                </center>
            </div>
        </>
    );
}
