import React, { createContext } from "react";

export const CounterContext = createContext();
export const Context = (props) => {
  const [count, setCount] = React.useState(0);

  function increment() {
    setCount(count + 1);
  }

  function decrement() {
    if (count === 0 || count < 0) {
      setCount(0);
    } else {
      setCount(count - 1);
    }
  }

  const value = {
    count,
    increment,
    decrement,
  };

  return (
    <CounterContext.Provider value={value}>
      {props.children}
    </CounterContext.Provider>
  );
};
