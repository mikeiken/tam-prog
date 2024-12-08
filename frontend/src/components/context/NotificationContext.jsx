import React, { createContext, useState, useContext } from "react";

const NotificationContext = createContext();

export const useNotification = () => {
    return useContext(NotificationContext);
};

export const NotificationProvider = ({ children }) => {
    const [notifications, setNotifications] = useState([]);

    const addNotification = (message, type = "info") => {
        const id = Date.now();
        setNotifications((prev) => [
            ...prev,
            { id, message, type, isVisible: false },
        ]);

        setTimeout(() => {
            setNotifications((prev) =>
                prev.map((n) =>
                    n.id === id ? { ...n, isVisible: true } : n
                )
            );
        }, 10); // Задержка минимальная, чтобы сработала анимация

        setTimeout(() => {
            setNotifications((prev) =>
                prev.map((n) =>
                    n.id === id ? { ...n, isVisible: false } : n
                )
            );
        }, 4500);

        setTimeout(() => {
            removeNotification(id);
        }, 5000);
    };

    const removeNotification = (id) => {
        setNotifications((prev) =>
            prev.filter((notification) => notification.id !== id)
        );
    };

    return (
        <NotificationContext.Provider value={{ addNotification }}>
            {children}
            <NotificationList notifications={notifications} />
        </NotificationContext.Provider>
    );
};

const NotificationList = ({ notifications }) => {
    return (
        <div style={{ position: "fixed", bottom: 10, right: 10, zIndex: 9999 }}>
            {notifications.map((notification) => (
                <div
                    key={notification.id}
                    style={{
                        margin: "10px",
                        padding: "15px",
                        backgroundColor: getColor(notification.type),
                        color: "white",
                        borderRadius: "5px",
                        fontSize: "16px",
                        boxShadow: "0 4px 6px rgba(0, 0, 0, 0.3)",
                        maxWidth: "300px",
                        wordWrap: "break-word",
                        opacity: notification.isVisible ? 1 : 0,
                        transform: notification.isVisible
                            ? "translateY(0)"
                            : "translateY(20px)",
                        transition: "opacity 0.5s ease, transform 0.5s ease",
                    }}
                >
                    {notification.message}
                </div>
            ))}
        </div>
    );
};

const getColor = (type) => {
    switch (type) {
        case "success":
            return "green";
        case "error":
            return "red";
        case "warning":
            return "orange";
        default:
            return "blue";
    }
};
