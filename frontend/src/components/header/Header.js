import React, { useRef } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import Garden from '../main-page/Garden/Garden';
import About from '../main-page/About/about';
import License from '../main-page/License/License';
import Contractor from '../main-page/Contractor/Contractor';
import { CSSTransition, SwitchTransition } from "react-transition-group";
import NotFound from '../not-found/NotFound';
import '../main-page/style.css';

export default function Header() {
    const location = useLocation();

    const routes = [
        { path: 'garden', Component: Garden },
        { path: 'about', Component: About },
        { path: 'license', Component: License },
        { path: 'contractor', Component: Contractor },
    ];

    const isActivePath = (path) => location.pathname === path;

    // Create a ref for the transition
    const transitionRef = useRef(null);

    return (
        <>
            <header className='header'>
                <img className='logo' src={process.env.PUBLIC_URL + '/logo.png'} alt="Logo" />
                <nav className='navbar'>
                    <Link
                        to='garden'
                        onClick={e => isActivePath('/navigate/garden') && e.preventDefault()}
                    >
                        Участки
                    </Link>
                    <Link
                        to='contractor'
                        onClick={e => isActivePath('/navigate/contractor') && e.preventDefault()}
                    >
                        Подрядчики
                    </Link>
                    <Link
                        to='license'
                        onClick={e => isActivePath('/navigate/license') && e.preventDefault()}
                    >
                        Ваши участки
                    </Link>
                    <Link
                        to='about'
                        onClick={e => isActivePath('/navigate/about') && e.preventDefault()}
                    >
                        О нас
                    </Link>
                </nav>
                <Link
                    to='/login'
                    onClick={e => isActivePath('/login') && e.preventDefault()}
                >
                    <button className='login-btn'>Выйти</button>
                </Link>
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
