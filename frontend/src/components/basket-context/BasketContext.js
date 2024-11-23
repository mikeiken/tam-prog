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
      const existingItem = prevItems.find((i) => i.id === item.id);
      if (existingItem) {
        return prevItems.map((i) =>
          i.id === item.id
            ? { ...i, quantity: i.quantity + 1, dateAdded: currentDate } // Добавляем или обновляем дату
            : i
        );
      }
      return [
        ...prevItems,
        { ...item, quantity: 1, dateAdded: currentDate }, // Добавляем дату добавления
      ];
    });
  };

  // Функция для удаления 1 единицы элемента из корзины
  const removeOneFromBasket = (id) => {
    setBasketItems((prevItems) => {
      const updatedItems = prevItems
        .map((item) =>
          item.id === id ? { ...item, quantity: item.quantity - 1 } : item
        )
        .filter((item) => item.quantity > 0); // Убираем элементы с нулевым количеством
      return updatedItems;
    });
  };

  // Функция для полного удаления элемента из корзины
  const removeFromBasket = (id) => {
    setBasketItems((prevItems) => prevItems.filter((item) => item.id !== id)); // Удаляем элемент по id
  };

  return (
    <BasketContext.Provider
      value={{
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
