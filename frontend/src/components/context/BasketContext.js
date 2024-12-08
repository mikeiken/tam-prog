import React, {createContext, useState, useContext, useEffect} from "react";
import {useNotification} from "./NotificationContext";

const BasketContext = createContext();

export const BasketProvider = ({children}) => {
    const {addNotification} = useNotification();
    const loadBasketItems = () => {
        const savedItems = localStorage.getItem("basketItems");
        return savedItems ? JSON.parse(savedItems) : [];
    };

    const [basketItems, setBasketItems] = useState(loadBasketItems);

    // Сохраняем корзину в localStorage при любом изменении состояния
    useEffect(() => {
        localStorage.setItem("basketItems", JSON.stringify(basketItems));
    }, [basketItems]);

    const addToBasket = (item) => {
        const currentDate = new Date().toLocaleDateString("ru-RU");

        setBasketItems((prevItems) => {
            const exists = prevItems.some((i) => i.id === item.id);
            if (exists) {
                addNotification(`Объект ${item.name} уже в корзине`, "warning");

                return prevItems.map((i) =>
                    i.id === item.id ? {...i, dateAdded: currentDate} : i
                );
            }
            addNotification(`Объект ${item.name} добавлен в корзину`, "success")
            return [...prevItems, {...item, dateAdded: currentDate}];
        });
    };

    const removeFromBasket = (item) => {
        setBasketItems((prevItems) => prevItems.filter((item) => item.id !== item.id));
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
                clearBasket,
            }}
        >
            {children}
        </BasketContext.Provider>
    );
};

export const useBasket = () => useContext(BasketContext);
