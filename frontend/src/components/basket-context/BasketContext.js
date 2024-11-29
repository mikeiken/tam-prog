import React, { createContext, useState, useContext, useEffect } from "react";

// Создаем контекст
const BasketContext = createContext();

// Провайдер контекста для оборачивания компонентов
export const BasketProvider = ({ children }) => {
  // Получаем данные из localStorage или начинаем с пустого массива
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

  const removeOneFromBasket = (id) => {
    setBasketItems((prevItems) => {
      return prevItems
        .map((item) =>
          item.id === id ? { ...item, quantity: item.quantity - 1 } : item
        )
        .filter((item) => item.quantity > 0); // Убираем элементы с нулевым количеством
    });
  };

  const removeFromBasket = (id) => {
    setBasketItems((prevItems) => prevItems.filter((item) => item.id !== id)); // Удаляем элемент по id
  };

  const totalItems = basketItems.length;

  return (
    <BasketContext.Provider
      value={{
        totalItems,
        basketItems,
        addToBasket,
        removeFromBasket,
        removeOneFromBasket,
      }}
    >
      {children}
    </BasketContext.Provider>
  );
};

// Хук для использования контекста
export const useBasket = () => useContext(BasketContext);
