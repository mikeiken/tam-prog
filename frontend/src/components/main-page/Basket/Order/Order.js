import React, { useState, useEffect, useContext } from "react";
import "./order.css";
import PlantArea from "./PlantArea/PlantArea";
import { CounterContext } from "../../ui/counter/CounterContext";
import Counter from "../../ui/counter/Counter";
import Instance from "../../../api/instance";
import {useNotification} from "../../../context/NotificationContext";

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

export default function Order({
  id,
  name,
  price,
  removeFromBasket,
  date,
  item,
}) {
  const { count } = useContext(CounterContext);
  const declension = getDeclension(count, "грядка", "грядки", "грядок");
  const [comment, setComment] = useState(" ");
  const [selectedPlant, setSelectedPlant] = useState(null); // Состояние для выбранного растения
  const [fertilize, setFertilization] = useState(false);
  const {addNotification} = useNotification()

  function createOrder() {
    Instance.post("order/", {
      field: item.id,
      beds_count: Number(count),
      plant: selectedPlant.id,
      comments: comment,
      fertilize: fertilize,
    })
        .then(() => {
          removeFromBasket(id); // Удаляем элемент из корзины
          addNotification("Заказ создан", "success"); // Добавляем уведомление
        })
        .catch((err) => {
          addNotification(err.message, "error"); // Показываем уведомление об ошибке
        });
  }


  const handleSetFertilizeFalse = () => {
    setFertilization(false);
  };

  const handleSetFertilizeTrue = () => {
    setFertilization(true);
  };

  useEffect(() => {
    if (selectedPlant) {
      console.log(
        "Выбранное поле:",
        item.id,
        "Выбранное растение:",
        selectedPlant.id,
        "количество выбранных грядок:",
        Number(count),
        "Комментарий: ",
        comment,
        "Удобрять?",
        fertilize
      );
    }
  }, [selectedPlant, count]);

  return (
    <div className="order-wrapper">
      <div className="order">
        <div className="order-info">
          <div
            className="order-info-wrapper"
            style={{
              backgroundImage: `url(${item.url})`, // Устанавливаем фон
              backgroundSize: "cover", // Масштабируем фон для заполнения
              backgroundPosition: "center", // Центрируем фон
              backgroundRepeat: "no-repeat", // Избегаем повторения изображения
              borderRadius: "20px",
            }}
          >
            <div className="order-description">
              Поле №{id} <br />
              {name} - {price} руб. <br />
              Свободных грядок: {item.count_free_beds}
            </div>
          </div>
          <div className="order-garden-list">
            {" "}
            <PlantArea onPlantSelect={setSelectedPlant} />{" "}
          </div>
        </div>

        <div className="order-order">
          <div>Условия заказа</div>
          <textarea
            className="order-input"
            placeholder="Введите комментарий"
            onChange={(e) => setComment(e.target.value)}
          ></textarea>
          <div className="order-submit-wrapper">
            <div>Дата заказа: {date}</div>
            <div className="order-change-volume">
              <div className="order-wrapper-itog">
                Итог: <Counter /> {declension}
              </div>
            </div>
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                gap: "20px",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              Удобрять?{" "}
              <div
                style={{
                  display: "flex",
                  flexDirection: "row",
                  gap: "3px",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <button
                  className={
                    fertilize ? "fertilize_btn" + " green" : "fertilize_btn"
                  }
                  onClick={handleSetFertilizeTrue}
                >
                  Да
                </button>
                <button
                  className={
                    fertilize ? "fertilize_btn" : "fertilize_btn" + " red"
                  }
                  onClick={handleSetFertilizeFalse}
                >
                  Нет
                </button>
              </div>
            </div>
            <div className="order-selected-plant">
              {selectedPlant ? (
                <div>Выбрано растение: {selectedPlant.name}</div>
              ) : (
                "Растение не выбрано"
              )}
            </div>
            <div>
              Цена:{" "}
              {item.price * Number(count) +
                (selectedPlant ? selectedPlant.price : 0)}{" "}
              ₽
            </div>
            <div className="order-submit-button-container">
              {selectedPlant ? (
                <button onClick={createOrder}>Заказать</button>
              ) : (
                ""
              )}
              <button onClick={() => removeFromBasket(id)}>Отменить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
