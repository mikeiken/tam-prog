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

        <div
          className={"section2"}
          style={{
            background:
              "linear-gradient(to top, #282828 0%, rgba(40, 40, 40, 0) 95%)",
            // boxShadow: "0 -30px 60px rgba(0, 0, 0, 0.8)",
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
                      left: "130px",
                      width: "150px",
                      background:
                        "radial-gradient(circle, yellow 5%, orange 50%)",
                    }}
                  >
                    <h2>Наш DevOps инженер</h2>
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
                    <h2>Наш Front-End разработчик</h2>
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
                      top: "-80px",
                      left: "110px",
                      width: "170px",
                      background:
                        "radial-gradient(circle, #F5B2CE 15%, #E74792 100%)",
                    }}
                  >
                    <h2>Наш Back-End разработчик</h2>
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
                      left: "-200px",
                      top: "-90px",
                      background:
                        "radial-gradient(circle, #E3F1F8 5%, #40BBE7 50%)",
                    }}
                  >
                    <h2>Наш Тестировщик</h2>
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
                      left: "130px",
                      background:
                        "radial-gradient(circle, #FEAA56 15%, #F67028 50%)",
                    }}
                  >
                    <h2>Наш Дизайнер</h2>
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
            backgroundImage: `url(${process.env.PUBLIC_URL + "/ferma.jpg"})`,
          }}
        >
          <div
            className={"parallax-text"}
            style={{
              fontSize: "31px",
            }}
          >
            ТАМПРОГ – автоматизация, которая работает для вас и вашего урожая.
          </div>
        </div>
        <div
          className={"section2"}
          style={{
            backgroundColor: "#282528",
          }}
        >
          <div className={"parallax-text"}>
            <div
              style={{
                fontSize: "14px",
              }}
            >
              Сажайте, ухаживайте, собирайте – всё в один клик, где бы вы ни
              находились.
            </div>
            <div
              style={{
                fontSize: "14px",
              }}
            >
              Управляйте растениями удаленно – от аренды до сбора урожая с нашей
              системой.
            </div>
          </div>
        </div>
      </div>
      <Routes>
        <Route path="/login" element={<Header />} />
      </Routes>
    </>
  );
}
