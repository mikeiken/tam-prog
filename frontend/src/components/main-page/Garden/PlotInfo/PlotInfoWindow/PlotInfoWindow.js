import React, { useState, useEffect } from 'react';

export default function PlotInfoWindow({ item }) {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        if (item) {
            setIsVisible(true);
        } else {
            setIsVisible(false);
        }
    }, [item]);

    return (
        <div className={`container-plot-wrapper ${isVisible ? 'visible' : ''}`}>
            <div className='container-plot-info'>
                <h3>Информация об объекте:</h3>
                <p>ID: {item.id}</p>
                <p>Название: {item.name}</p>
                <p>Описание: {item.description}</p>
            </div>

            <div className='container-plot-products'>
                <h1>ID: {item.id}</h1>

            </div>
        </div>
    );
}
