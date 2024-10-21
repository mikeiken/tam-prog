import React from 'react';
import PlotInfoWindow from './PlotInfoWindow/PlotInfoWindow';

export default function PlotInfo({ selectedItem }) {
    return (
        <div className='box2'>
            {selectedItem ? (
                <PlotInfoWindow item={selectedItem} />
            ) : (
                <p>Пожалуйста, выберите объект</p>
            )}
        </div>
    );
}
