import React, { createContext } from "react";

export const CounterContext = createContext();

export const Context = (props) => {
  const [count, setCount] = React.useState("1");
  const maxLength = 10; // Максимальная длина числа (например, 10 цифр)

  function setCountValue(e) {
    const value = e.target.value;

    // Проверка, если введенное значение больше, чем количество доступных мест
    if (parseInt(value) > props.free_beds) {
      setCount(props.free_beds.toString()); // Обновляем значение до свободных мест
      return;
    }

    // Если строка состоит только из нулей, устанавливаем значение как "0"
    if (/^0+$/.test(value)) {
      setCount("0");
      return;
    }

    // Ограничиваем количество цифр
    if (value === "" || /^[0-9]*$/.test(value)) {
      if (value.length <= maxLength) {
        setCount(value); // Обновляем состояние только если длина значения не превышает maxLength
      }
    }
  }

  function increment() {
    setCount((prevCount) => {
      const newCount = Math.min(parseInt(prevCount) + 1, props.free_beds); // Ограничение максимальным числом
      return newCount.toString();
    });
  }

  function decrement() {
    setCount((prevCount) => {
      const newCount = Math.max(parseInt(prevCount) - 1, 0);
      return newCount.toString();
    });
  }

  const value = {
    count,
    increment,
    decrement,
    setCountValue,
  };

  return (
    <CounterContext.Provider value={value}>
      {props.children}
    </CounterContext.Provider>
  );
};
