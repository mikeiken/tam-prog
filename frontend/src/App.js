import './App.css';
import MainPage from './components/main-page/MainPage';
import AuthForm from './components/auth/auth';
import { Routes, Route } from 'react-router-dom';
import Header from './components/header/Header'; // Импортируем Header

function App() {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/" element={<AuthForm />} />
        <Route path="/main" element={<MainPage />} />
      </Routes>
    </div>
  );
}

export default App;
