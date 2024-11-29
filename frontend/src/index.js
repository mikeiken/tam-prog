import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter } from "react-router-dom";
import { BasketProvider } from "./components/basket-context/BasketContext";
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BasketProvider>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </BasketProvider>
);
