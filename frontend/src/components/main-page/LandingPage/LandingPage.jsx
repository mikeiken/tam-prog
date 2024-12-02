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
        <div className="modern">TAMPROG</div>
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
          <div className={"parallax-text"}>
            <h2
              style={{
                marginBottom: "0",
                marginTop: "20px",
                textShadow: "1px 1px 2px rgba(0, 0, 0, 0.1)",
              }}
            >
              BSTUteam
            </h2>
            <h3
              style={{
                margin: "0",
                textShadow: "1px 1px 2px rgba(0, 0, 0, 0.1)",
                fontSize: "35px",
              }}
            >
              представляет
            </h3>
          </div>
        </div>

        <div
          className={"section2"}
          style={{
            background:
              "linear-gradient(to top, #282528 0%, rgba(40, 37, 40, 0) 95%)",
          }}
        >
          <div className="dream-team">
            <div className="dream-team-container">
              <div
                style={{
                  width: "370px",
                  display: "flex",
                  justifyContent: "right",
                }}
              >
                <div className="developer-wrapper denis">
                  <img
                    className="developer-img"
                    src={process.env.PUBLIC_URL + "/students/Денис.png"}
                    alt="img"
                    style={{
                      width: "150px",
                    }}
                  ></img>
                  <div
                    className="popup"
                    style={{
                      top: "-90px",
                      left: "100px",
                      width: "150px",
                      background:
                        "radial-gradient(circle, yellow 5%, orange 50%)",
                    }}
                  >
                    <h2
                      style={{
                        display: "flex",
                        justifyContent: "center",
                      }}
                    >
                      Денис
                    </h2>
                    <p>Наш DevOps инженер</p>
                  </div>
                </div>
              </div>

              <div
                style={{
                  width: "400px",
                  display: "flex",
                  justifyContent: "left",
                  position: "relative",
                  height: "100px",
                }}
              >
                <div className="developer-wrapper leonid">
                  <img
                    className="developer-img"
                    src={process.env.PUBLIC_URL + "/students/Леонид.png"}
                    alt="img"
                  />
                  <div
                    className="popup"
                    style={{
                      top: "-110px",
                      width: "170px",
                      background:
                        "radial-gradient(circle, #E9EAA0 5%, #11B278 50%)",
                    }}
                  >
                    <h2
                      style={{
                        display: "flex",
                        justifyContent: "center",
                      }}
                    >
                      Леонид
                    </h2>
                    <p>Наш Front-End разработчик</p>
                  </div>
                </div>
              </div>

              <div
                style={{
                  width: "400px",
                  display: "flex",
                  justifyContent: "right",
                }}
              >
                <div className="developer-wrapper anastasiya">
                  <img
                    className="developer-img"
                    src={process.env.PUBLIC_URL + "/students/Анастасия.png"}
                    alt="img"
                  ></img>
                  <div
                    className="popup"
                    style={{
                      top: "-90px",
                      left: "80px",
                      width: "170px",
                      background:
                        "radial-gradient(circle, #F5B2CE 15%, #E74792 100%)",
                    }}
                  >
                    <h2
                      style={{
                        display: "flex",
                        justifyContent: "center",
                      }}
                    >
                      Анастасия
                    </h2>
                    <p>Наш Back-End разработчик</p>
                  </div>
                </div>
              </div>

              <div
                style={{
                  width: "400px",
                  display: "flex",
                  justifyContent: "left",
                }}
              >
                <div className="developer-wrapper nikolay">
                  <img
                    className="developer-img"
                    src={process.env.PUBLIC_URL + "/students/Николай.png"}
                    alt="img"
                  ></img>
                  <div
                    className="popup"
                    style={{
                      left: "-130px",
                      top: "-90px",
                      background:
                        "radial-gradient(circle, #E3F1F8 5%, #40BBE7 50%)",
                    }}
                  >
                    <h2
                      style={{
                        display: "flex",
                        justifyContent: "center",
                      }}
                    >
                      Николай
                    </h2>
                    <p>Наш Тестировщик</p>
                  </div>
                </div>
              </div>
              <div
                style={{
                  width: "400px",
                  display: "flex",
                  justifyContent: "right",
                }}
              >
                <div className="developer-wrapper daria">
                  <img
                    className="developer-img"
                    src={process.env.PUBLIC_URL + "/students/Дарья.png"}
                    alt="img"
                  ></img>
                  <div
                    className="popup"
                    style={{
                      left: "80px",
                      background:
                        "radial-gradient(circle, #FEAA56 15%, #F67028 50%)",
                      width: "150px",
                      height: "120px",
                    }}
                  >
                    <h2
                      style={{
                        display: "flex",
                        justifyContent: "center",
                      }}
                    >
                      Дарья
                    </h2>
                    <p>Наш Дизайнер</p>
                  </div>
                </div>
              </div>
            </div>
            <div
              className={"default-text"}
              style={{
                fontSize: "40px",
                width: "400px",
                textAlign: "start",
              }}
            >
              Мы – команда инженеров, которая делает управление виртуальными
              грядками проще и удобнее!
            </div>
          </div>
        </div>
        <div
          className={"section2"}
          style={{
            // backgroundImage: `url(${process.env.PUBLIC_URL + "/ferma.jpg"})`,
            backgroundColor: "#282528",
          }}
        >
          <div
            className={"parallax-text"}
            style={{
              fontSize: "41px",
            }}
          >
            <h1
              style={{
                display: "flex",
                justifyContent: "center",
                fontSize: "120px",
              }}
            >
              ТАМПРОГ
            </h1>{" "}
            – автоматизация, которая работает для <u>Вас</u> и вашего урожая.
          </div>
        </div>
      </div>
      <Routes>
        <Route path="/login" element={<Header />} />
      </Routes>
    </>
  );
}
