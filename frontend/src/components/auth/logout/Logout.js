import React from "react";
import { useNavigate } from "react-router-dom";
import Instance from "../../api/instance";
import {useBasket} from "../../basket-context/BasketContext";
export default function Logout() {
  const navigate = useNavigate();
  const {clearBasket} = useBasket();

  const handleLogout = async () => {
    try {
      await Instance.post("/logout/");

      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      clearBasket();
      navigate("/");
    } catch (error) {
      console.error("Ошибка при выходе:", error);
    }
  };

  return (
    <button className="login-btn" onClick={handleLogout}>
      Выйти
    </button>
  );
}
