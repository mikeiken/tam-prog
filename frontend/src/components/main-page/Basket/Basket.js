import React from "react";
import { useBasket } from "../../basket-context/BasketContext";
import Order from "./Order/Order";
import "./basket.css";
import { Context } from "../ui/counter/CounterContext";

export default function Basket() {
  const { addToBasket, basketItems, removeFromBasket, removeOneFromBasket } =
    useBasket();

  return (
    <div className="license-wrapper" style={{ "--font-size": "2em" }}>
      {basketItems.length === 0 ? (
        <div className="basket-empty text-color">Корзина пуста</div>
      ) : (
        <div className="basket-around">
          {basketItems.map((item) => (
            <Context key={item.id}>
              <Order
                key={item.id}
                id={item.id}
                name={item.name}
                price={item.price}
                removeFromBasket={removeFromBasket}
                quantity={item.quantity}
                date={item.dateAdded}
                removeOneFromBasket={removeOneFromBasket}
                item={item}
                addToBasket={addToBasket}
              />
            </Context>
          ))}
        </div>
      )}
    </div>
  );
}
