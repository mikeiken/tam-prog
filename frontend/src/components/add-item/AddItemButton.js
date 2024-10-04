import React from 'react';
import './add-item-button.css';

export default function AddItemButton({ onAdd }) {

    return (
        <div>
            <button
                className='add-button'
                onClick={onAdd}
            ></button>
        </div>
    );
}
