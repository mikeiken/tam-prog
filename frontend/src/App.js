import './App.css';
import MainPage from './components/main-page/MainPage';
import AuthForm from './components/auth/auth';
import { Routes, Route } from 'react-router-dom';
import Header from './components/header/Header';
import NotFound from './components/not-found/NotFound';

function App() {

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
