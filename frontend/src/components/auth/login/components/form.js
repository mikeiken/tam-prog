import React, { useState } from "react";
import { Link, Routes, Route, useNavigate } from "react-router-dom";
import RegisterForm from "../../register/RegisterForm";
import Instance from "../../../api/instance";
import Welcome from "./welocme/Welcome";
import {useNotification} from "../../../context/NotificationContext";

export default function Form() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { addNotification } = useNotification();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      localStorage.removeItem("wallet_balance");
      localStorage.removeItem("user_id");
      const response = await Instance.post("/login/", {
        username,
        password,
      });
      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);
      localStorage.setItem("wallet_balance", response.data.wallet_balance);
      localStorage.setItem("user_id", response.data.id);
      navigate("/navigate/garden");
      //alert("Приветствуем вас!");
    } catch (error) {
      const errorMessage =
          error.response?.data?.detail || // Попробуйте взять сообщение с сервера
          error.message ||               // Если нет, используйте сообщение ошибки
          "An unknown error occurred";   // Запасной вариант
      addNotification(errorMessage, "error");
    }
  };

  const handleChangeName = (event) => {
    setUsername(event.target.value);
  };

  const handleChangePassword = (event) => {
    setPassword(event.target.value);
  };

  return (
    <div className="wrapper">
      <form onSubmit={handleSubmit}>
        <div className="welcome-show">
          <Welcome />
        </div>
        <div className="input-box">
          <input
            className=""
            type="text"
            required
            onChange={handleChangeName}
          />
          <label>Enter your name</label>
          <img
            className="user-icon-auth"
            src={process.env.PUBLIC_URL + "/user.png"}
            alt="text"
          ></img>
        </div>

        <div className="input-box">
          <input
            className=""
            type="password"
            required
            onChange={handleChangePassword}
          />
          <label>Enter your password</label>
          <img
            className="user-icon-auth"
            src={process.env.PUBLIC_URL + "/key-chain.png"}
            alt="text"
          ></img>
        </div>

        <div className="remember">
          <label htmlFor="">
            {" "}
            <input type="checkbox" /> Remember me
          </label>
          <a href="/">Forgot password?</a>
        </div>

        <button type="submit" className="btn">
          Login
        </button>
        <div className="register-link">
          <p>
            Don't have an account?
            <Link to="/register">Register</Link>
          </p>
        </div>
      </form>

      <Routes>
        <Route path="/register" element={<RegisterForm />} />
      </Routes>
    </div>
  );
}
