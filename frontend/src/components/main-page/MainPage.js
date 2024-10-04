import React, { useState } from 'react';
import Header from '../header/Header';
import Card from '../card/Card';
import AddItemButton from '../add-item/AddItemButton';
import './style.css';

export default function MainPage() {
    const [cards, setCards] = useState([{ label: 'АГУРЭЦ', description: 'ВКУСНАЯЪ' }]);

    const addCard = () => {
        // Добавляем новую карточку, можно сделать динамичнее
        setCards([...cards, { label: 'новая карточка', description: 'описание новой карточки' }]);
    };

    return (
        <div className='main-container'>
            <Header />
            <div className='h-container'>
                <div className='box1'>
                    наверное выбор всякой всячины
                </div>
                <div className='box2'>
                    {cards.map((card, index) => (
                        <Card key={index} label={card.label + ` ${index}`} description={card.description} />
                    ))}
                    <AddItemButton onAdd={addCard} />
                </div>
            </div>
        </div>
    );
}
