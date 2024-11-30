import React, { useContext } from "react";
import { CounterContext } from "./CounterContext";

export default function Counter() {
  const { count, increment, decrement, setCountValue } =
    useContext(CounterContext);

  return (
    <div className="counter-wrapper">
      <button onClick={increment}>+</button>
      <input type="text" value={count} onChange={setCountValue} />
      <button onClick={decrement}>-</button>
    </div>
  );
}
