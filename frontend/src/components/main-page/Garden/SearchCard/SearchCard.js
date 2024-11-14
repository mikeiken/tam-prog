import React from 'react';

export default function SearchCard({ item, onClick }) {
  return (
    <div className='search-card-wrapper' onClick={onClick}>
      <img className='search-card-img' src=''></img>
      <p>Название: {item.state}<br /> Площадь:{item.size}<br/> Цена: {item.price}</p>
    </div>
  );
}
