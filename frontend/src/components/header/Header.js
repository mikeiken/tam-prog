import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import AuthForm from '../auth/auth';
import Garden from '../main-page/Garden/Garden';
import About from '../main-page/About/about';
import License from '../main-page/License/License';
import Conractor from '../main-page/Contractor/Conractor';
import { CSSTransition, SwitchTransition } from "react-transition-group";
import '../main-page/style.css';

export default function Header() {
    const location = useLocation();  // Получаем текущее местоположение

    const routes = [
        { path: '/', Component: Garden },
        { path: '/about', Component: About },
        { path: '/license', Component: License },
        { path: '/contractor', Component: Conractor },
        { path: '/login', Component: AuthForm }, // Маршрут для AuthForm
    ];

    const isLoginRoute = location.pathname === '/login';

    return (
        <>
            <header className='header'>
                <img className='logo' src={process.env.PUBLIC_URL + '/logo.png'} alt="Logo" />
                <nav className='navbar'>
                    <Link to=''>Участки</Link>
                    <Link to='/contractor'>Подрядчики</Link>
                    <Link to='/license'>Лицензия</Link>
                    <Link to='/about'>О нас</Link>
                </nav>
                <Link to='/login'>
                    <button className='login-btn'>Войти</button>
                </Link>
            </header>

            {!isLoginRoute ? (
                <SwitchTransition>
                    <CSSTransition
                        key={location.key}
                        timeout={530}
                        classNames="main"
                        unmountOnExit
                    >
                        <Routes location={location}>
                            {routes.map(({ path, Component }) => (
                                <Route key={path} path={path} element={<Component />} />
                            ))}
                        </Routes>
                    </CSSTransition>
                </SwitchTransition>
            ) : (
                // Если это /login, показываем компонент без анимации
                <Routes location={location}>
                    {routes.map(({ path, Component }) => (
                        <Route key={path} path={path} element={<Component />} />
                    ))}
                </Routes>
            )}
        </>
    );
}
