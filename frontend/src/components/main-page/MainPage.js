import { useState } from 'react';
import './style.css';
import LoginBtn from './ui/login-btn /LoginBtn';

export default function MainPage() {
    const [loaded, setLoaded] = useState(false);

    const handleLoad = () => {
        setLoaded(true);
    };

    return (
        <>
            <header className='header-for-landing'>
                <div >TAMPROG</div>
                <LoginBtn />
            </header>
            <div className='landing-page'>
                <center>
                    <div className='landing'>
                        <div className='image-container'>
                            <img
                                src={process.env.PUBLIC_URL + '/field1.jpg'}
                                alt='field1'
                                onLoad={handleLoad}
                                className={loaded ? 'loaded' : ''}
                            />
                            <div className='text-overlay landing-container-text'>TAMPROG by BGTUTeam</div>
                        </div>
                        <h1>Мы команда инженеров!</h1>
                        <div className='image-container'>
                            <img
                                src={process.env.PUBLIC_URL + '/field2.jpg'}
                                alt='field2'
                                onLoad={handleLoad}
                                className={loaded ? 'loaded' : ''}
                            />
                            <div className='text-overlay'>Что мы делаем?</div>
                        </div>
                        <div className='image-container'>
                            <img
                                src={process.env.PUBLIC_URL + '/field1.jpg'}
                                alt='field1'
                                onLoad={handleLoad}
                                className={loaded ? 'loaded' : ''}

                            />
                            <div className='text-overlay'>Другой текст</div>
                        </div>
                    </div>
                </center>
            </div>
        </>
    );
}
