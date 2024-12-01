import React, { createContext, useState, useContext, useEffect } from "react";

// Создаем контекст
const BasketContext = createContext();

export const BasketProvider = ({ children }) => {
  const loadBasketItems = () => {
    const savedItems = localStorage.getItem("basketItems");
    return savedItems ? JSON.parse(savedItems) : [];
  };

  const [basketItems, setBasketItems] = useState(loadBasketItems);

  // Сохраняем корзину в localStorage при изменении состояния
  useEffect(() => {
    if (basketItems.length > 0) {
      localStorage.setItem("basketItems", JSON.stringify(basketItems));
    }
  }, [basketItems]);

  const addToBasket = (item) => {
    const currentDate = new Date().toLocaleDateString("ru-RU"); // Получаем дату в формате "день.месяц.год"

    setBasketItems((prevItems) => {
      // Проверяем, есть ли уже такой элемент в корзине
      const exists = prevItems.some((i) => i.id === item.id);
      if (exists) {
        // Если элемент уже есть, просто возвращаем текущий список
        return prevItems.map((i) =>
            i.id === item.id ? { ...i, dateAdded: currentDate } : i
        );
      }
      // Если элемента нет, добавляем его
      return [...prevItems, { ...item, dateAdded: currentDate }];
    });
  };

  const removeFromBasket = (id) => {
    setBasketItems((prevItems) => prevItems.filter((item) => item.id !== id)); // Удаляем элемент по id
  };

  const totalItems = basketItems.length;

  const clearBasket = () => {
    setBasketItems([]);
  };

  return (
    <BasketContext.Provider
      value={{
        totalItems,
        basketItems,
        addToBasket,
        removeFromBasket,
        clearBasket
      }}
    >
      {children}
    </BasketContext.Provider>
  );
};

// Хук для использования контекста
export const useBasket = () => useContext(BasketContext);
