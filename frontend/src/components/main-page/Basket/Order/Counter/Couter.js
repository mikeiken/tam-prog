import React, { useState } from "react";
import "./counter.css";
export default function Counter({
  id,
  quantity,
  removeOneFromBasket,
  removeFromBasket,
  item,
  addToBasket,
}) {
  const [count, setCount] = useState(quantity);
  // Функция увеличения количества
  const increase = () => {
    setCount(count + 1);
    addToBasket(item);
  };

  // Функция уменьшения количества
  const decrease = () => {
    if (count > 1) {
      setCount(count - 1); // Уменьшаем количество на 1, если оно больше 1
      removeOneFromBasket(item); // Удаляем 1 элемент из корзины
    } else if (count === 1) {
      setCount(0); // Если количество 1, устанавливаем 0
      removeFromBasket(id); // Удаляем полностью, если количество 1 и нажали минус
    }
  };

  return (
    <div className="counter-container">
      <button className="decrease" onClick={decrease}>
        -
      </button>
      <div className="count">{count}</div>
      <button className="increase" onClick={increase}>
        +
      </button>
    </div>
  );
}
