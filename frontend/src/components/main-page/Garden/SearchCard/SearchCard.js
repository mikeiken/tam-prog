import React from "react";
import { useBasket } from "../../../basket-context/BasketContext";
export default function SearchCard({ item, onClick }) {
  const { addToBasket } = useBasket();
  return (
    <div className="search-card-wrapper" onClick={onClick}>
      <div className="search-card-wrapper-v2">
        <img
          className="search-card-img"
          src="https://avatars.mds.yandex.net/i?id=b4560f26cb2f9fab2f7395b28c1fed50_l-5236855-images-thumbs&n=13"
          alt="img"
        ></img>
        <div>
          <p className="text-into-search-card">
            {item.name}, {item.id}
            <br /> Cвободно {item.count_free_beds} грядок
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
