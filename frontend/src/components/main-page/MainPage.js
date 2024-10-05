import React, { useState } from 'react';
import Header from '../header/Header';
import Card from '../card/Card';
import AddItemButton from '../add-item/AddItemButton';
import {Routes, Route, Link} from 'react-router-dom';
import AuthForm from '../auth/auth';
import './style.css';

export default function MainPage() {
    const [cards, setCards] = useState([{ label: 'АГУРЭЦ', description: 'ВКУСНАЯЪ' }]);

    const addCard = () => {
        // Добавляем новую карточку, можно сделать динамичнее
        setCards([...cards, { label: 'новая карточка', description: 'описание новой карточки' }]);
    };

    return (
        <div className='h-container'>
            <div className='box1'>
                <Link to='/login'>Login</Link>
            </div>
            <div className='box2'>
                {cards.map((card, index) => (
                    <Card key={index} label={card.label + ` ${index}`} description={card.description} />
                ))}
                <AddItemButton onAdd={addCard} />
            </div>
            <Routes>
                <Route path='/login' element={<AuthForm />} />
            </Routes>
        </div>
    );
}
