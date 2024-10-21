import React from 'react';

export default function SearchCard({ item, onClick }) {
  return (
    <div className='search-card-wrapper' onClick={onClick}>
      <img className='search-card-img' src=''></img>
      <p>{item.name}<br /> {item.description}</p>
    </div>
  );
}
