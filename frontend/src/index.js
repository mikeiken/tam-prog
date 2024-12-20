import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import {BrowserRouter} from "react-router-dom";
import {BasketProvider} from "./components/context/BasketContext";
import {NotificationProvider} from "./components/context/NotificationContext";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<NotificationProvider>
    <BasketProvider>
        <BrowserRouter>
            <App/>
        </BrowserRouter>
    </BasketProvider>
</NotificationProvider>);
