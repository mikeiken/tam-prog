import React from 'react';
import { Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import Garden from '../main-page/Garden/Garden';
import About from '../main-page/About/about';
import License from '../main-page/License/License';
import Contractor from '../main-page/Contractor/Contractor';
import { CSSTransition, SwitchTransition } from "react-transition-group";
import '../main-page/style.css';

export default function Header() {
    const location = useLocation();

    const routes = [
        { path: '/garden', Component: Garden },
        { path: '/about', Component: About },
        { path: '/license', Component: License },
        { path: '/contractor', Component: Contractor },
    ];

    const isActivePath = (path) => location.pathname === path;

    return (
        <>
            <header className='header'>
                <img className='logo' src={process.env.PUBLIC_URL + '/logo.png'} alt="Logo" />
                <nav className='navbar'>
                    <Link
                        to='/garden'
                        onClick={e => isActivePath('/garden') && e.preventDefault()}
                    >
                        Участки
                    </Link>
                    <Link
                        to='/contractor'
                        onClick={e => isActivePath('/contractor') && e.preventDefault()}
                    >
                        Подрядчики
                    </Link>
                    <Link
                        to='/license'
                        onClick={e => isActivePath('/license') && e.preventDefault()}
                    >
                        Лицензия
                    </Link>
                    <Link
                        to='/about'
                        onClick={e => isActivePath('/about') && e.preventDefault()}
                    >
                        О нас
                    </Link>
                </nav>
                <Link
                    to='/'
                    onClick={e => isActivePath('/') && e.preventDefault()}
                >
                    <button className='login-btn'>Войти</button>
                </Link>
            </header>

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
        </>
    );
}
