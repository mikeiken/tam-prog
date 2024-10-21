import React from 'react';

export default function SearchCard({ item, onClick }) {
    return (
        <div className='search-card-wrapper' onClick={onClick}>
            <h4>{item.name}</h4>
            <p>{item.description}</p>
        </div>
    );
}
