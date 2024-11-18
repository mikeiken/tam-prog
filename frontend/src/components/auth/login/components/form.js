import React, { useState } from "react";
import { Link, Routes, Route, useNavigate } from "react-router-dom";
import axios from "../../../api/instance";
import RegisterForm from "../../register/RegisterForm";

export default function Form() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/login/", {
        username,
        password,
      });
      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);
      navigate("/navigate/garden");
    } catch (error) {
      console.error("Login failed:", error);
      // Handle error (e.g., display message to the user)
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
        <h1>Login</h1>
        <div className="input-box">
          <input
            className=""
            type="text"
            required
            onChange={handleChangeName}
          />
          <label>Enter your name</label>
          <img
            style={{
              position: "absolute",
              left: "10px",
              top: "50%",
              transform: "translateY(-50%)",
              width: "24px",
              height: "24px",
            }}
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
            style={{
              position: "absolute",
              left: "10px",
              top: "50%",
              transform: "translateY(-50%)",
              width: "24px",
              height: "24px",
            }}
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
