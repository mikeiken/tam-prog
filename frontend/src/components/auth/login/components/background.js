import React from "react";
import "./auth-style.css";
import Form from "./form";

export default function AuthFormBackgroundComponent() {
  return (
    <div className="intro">
      <div className="auth-page-wrapper">
        <div className="waves"></div>
        <div className="waves"></div>
        <div className="waves"></div>
        <div className="main-wrapper">
          <Form />
        </div>
      </div>
    </div>
  );
}
