import React from "react";
import { useNavigate } from "react-router-dom";

export default function Logout() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("accessToken");

    navigate("/");
  };

  return (
    <button className="login-btn" onClick={handleLogout}>
      Выйти
    </button>
  );
}
