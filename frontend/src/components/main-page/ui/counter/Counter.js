import React, { useContext } from "react";
import { CounterContext } from "./CounterContext";

//! Стилизовать
export default function Counter() {
  const { count, increment, decrement } = useContext(CounterContext);

  return (
    <div>
      <button onClick={increment}>+</button>
      <span>{count}</span>
      <button onClick={decrement}>-</button>
    </div>
  );
}
