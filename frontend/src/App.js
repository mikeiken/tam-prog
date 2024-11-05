import './App.css';
import MainPage from './components/main-page/MainPage';
import AuthForm from './components/auth/auth';
import { Routes, Route, useLocation } from 'react-router-dom';
import Header from './components/header/Header';
import NotFound from './components/not-found/NotFound';
import Garden from './components/main-page/Garden/Garden';

function App() {
  const location = useLocation();

  // Header отображается только на конкретных страницах
  const showHeader = !["/", "/login"].includes(location.pathname);

  return (
    <div className="App">

      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<AuthForm />} />
        <Route path="/navigate/*" element={<Header />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}

export default App;
