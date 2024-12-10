import React, { useState, useEffect } from "react";

export default function PlotInfoWindow({ item }) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (item) {
      setIsVisible(true);
    } else {
      setIsVisible(false);
    }
  }, [item]);

  return (
    <div className={`container-plot-wrapper ${isVisible ? "visible" : ""}`}>
      <div className="container-plot-info">
        <div className="plot-image-wrapper">
          <img className="plot-card-img" src={item.url} alt="img"></img>
        </div>
        <div className={"container-for-text"}>
          <h3>Лучшее решение для начинающего предпринимателя!</h3>
          <ul>
            <li>Минимальные обязательства</li>
            <li>Простое обслуживание</li>
            <li>Идеально для сезонного использования</li>
            <li>Цена: {item.price}</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
