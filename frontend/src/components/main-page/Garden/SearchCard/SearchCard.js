import React from "react";
import { useBasket } from "../../../basket-context/BasketContext";
export default function SearchCard({ item, onClick }) {
  const { addToBasket } = useBasket();
  return (
    <div className="search-card-wrapper" onClick={onClick}>
      <div className="search-card-wrapper-v2">
        <img className="search-card-img" src={""} alt="img"></img>
        <div>
          <p>
            Название: {item.name}
            <br /> Кол-во грядок: {item.count_free_beds} шт
            <br /> Цена: {item.price} Рублей
          </p>
        </div>
      </div>
      <div className="add-to-basket" onClick={() => addToBasket(item)}>
        <img
          className="add-to-basket-img"
          src={process.env.PUBLIC_URL + "/plus.svg"}
          alt="img"
        ></img>
      </div>
    </div>
  );
}
