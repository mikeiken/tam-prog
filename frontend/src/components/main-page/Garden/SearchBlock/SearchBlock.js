import React from 'react';
import '../garden.css';

export default function SearchBlock() {
    return (
        <div className='box1'>
            <div className='search-block'>
                <input className='search-input' placeholder='Название объекта' />
                <img src={process.env.PUBLIC_URL + '/search.png'} alt='Search Icon' className='search-icon' />
            </div>
        </div>
    );
}
