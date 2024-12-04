import "./App.css";
import LandingPage from "./components/main-page/LandingPage/LandingPage";
import AuthForm from "./components/auth/login/auth";
import { Routes, Route } from "react-router-dom";
import Header from "./components/header/Header";
import NotFound from "./components/not-found/NotFound";
import RegisterForm from "./components/auth/register/RegisterForm";
import Garden from "./components/main-page/Garden/Garden";
import Contractor from "./components/main-page/Contractor/Contractor";
import About from "./components/main-page/About/about";
import PrivateRoute from "./components/auth/private-route/PrivateRoute";
import Basket from "./components/main-page/Basket/Basket";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<AuthForm />} />
        <Route path="/register" element={<RegisterForm />} />

        <Route
          path="/navigate"
          element={
            <PrivateRoute>
              <Header />
            </PrivateRoute>
          }
        >
          <Route path="garden" element={<Garden />} />
          <Route path="contractor" element={<Contractor />} />
          <Route path="license" element={<Basket />} />
          <Route path="about" element={<About />} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}

export default App;
