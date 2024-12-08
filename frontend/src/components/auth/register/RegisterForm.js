import React, { useState } from "react";
import { Link, Routes, Route, useNavigate } from "react-router-dom";
import AuthForm from "../login/auth";
import "../login/components/auth-style.css";
import Instance from "../../api/instance";
import {useNotification} from "../../context/NotificationContext";

export default function RegisterForm() {
  const [login, setLogin] = useState("");
  const [username, setUsername] = useState("");
  const [phone, setPhone] = useState("");
  const [passwordFirst, setPasswordFirst] = useState("");
  const [passwordSecond, setPasswordSecond] = useState("");
  const {addNotification} = useNotification();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (passwordFirst !== passwordSecond) {
      addNotification("Passwords do not match", "warning");
      return;
    }

    try {
      await Instance.post("/register/", {
        username: login,
        full_name: username,
        phone_number: phone,
        password: passwordFirst,
      });

      navigate("/login");
    } catch (error) {
      if (error.response && error.response.data) {
        for (const err of Object.entries(error.response.data)) {
          addNotification(`${err}`, "error");
        }
      } else {
        addNotification("An error occurred. Please try again.", "error");
      }
    }
  };


  const handleChange = (setter) => (event) => {
    setter(event.target.value);
  };


  return (
    <div className="intro">
      <div className="auth-page-wrapper">
        <div className="waves"></div>
        <div className="waves"></div>
        <div className="waves"></div>

        <div className="main-wrapper">
          <div className="wrapper">
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
    </div>
  );
}
