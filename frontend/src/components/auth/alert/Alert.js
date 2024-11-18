import React, { useEffect } from 'react';

export default function Alert({ text, className, onClose }) {
    useEffect(() => {
        if (className === 'hide') {
            const timer = setTimeout(() => {
                onClose(); // Убирает Alert из DOM после анимации
            }, 500); // Должно совпадать с длительностью анимации fade-out
            return () => clearTimeout(timer);
        }
    }, [className, onClose]);

    return (
        <div className={`alert ${className}`}>
            <img
                style={{
                    width: '40px',
                    height: '40px',
                }}
                src={process.env.PUBLIC_URL + '/exclamation-mark.png'}
                alt='text'
            />
            {text}
        </div>
    );
}
