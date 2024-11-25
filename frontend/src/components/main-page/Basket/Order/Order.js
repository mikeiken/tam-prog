import React, { useState, useEffect } from "react";
import "./order.css";
import Counter from "./Counter/Couter";
import PlantArea from "./PlantArea/PlantArea";

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
                                quantity,
                                date,
                                removeOneFromBasket,
                                item,
                                addToBasket,
                              }) {
  const declension = getDeclension(quantity, "товар", "товара", "товаров");
  const [comment, setComment] = useState("");
  const [selectedPlant, setSelectedPlant] = useState(null); // Состояние для выбранного растения

  // Логируем выбранное растение при его изменении
  useEffect(() => {
    if (selectedPlant) {
      console.log("Выбранное растение:", selectedPlant);
    }
  }, [selectedPlant]);

  return (
      <div className="order-wrapper">
        <div className="order">
          <div className="order-info">
            <div className="order-info-wrapper">
              <div className={"order-image-align"}>
                <img
                    src={process.env.PUBLIC_URL + "/user.png"}
                    alt="object"
                    className="order-image"
                ></img>
              </div>
              <div className="oreder-description">
                {name} - {price} руб. <br />
                Поле №{id}
              </div>
            </div>
            <div className="order-garden-list">
              {" "}
              <PlantArea onPlantSelect={setSelectedPlant} /> {/* Передаем функцию */}
            </div>
          </div>

          <div className="order-order">
            <div>Условия заказа</div>
            <textarea
                className="order-input"
                placeholder="Введите комментарий"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
            ></textarea>

            <div className="order-submit-wrapper">
              <div>Дата заказа: {date}</div>
              <div className="order-change-volume">
                Итог:{" "}
                <Counter
                    id={id}
                    quantity={quantity}
                    removeOneFromBasket={removeOneFromBasket}
                    removeFromBasket={removeFromBasket}
                    item={item}
                    addToBasket={addToBasket}
                />{" "}
                {declension}
              </div>
              <div className="order-selected-plant">
                {selectedPlant ? (
                    <div>Выбрано растение: {selectedPlant.name}</div>
                ) : (
                    "Растение не выбрано"
                )}
              </div>
              <div className="order-submit-button-container">
                <button>Заказать</button>
                <button onClick={() => removeFromBasket(id)}>Отменить</button>
              </div>
            </div>
          </div>
        </div>
      </div>
  );
}
