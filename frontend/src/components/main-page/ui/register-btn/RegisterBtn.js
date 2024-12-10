import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import RegisterForm from "../../../auth/register/RegisterForm";
export default function RegisterBtn() {
  return (
    <>
      <Link className="landing-link" to="/register">
        <div className="landing-login-btn">
          <p>Регистрация</p>
          <img
            className="user-interface-login"
            src={process.env.PUBLIC_URL + "/arrow-left-svgrepo-com.svg"}
            alt="user-icon"
          ></img>
        </div>
      </Link>
      <Routes>
        <Route path="/register" element={<RegisterForm />} />
      </Routes>
    </>
  );
}
