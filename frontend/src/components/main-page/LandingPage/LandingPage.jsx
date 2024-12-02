import "./main.css";
import LoginBtn from "../ui/login-btn/LoginBtn";
import RegisterBtn from "../ui/register-btn/RegisterBtn";
import { Link, Route, Routes } from "react-router-dom";
import Header from "../../header/Header";
export default function LandingPage() {
  const state = localStorage.getItem("accessToken");
  return (
    <>
      <header className="page-header">
        <div>TAMPROG</div>
        {state && state.length > 0 ? (
          <Link to="/navigate/garden">
            <div>По коням!</div>
          </Link>
        ) : (
          <div className={"buttons-wrapper"}>
            <LoginBtn />
            <RegisterBtn />
          </div>
        )}
      </header>

      <div className={"landing-main-wrapper"}>
        <div className={"section1"}>
          <div className={"parallax-text"}>BSTUteam</div>
        </div>
        <div className={"section2"}>
          <div className={"parallax-text"}>NORMAL</div>
        </div>
      </div>
      <Routes>
        <Route path="/login" element={<Header />} />
      </Routes>
    </>
  );
}
