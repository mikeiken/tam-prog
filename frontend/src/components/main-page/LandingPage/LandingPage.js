import { useState } from "react";
import "./main.css";
import LoginBtn from "../ui/login-btn/LoginBtn";
import RegisterBtn from "../ui/register-btn/RegisterBtn";

export default function LandingPage() {
  const [loaded, setLoaded] = useState(false);

  const handleLoad = () => {
    setLoaded(true);
  };

  return (
    <>
      <header className="header-for-landing">
        <div>TAMPROG</div>
        <div className="landing-buttons">
          <LoginBtn />
          <RegisterBtn />
        </div>
      </header>
      <div className="landing-page">
        <center>
          <div className="landing">
            <div className="image-container">
              <img
                src={process.env.PUBLIC_URL + "/field1.jpg"}
                alt="field1"
                onLoad={handleLoad}
                className={loaded ? "loaded" : ""}
              />
              <div className="text-overlay">TAMPROG by BSTUTeam</div>
            </div>
            <h1 className="custom-text">Мы команда инженеров!</h1>
            <div className="image-container">
              <img
                src={process.env.PUBLIC_URL + "/field2.jpg"}
                alt="field2"
                onLoad={handleLoad}
                className={loaded ? "loaded" : ""}
              />
              <div className="text-overlay">Что мы делаем?</div>
            </div>
            <div className="image-container">
              <img
                src={process.env.PUBLIC_URL + "/field1.jpg"}
                alt="field1"
                onLoad={handleLoad}
                className={loaded ? "loaded" : ""}
              />
              <div className="text-overlay">Другой текст</div>
            </div>
          </div>
        </center>
      </div>
    </>
  );
}
