import React from "react";

export default function SearchCard({ item, onClick }) {
  return (
    <div className="search-card-wrapper" onClick={onClick}>
      <img className="search-card-img" src="" alt="img"></img>
      <p>
        Название: {item.name}
        <br /> Кол-во грядок:{item.count_beds}
        <br /> Цена: {item.price}
      </p>
    </div>
  );
}
