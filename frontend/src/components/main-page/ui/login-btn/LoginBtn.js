import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import AuthForm from "../../../auth/login/auth";
export default function LoginBtn() {
  return (
    <>
      <Link className="landing-link" to="/login">
        <div className="landing-login-btn">
          <img
            className="user-interface-login"
            src={process.env.PUBLIC_URL + "/arrow-right-svgrepo-com.svg"}
            alt="user-icon"
          ></img>
          <p>Войти</p>
        </div>
      </Link>
      <Routes>
        <Route path="/login" element={<AuthForm />} />
      </Routes>
    </>
  );
}
