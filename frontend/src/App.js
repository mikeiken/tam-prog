import './App.css';
import MainPage from './components/main-page/MainPage';
import AuthForm from './components/auth/auth';
import { Routes, Route, useLocation } from 'react-router-dom';
import Header from './components/header/Header';

function App() {
  const location = useLocation(); // Получаем текущий путь

  return (
    <div className="App">
      {location.pathname !== "/" && <Header />}

      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<AuthForm />} />
      </Routes>
    </div>
  );
}

export default App;
