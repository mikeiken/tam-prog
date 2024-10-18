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
    const location = useLocation();  // Получаем текущее местоположение (маршрут)

    const routes = [
        { path: '/', Component: Garden },
        { path: '/about', Component: About },
        { path: '/license', Component: License },
        { path: '/contractor', Component: Conractor },
    ];

    return (
        <>
            <header className='header'>
                <img className='logo' src={process.env.PUBLIC_URL + '/logo.png'} alt="Logo"></img>
                <nav className='navbar'>
                    <Link to='/'>Участки</Link>
                    <Link to='/contractor'>Подрядчики</Link>
                    <Link to='/license'>Лицензия</Link>
                    <Link to='/about'>О нас</Link>
                </nav>

                <Link to='/login'>
                    <button className='login-btn'>Войти</button>
                </Link>
            </header>

            {/* Оборачиваем в SwitchTransition для плавного переключения страниц */}
            <SwitchTransition>
                <CSSTransition
                    key={location.key}  // Используем уникальный ключ для каждой локации
                    timeout={1000}
                    classNames="main"
                    unmountOnExit
                >
                    <Routes location={location}>
                        {routes.map(({ path, Component }) => (
                            <Route key={path} path={path} element={<Component />} />
                        ))}
                        <Route path='/login' element={<AuthForm />} />
                    </Routes>
                </CSSTransition>
            </SwitchTransition>
        </>
    );
}
