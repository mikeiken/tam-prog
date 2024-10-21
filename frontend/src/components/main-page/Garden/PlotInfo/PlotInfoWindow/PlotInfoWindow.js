import React from 'react';

export default function PlotInfoWindow({ item }) {
    return (
        <div className='container-plot-wrapper'>
            <div className='container-plot-info'>
                <h3>Информация об объекте:</h3>
                <p>ID: {item.id}</p>
                <p>Название: {item.name}</p>
                <p>Описание: {item.description}</p>
            </div>

            <div className='container-plot-products'>
                {/* Можно добавить другую информацию о продукте здесь */}
            </div>
        </div>
    );
}
