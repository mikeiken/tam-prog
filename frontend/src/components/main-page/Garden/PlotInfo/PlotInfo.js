import React from 'react';
import PlotInfoWindow from './PlotInfoWindow/PlotInfoWindow';

export default function PlotInfo({ selectedItem }) {
    return (
        <div className='box2'>
            {selectedItem ? (
                <PlotInfoWindow item={selectedItem} />
            ) : (
                <p className='select-wrapper text-color ' style={{ '--font-size': '40px' }}>Пожалуйста, выберите объект</p>
            )}
        </div>
    );
}
