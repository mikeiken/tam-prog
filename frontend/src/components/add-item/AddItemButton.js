import React, { useRef } from 'react';
import './add-item-button.css';

export default function AddItemButton() {
    const buttonRef = useRef(null);

    const handleClick = () => {
        // Добавляем класс вращения
        buttonRef.current.classList.add('rotated');

        // Удаляем класс после завершения анимации
        setTimeout(() => {
            buttonRef.current.classList.remove('rotated');
        }, 200); // Длительность анимации
    };

    return (
        <div>
            <button
                ref={buttonRef} // Привязываем реф к кнопке
                className='add-button'
                onClick={handleClick}
            ></button>
        </div>
    );
}
