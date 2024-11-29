import React, { useRef, useState, useEffect } from "react";
import { Routes, Route, Link, useLocation } from "react-router-dom";
import Garden from "../main-page/Garden/Garden";
import About from "../main-page/About/about";
import Basket from "../main-page/Basket/Basket";
import Contractor from "../main-page/Contractor/Contractor";
import { useBasket } from "../basket-context/BasketContext";
import { CSSTransition, SwitchTransition } from "react-transition-group";
import "../main-page/style.css";
import Logout from "../auth/logout/Logout";

export default function Header() {
  const location = useLocation();
  const { totalItems } = useBasket();
  const [showIndicator, setShowIndicator] = useState(false);
  const [lastBasketCount, setLastBasketCount] = useState(0);

  const routes = [
    { path: "garden", Component: Garden },
    { path: "about", Component: About },
    { path: "license", Component: Basket },
    { path: "contractor", Component: Contractor },
  ];

  const isActivePath = (path) => location.pathname === path;


  useEffect(() => {
    if (location.pathname === "/navigate/license") {
      setLastBasketCount(totalItems);
      setShowIndicator(false);
      setTimeout(() => setShowIndicator(false), 300); // Удалить из DOM после завершения анимации
    } else if (totalItems > lastBasketCount) {
      setShowIndicator(true);
      setTimeout(() => setShowIndicator(true), 0); // Добавить анимацию
    }
  }, [location.pathname, totalItems, lastBasketCount]);

  const transitionRef = useRef(null);

  return (
      <>
        <header className="header">
          <img
              className="logo"
              src={process.env.PUBLIC_URL + "/logo.png"}
              alt="Logo"
          />
          <nav className="navbar">
            <Link
                to="garden"
                onClick={(e) =>
                    isActivePath("/navigate/garden") && e.preventDefault()
                }
            >
              Участки
            </Link>
            <Link
                to="contractor"
                onClick={(e) =>
                    isActivePath("/navigate/contractor") && e.preventDefault()
                }
            >
              Личный кабинет
            </Link>
            <div className="basket-link-wrapper">
              <Link
                  to="license"
                  onClick={(e) =>
                      isActivePath("/navigate/license") && e.preventDefault()
                  }
              >
                Корзина
              </Link>
              {showIndicator && (
                  <div className={`basket-indicator ${!showIndicator ? "hidden" : ""}`}>
                    {totalItems}
                  </div>
              )}
            </div>
            <Link
                to="about"
                onClick={(e) =>
                    isActivePath("/navigate/about") && e.preventDefault()
                }
            >
              О нас
            </Link>
          </nav>
          <Logout />
        </header>

        <SwitchTransition>
          <CSSTransition
              nodeRef={transitionRef}
              key={location.key}
              timeout={530}
              classNames="main"
              unmountOnExit
          >
            <div ref={transitionRef}>
              <Routes location={location}>
                {routes.map(({ path, Component }) => (
                    <Route key={path} path={path} element={<Component />} />
                ))}
              </Routes>
            </div>
          </CSSTransition>
        </SwitchTransition>
      </>
  );
}
