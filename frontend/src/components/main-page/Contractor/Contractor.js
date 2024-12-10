import React, { useEffect, useState } from "react";
import Instance from "../../api/instance";
import "./user.css";

const options = {
  year: "numeric",
  month: "long",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  timeZone: "UTC",
};

function getDeclension(quantity, one, few, many) {
  if (quantity % 10 === 1 && quantity % 100 !== 11) {
    return one;
  } else if (
    [2, 3, 4].includes(quantity % 10) &&
    ![12, 13, 14].includes(quantity % 100)
  ) {
    return few;
  } else {
    return many;
  }
}

function correctDate(date) {
  const newDate = new Date(date);
  return newDate.toLocaleString("ru-RU", options);
}

export default function Contractor() {
  const [user, setUser] = useState(null);
  const [orders, setOrders] = useState([]);
  const [workers, setWorkers] = useState({});
  const [plants, setPlants] = useState({});

  const [tooltip, setTooltip] = useState({
    visible: false,
    content: "",
    position: { x: 0, y: 0 },
  });

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalAnimation, setModalAnimation] = useState(false);
  const [amount, setAmount] = useState(""); // Track input amount

  const user_id = localStorage.getItem("user_id");

  useEffect(() => {
    Instance.get(`person/${user_id}`)
      .then((response) => {
        setUser(response.data);
      })
      .catch((error) => console.error("Failed to fetch user data: ", error));
  }, [user_id]);

  useEffect(() => {
    Instance.get("/order/my_orders")
      .then((response) => {
        setOrders(response.data);
      })
      .catch((error) => console.error("Failed to fetch order data: ", error));
  }, [user_id]);

  useEffect(() => {
    const uniqueWorkers = Array.from(
      new Set(orders.map((order) => order.worker).filter(Boolean))
    );

    uniqueWorkers.forEach((workerId) => {
      if (!workers[workerId]) {
        Instance.get(`/worker/${workerId}`)
          .then((response) => {
            setWorkers((prevWorkers) => ({
              ...prevWorkers,
              [workerId]: response.data,
            }));
          })
          .catch((error) =>
            console.error(`Failed to fetch worker ${workerId}:`, error)
          );
      }
    });
  }, [orders, workers]);

  useEffect(() => {
    const uniquePlants = Array.from(
      new Set(orders.map((order) => order.plant).filter(Boolean))
    );

    uniquePlants.forEach((plantId) => {
      if (!plants[plantId]) {
        Instance.get(`/plant/${plantId}`)
          .then((response) => {
            setPlants((prevPlants) => ({
              ...prevPlants,
              [plantId]: response.data,
            }));
          })
          .catch((error) => console.error(error));
      }
    });
  }, [orders]);

  const showTooltip = (description, price, event) => {
    const rect = event.target.getBoundingClientRect();
    setTooltip({
      visible: true,
      content: (
        <>
          <div>Цена: {price ? <u>{price}₽</u> : "Нет данных"}</div>
          <div>Описание: {description || "Нет информации"}</div>
        </>
      ),
      position: {
        x: rect.x + window.scrollX,
        y: rect.y + window.scrollY + rect.height,
      },
    });
  };

  const hideTooltip = () => {
    setTooltip({ visible: false, content: "", position: { x: 0, y: 0 } });
  };

  const handleModalToggle = () => {
    if (!isModalOpen) {
      setIsModalOpen(true);
      setTimeout(() => setModalAnimation(true), 10);
    } else {
      setModalAnimation(false);
      setTimeout(() => setIsModalOpen(false), 400);
    }
  };

  const handleUpdateUser = () => {
    const amountToAdd = parseFloat(amount);

    // Проверяем, что введенная сумма больше нуля
    if (amountToAdd > 0) {
      // Получаем текущий баланс и добавляем к нему введенную сумму
      const newBalance = user?.wallet_balance + amountToAdd;

      Instance.patch(`/person/${user_id}/`, {
        wallet_balance: newBalance,
      })
        .then((response) => {
          setUser((prevUser) => ({
            ...prevUser,
            wallet_balance: response.data.wallet_balance,
          }));
          setAmount("");
          handleModalToggle();
        })
        .catch((error) => {
          console.error("Failed to recharge wallet:", error);
          alert("Произошла ошибка при пополнении баланса.");
        });
    } else {
      alert("Введите корректную сумму.");
    }
  };

  return (
    <div
      className="contractor-wrapper lk-centered"
      style={{ "--font-size": "2em" }}
    >
      <div>
        <div
          style={{
            width: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div className="lk-user-info-wrapper">
            <div className="lk-user-img-wrapper">
              <img
                className={"lk-img"}
                src={process.env.PUBLIC_URL + "/man.jpg"}
                alt="User Avatar"
              />
            </div>
            <div className="lk-user-text-wrapper">
              <div>
                <h1>Имя: {user?.full_name}</h1>
                <p>Номер телефона: {user?.phone_number}</p>
              </div>
              <div className="lk-user-balance">
                <h3>Баланс:</h3>
                <div
                  style={{ display: "flex", flexDirection: "row", gap: "5px" }}
                >
                  <p>{user?.wallet_balance} ₽</p>
                  <img
                    className="lk-plus-img"
                    src={process.env.PUBLIC_URL + "/user_plus.png"}
                    alt="plus"
                    onClick={handleModalToggle}
                    style={{ cursor: "pointer" }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div style={{ width: "100%", height: "auto" }}>
          <div className="lk-user-orders">
            {orders.map((order) => (
              <div key={order.id} className="user-order">
                <div className="user-order-numbers">
                  <div>Заказ #{order.id}</div>
                  <div>Поле #{order.field}</div>
                </div>
                <div
                  style={{
                    width: "122px",
                    height: "100%",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    backgroundColor: "rgb(72, 128, 120, 0.4)",
                    borderRadius: "5px",
                  }}
                >
                  <img
                    className="order-plant-image"
                    src={plants[order.plant] ? plants[order.plant].url : ""}
                    alt={
                      plants[order.plant]
                        ? `Изображение растения ${plants[order.plant].name}`
                        : "Нет изображения"
                    }
                  ></img>
                </div>
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-around",
                    width: "400px",
                    marginRight: "100px",
                    backgroundColor: "rgb(72, 128, 120, 0.4)",
                    borderRadius: "5px",
                    padding: "10px",
                  }}
                >
                  <div>
                    {plants[order.plant]
                      ? plants[order.plant].name
                      : "Загрузка"}{" "}
                    {order.beds_count} {""}
                    {getDeclension(
                      order.beds_count,
                      "грядка",
                      "грядки",
                      "грядок"
                    )}
                  </div>
                  <div>
                    Удобрение:{" "}
                    {order.fertilize ? "Присутствует" : "Отсутствует"}
                  </div>
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "row",
                      justifyContent: "space-between",
                    }}
                  >
                    <div>Стоимость: {order.total_cost} ₽.</div>
                    <div>
                      Выполняет:{" "}
                      <u
                        onMouseEnter={(event) =>
                          showTooltip(
                            workers[order.worker]?.description,
                            workers[order.worker]?.price,
                            event
                          )
                        }
                        onMouseLeave={hideTooltip}
                      >
                        {workers[order.worker]?.name || "Загрузка..."}
                      </u>
                    </div>
                  </div>
                </div>
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    height: "100%",
                    justifyContent: "space-between",
                    width: "400px",
                    backgroundColor: "rgb(72, 128, 120, 0.4)",
                    borderRadius: "5px",
                    padding: "10px",
                  }}
                >
                  <div>Создан: {correctDate(order.created_at)}</div>
                  <div>Срок Выполнения: {correctDate(order.completed_at)} </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {tooltip.visible && (
        <div
          className="tooltip"
          style={{
            position: "absolute",
            top: `${tooltip.position.y - 55}px`,
            left: `${tooltip.position.x + 40}px`,
            backgroundColor: "#BD9F74",
            border: "1px solid rgba(0, 0,0, 0.3)",
            padding: "5px",
            borderRadius: "5px",
            zIndex: 1000,
            whiteSpace: "pre-line",
          }}
        >
          {tooltip.content}
        </div>
      )}

      {isModalOpen && (
        <div
          className="modal"
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0, 0, 0, 0.3)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
            opacity: modalAnimation ? 1 : 0,
            transform: modalAnimation ? "scale(1)" : "scale(1)",
            transition: "opacity 0.5s ease-in-out, transform 0.5s ease-in-out",
          }}
          onClick={handleModalToggle}
        >
          <div
            className="modal-content"
            style={{
              backgroundColor: "rgb(250, 235, 215, 1)",
              padding: "20px",
              borderRadius: "10px",
              maxWidth: "600px",
              maxHeight: "80vh",
              overflowY: "auto",
              filter: "drop-shadow(0px 0px 1px rgba(0, 0, 0, 1))",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2
              style={{
                filter: "drop-shadow(0px 0px 1px rgba(0, 0, 0, 0.7))",
              }}
            >
              Пополнение баланса
            </h2>
            <div
              style={{
                filter: "drop-shadow(0px 0px 1px rgba(0, 0, 0, 0.4))",
              }}
              className="lk-input-wrapper"
            >
              <input
                type="number"
                placeholder="Введите сумму"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                onKeyDown={(e) => {
                  const allowedKeys = [
                    "Backspace",
                    "Tab",
                    "ArrowLeft",
                    "ArrowRight",
                    "Delete",
                  ];
                  if (
                    !/[0-9]/.test(e.key) &&
                    !allowedKeys.includes(e.key) &&
                    !(e.key === "." && !e.target.value.includes("."))
                  ) {
                    e.preventDefault();
                  }
                }}
              />

              <span className="currency-sign">₽</span>
              <button
                style={{
                  filter: "drop-shadow(0px 0px 1px rgba(0, 0, 0, 0.4))",
                }}
                onClick={handleUpdateUser}
              >
                Пополнить
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
