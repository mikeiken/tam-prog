import React, { useContext } from "react";
import { CounterContext } from "./CounterContext";

export default function Counter() {
  const { count, increment, decrement, setCountValue } =
    useContext(CounterContext);

  return (
    <div className="counter-wrapper">
      <button className="btn-left" onClick={increment}>
        +
      </button>
      <input type="text" value={count} onChange={setCountValue} />
      <button className="btn-right" onClick={decrement}>
        -
      </button>
    </div>
  );
}
