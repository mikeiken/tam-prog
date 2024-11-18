import React, { useState } from "react";
import { Link, Routes, Route, useNavigate } from "react-router-dom";
import AuthForm from "../login/auth";
import "../login/components/auth-style.css";
import Alert from "../alert/Alert";
import Instance from "../../api/instance";

export default function RegisterForm() {
  const [login, setLogin] = useState("");
  const [username, setUsername] = useState("");
  const [phone, setPhone] = useState("");
  const [passwordFirst, setPasswordFirst] = useState("");
  const [passwordSecond, setPasswordSecond] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (passwordFirst !== passwordSecond) {
      setErrorMessage("Passwords do not match");
      setShowAlert(true);
      return;
    }

    try {
      const response = await Instance.post("/register/", {
        username: login,
        full_name: username,
        phone_number: phone,
        password: passwordFirst,
      });

      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);
      navigate("/login");
      alert("Регистрация прошла успешно!");
    } catch (error) {
      console.error("Register failed:", error);
      setErrorMessage("Registration failed. Please try again.");
      setShowAlert(true);
    }
  };

  const handleChange = (setter) => (event) => {
    setter(event.target.value);
    setShowAlert(false);
  };

  const [showAlert, setShowAlert] = useState(false);

  return (
    <div className="intro">
      <div className="video">
        <img
          src={process.env.PUBLIC_URL + "/tenor.gif"}
          alt="Background GIF"
          className="background-video"
        />
      </div>

      <div className="main-wrapper">
        <div className="wrapper">
          {showAlert && (
            <Alert text={errorMessage} className={showAlert ? "" : "hide"} />
          )}

          <form onSubmit={handleSubmit}>
            <h1>Register</h1>
            <div className="input-box">
              <input
                className=""
                type="text"
                required
                onChange={handleChange(setUsername)}
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
                type="text"
                required
                onChange={handleChange(setLogin)}
              />
              <label>Enter your login</label>
              <img
                className="user-icon-auth"
                src={process.env.PUBLIC_URL + "/user.png"}
                alt="text"
              ></img>
            </div>

            <div className="input-box">
              <input
                className=""
                type="phone"
                required
                onChange={handleChange(setPhone)}
              />
              <label>Enter your phone</label>
              <img
                className="user-icon-auth"
                src={process.env.PUBLIC_URL + "/phone.png"}
                alt="text"
              ></img>
            </div>

            <div className="input-box">
              <input
                className=""
                type="password"
                required
                onChange={handleChange(setPasswordFirst)}
              />
              <label>Enter your password</label>
              <img
                className="user-icon-auth"
                src={process.env.PUBLIC_URL + "/key-chain.png"}
                alt="text"
              ></img>
            </div>

            <div className="input-box">
              <input
                className=""
                type="password"
                required
                onChange={handleChange(setPasswordSecond)}
              />
              <label>Repeat your password</label>
              <img
                className="user-icon-auth"
                src={process.env.PUBLIC_URL + "/key-chain.png"}
                alt="text"
              ></img>
            </div>

            <button type="submit" className="btn">
              Register
            </button>
            <div className="register-link">
              <Link to="/">← Go back</Link>
            </div>
          </form>

          <Routes>
            <Route path="/login" element={<AuthForm />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}
