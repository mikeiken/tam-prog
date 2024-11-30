import React, { useContext } from "react";
import { CounterContext } from "./CounterContext";

export default function Counter() {
  const { count, increment, decrement, setCountValue } =
    useContext(CounterContext);

  return (
    <div>
      <button onClick={increment}>+</button>
      <input
        type="text" // Меняем тип input на "text" для возможности ввода пустого значения
        value={count}
        onChange={setCountValue}
      />
      <button onClick={decrement}>-</button>
    </div>
  );
}
