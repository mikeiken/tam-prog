import React from 'react';
import { Navigate } from 'react-router-dom';
import NotFound from '../../not-found/NotFound';

// Функция, которая проверяет, авторизован ли пользователь
const PrivateRoute = ({ children }) => {
    const isAuthenticated = localStorage.getItem('accessToken'); // или другой механизм авторизации

    // Если пользователь не авторизован, показываем страницу NotFound
    if (!isAuthenticated) {
        return <NotFound />;
    }

    // Если авторизован, рендерим переданные дочерние компоненты
    return children;
};

export default PrivateRoute;
