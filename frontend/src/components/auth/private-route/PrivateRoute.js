import React from "react";
import { Navigate } from "react-router-dom";

const PrivateRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem("accessToken"); // Проверка авторизации

  // Если пользователь не авторизован, перенаправляем на страницу 404 или на логин
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Возвращаем дочерние элементы или вложенные маршруты через Outlet
  return <>{children}</>;
};

export default PrivateRoute;
